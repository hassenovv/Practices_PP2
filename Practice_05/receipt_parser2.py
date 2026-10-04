#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path

MONEY = r"\d{1,3}(?:[\s\u00a0]\d{3})*,\d{2}|\d+,\d{2}"
QTY = r"\d+(?:[.,]\d{1,3})?"

ITEM_START_RE = re.compile(r"^(\d+)\.$")
ITEM_PRICE_RE = re.compile(rf"^({QTY})\s*[xх×]\s*({MONEY})$", re.IGNORECASE)
MONEY_LINE_RE = re.compile(rf"^({MONEY})$")
DATETIME_RE = re.compile(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})")
TOTAL_RE = re.compile(rf"ИТОГО:\s*\n?\s*({MONEY})", re.IGNORECASE)
VAT_RE = re.compile(rf"НДС\s*(\d+)%:\s*\n?\s*({MONEY})", re.IGNORECASE)
PAYMENT_RE = re.compile(
    rf"^(Банковская карта|Наличные|Безналичн\w*|Карта|Смешанная оплата)\s*:\s*\n?\s*({MONEY})",
    re.IGNORECASE | re.MULTILINE,
)

HEADER_PATTERNS = {
    "company": r"^(Филиал\s.+|ТОО\s.+|ИП\s.+)$",
    "bin": r"БИН\s*(\d{12})",
    "vat_series": r"НДС\s+Серия\s+(\d+)",
    "vat_number": r"^\s*№\s*(\d+)\s*$",
    "cash_register": r"Касса\s+(\S+)",
    "shift": r"Смена\s+(\d+)",
    "receipt_sequence": r"Порядковый номер чека\s*№\s*(\d+)",
    "receipt_number": r"^Чек\s*№\s*(\d+)",
    "cashier": r"Кассир\s+(.+)",
    "fiscal_sign": r"Фискальный признак:\s*\n?\s*(\d+)",
    "address": r"^(г\..+)$",
    "ofd_site": r"сайт:\s*([\w.\-]+\.[a-z]{2,})",
    "ofd_ink": r"ИНК ОФД:\s*(\d+)",
    "kkm_rnm": r"Код ККМ КГД \(РНМ\):\s*(\d+)",
    "znm": r"ЗНМ:\s*(\S+)",
}


def parse_money(text):
    return Decimal(re.sub(r"[\s\u00a0]", "", text).replace(",", "."))


def parse_items(lines):
    items = []
    current = None
    name_parts = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        start = ITEM_START_RE.match(line)
        if start and (current is None or current.get("line_total") is not None):
            current = {"index": int(start.group(1)), "line_total": None}
            name_parts = []
            continue
        if current is None:
            continue

        if "quantity" not in current:
            price = ITEM_PRICE_RE.match(line)
            if price:
                current["name"] = re.sub(r"\s+", " ", " ".join(name_parts)).strip()
                current["quantity"] = Decimal(price.group(1).replace(",", "."))
                current["unit_price"] = parse_money(price.group(2))
            else:
                name_parts.append(line)
        elif current["line_total"] is None:
            total = MONEY_LINE_RE.match(line)
            if total:
                current["line_total"] = parse_money(total.group(1))
                current["prescription"] = current["name"].startswith("[RX]")
                items.append(current)
    return items


def parse_header(text):
    info = {}
    for key, pattern in HEADER_PATTERNS.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            info[key] = match.group(1).strip()
    operator = re.search(r"Оператор фискальных данных:\s*(.+?)(?:Для проверки|\n|$)", text)
    if operator:
        info["ofd_operator"] = operator.group(1).strip()
    return info


def parse_receipt(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    items = parse_items(text.split("\n"))

    moment = None
    match = DATETIME_RE.search(text)
    if match:
        moment = datetime.strptime(f"{match.group(1)} {match.group(2)}", "%d.%m.%Y %H:%M:%S")

    payments = [
        {"method": m.group(1), "amount": parse_money(m.group(2))}
        for m in PAYMENT_RE.finditer(text)
    ]

    match = TOTAL_RE.search(text)
    printed_total = parse_money(match.group(1)) if match else None

    match = VAT_RE.search(text)
    vat = {"rate_percent": int(match.group(1)), "amount": parse_money(match.group(2))} if match else None

    calculated_total = sum((i["line_total"] for i in items), Decimal("0"))

    warnings = []
    for i in items:
        expected = (i["quantity"] * i["unit_price"]).quantize(Decimal("0.01"))
        if expected != i["line_total"]:
            warnings.append(f"Item {i['index']}: {expected} != {i['line_total']}")
    if printed_total is not None and printed_total != calculated_total:
        warnings.append(f"Printed total {printed_total} != sum of items {calculated_total}")
    if payments and printed_total is not None and sum(p["amount"] for p in payments) != printed_total:
        warnings.append("Payments do not add up to printed total")

    return {
        "receipt": parse_header(text),
        "datetime": {
            "iso": moment.isoformat() if moment else None,
            "date": moment.strftime("%Y-%m-%d") if moment else None,
            "time": moment.strftime("%H:%M:%S") if moment else None,
        },
        "items": items,
        "item_count": len(items),
        "units_total": sum((i["quantity"] for i in items), Decimal("0")),
        "payments": payments,
        "totals": {
            "calculated": calculated_total,
            "printed": printed_total,
            "vat": vat,
            "currency": "KZT",
            "matches": printed_total == calculated_total,
        },
        "warnings": warnings,
    }


def json_default(value):
    if isinstance(value, Decimal):
        return float(value) if value % 1 else int(value)
    raise TypeError(f"Not serializable: {type(value)}")


def to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2, default=json_default)


def fmt(value):
    return f"{value:,.2f}".replace(",", " ")


def to_text(data):
    r = data["receipt"]
    out = [
        "=" * 78,
        f"{r.get('company', '?')}  (БИН {r.get('bin', '?')})",
        f"Чек №{r.get('receipt_number', '?')} | Касса {r.get('cash_register', '?')} | "
        f"Смена {r.get('shift', '?')} | Кассир: {r.get('cashier', '?')}",
        f"Дата: {data['datetime']['date']}  Время: {data['datetime']['time']}",
        f"Адрес: {r.get('address', '?')}",
        "=" * 78,
        f"{'#':>2}  {'Наименование':<44}{'Кол-во':>7}{'Цена':>10}{'Сумма':>11}",
        "-" * 78,
    ]
    for i in data["items"]:
        name = i["name"] if len(i["name"]) <= 43 else i["name"][:40] + "..."
        out.append(
            f"{i['index']:>2}  {name:<44}{i['quantity']:>7.0f}"
            f"{fmt(i['unit_price']):>10}{fmt(i['line_total']):>11}"
        )
    out.append("-" * 78)
    summary = f"Позиций: {data['item_count']}, единиц: {int(data['units_total'])}"
    out.append(f"{summary:<55}{'ИТОГО:':>12}{fmt(data['totals']['calculated']):>11}")
    for p in data["payments"]:
        out.append(f"Оплата: {p['method']} - {fmt(p['amount'])} KZT")
    vat = data["totals"]["vat"]
    if vat:
        out.append(f"в т.ч. НДС {vat['rate_percent']}%: {fmt(vat['amount'])} KZT")
    out.append(f"Фискальный признак: {r.get('fiscal_sign', '?')}")
    out.append(f"Проверка суммы: {'OK' if data['totals']['matches'] else 'ОШИБКА'}")
    out.extend(f"! {w}" for w in data["warnings"])
    return "\n".join(out)


def resolve_path(name):
    path = Path(name)
    if path.exists():
        return path
    beside_script = Path(__file__).resolve().parent / name
    if beside_script.exists():
        return beside_script
    sys.exit(
        f"File not found: {name}\n"
        f"Looked in: {Path.cwd()} and {beside_script.parent}"
    )


def main():
    parser = argparse.ArgumentParser(description="Parse a Kazakhstan fiscal receipt text file.")
    parser.add_argument("path", nargs="?", default="raw.txt")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    parser.add_argument("-o", "--output", help="also write JSON to this file")
    args = parser.parse_args()

    path = resolve_path(args.path)
    data = parse_receipt(path.read_text(encoding="utf-8"))

    if args.output:
        Path(args.output).write_text(to_json(data), encoding="utf-8")
    print(to_json(data) if args.json else to_text(data))


if __name__ == "__main__":
    main()

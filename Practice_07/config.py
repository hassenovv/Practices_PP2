"""Reads PostgreSQL connection parameters from database.ini."""
from configparser import ConfigParser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config(filename=os.path.join(BASE_DIR, "database.ini"), section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section(section):
        raise Exception(f"Section [{section}] not found in {filename}")

    return {key: value for key, value in parser.items(section)}


if __name__ == "__main__":
    print(load_config())

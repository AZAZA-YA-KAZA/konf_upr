import py
import pytest
import os

# Импортируем функции из вашего модуля
from main import down_inf, write_obr

# Тестовые данные
TOML_DATA = """
server:
  # host: "localhost"
  port: 8080
  timeout: 30

database:
  user: "admin"
  password: "secret"
  hosts:
    - "host1"
    - "host2"
    - "host3"
"""

EXPECTED_OUTPUT = {'server': ['server -> {', '  % host: "localhost"', '  port ->  8080', '  timeout ->  30', '}'], 'database': ['database -> {', '  user ->  "admin"', '  password ->  "secret"', '  hosts -> <<', '    "host1"', '    "host2"', '    "host3"', '>>', '}']}

EXPECTED_WRITE_OBR_OUTPUT = ['server -> {', '  % host: "localhost"', '  port ->  8080', '  timeout ->  30', '}', 'database -> {', '  user ->  "admin"', '  password ->  "secret"', '  hosts -> <<"host1", "host2", "host3">>', '}']


@pytest.fixture
def create_temp_file(tmp_path):
    """Создает временный файл с тестовыми данными."""
    test_file = tmp_path / "test.toml"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(TOML_DATA.strip())
    return test_file


def test_down_inf(create_temp_file):
    result = down_inf(create_temp_file)
    assert result == EXPECTED_OUTPUT


def test_write_obr():
    result = write_obr(EXPECTED_OUTPUT)
    assert result == EXPECTED_WRITE_OBR_OUTPUT

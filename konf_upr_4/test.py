import pytest

# Импортируем функции из вашего модуля
from assembler import test_bswap

# Тестовые данные
TOML_DATA = ['0x222e', '0x1637', '0x7f79', '0xf625']


def test_bybswap():
    test_bswap()
    with open("log_com.csv", "r") as f:
        arr = []
        for line in f:
            arr.append(line.split(",")[-1][:-1])
    assert arr == TOML_DATA

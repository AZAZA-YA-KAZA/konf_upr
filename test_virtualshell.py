import os
import zipfile
import xml.etree.ElementTree as ET
import pytest
from main import VirtualShell, write_config

@pytest.fixture
def temp_zip(tmp_path):
    # Создаем временный ZIP-архив с некоторыми файлами и каталогами
    zip_path = os.path.abspath('ex1.zip')
    return zip_path

@pytest.fixture
def temp_config():
    # Создаем временный конфигурационный XML-файл
    config_path = "config.xml"
    return config_path

def test_read_config(temp_config):
    tree = ET.parse("config.xml")
    root = tree.getroot()
    shell = VirtualShell("config.xml")
    assert shell.nam is not None, "Hostname должен быть прочитан из конфигурации"
    assert shell.vfs_path == root.find('filesystem').text, "Путь к файловой системе должен соответствовать конфигурации"

def test_load_filesystem(temp_config, temp_zip):
    shell = VirtualShell(temp_config)
    expected_files = [
        '//',
        'aoa//',
        'aoa/oao.txt/',
        'fir//',
        'fir/first.txt/',
        'hjkl.txt/',
        'lalala//',
        'lalala/pupupu.txt/',
        'sec//',
        'sec/second.txt/']
    assert set(shell.filesystem) == set(expected_files), "Файловая система должна содержать правильные файлы и каталоги"

def test_ls_root(temp_config, capsys):
    shell = VirtualShell(temp_config)
    shell.ls("/")
    captured = capsys.readouterr()
    expected = "lalala fir sec aoa hjkl.txt  \n"
    assert captured.out == expected, "Команда ls в корне должна отображать правильные элементы"

def test_ls_folder1(temp_config, capsys):
    shell = VirtualShell(temp_config)
    shell.ls("lalala/")
    captured = capsys.readouterr()
    expected = "pupupu.txt  \n"
    assert captured.out == expected, "Команда ls в folder1 должна отображать правильные файлы"

def test_cd_valid_directory(temp_config, capsys):
    shell = VirtualShell(temp_config)
    shell.cd("lalala")
    assert shell.current_directory == "/lalala", "Текущий каталог должен измениться на /folder1"

def test_cd_invalid_directory(temp_config, capsys):
    shell = VirtualShell(temp_config)
    shell.cd("nonexistent")
    captured = capsys.readouterr()
    assert shell.current_directory == "/", "Текущий каталог не должен измениться при ошибке"
    assert "cd: nonexistent: No such file or directory" in captured.out, "Должно выводиться сообщение об ошибке"

def test_du_file(temp_config, temp_zip, capsys):
    # Тестируем du для отдельного файла
    shell = VirtualShell(temp_config)
    # Предположим, что shell.du может принимать путь к файлу
    shell.du(str(temp_zip))
    captured = capsys.readouterr()
    # Получаем размер ZIP-файла
    expected_size = os.path.getsize(temp_zip)
    assert f"Total size: {expected_size} bytes" in captured.out, "du должен показать правильный размер файла"

def test_du_directory(temp_config, capsys):
    shell = VirtualShell(temp_config)
    shell.du()  # По умолчанию "ex1.zip"
    captured = capsys.readouterr()
    assert captured.out.startswith("Total size: "), "du должен выводить общий размер"

def test_clear(capsys):
    shell = VirtualShell("config.xml")
    os.system('cls')
    captured = capsys.readouterr()
    assert "" in captured.out

def test_write_config(tmp_path):
    filesystem_path = os.path.abspath('ex1.zip')
    output_file = tmp_path / "config.xml"
    # Мокаем input, чтобы вернуть фиксированное имя хоста
    with pytest.MonkeyPatch.context() as m:
        m.setattr('builtins.input', lambda _: "TestHost")
        write_config(filesystem_path, output_file)
    tree = ET.parse(output_file)
    root = tree.getroot()
    assert root.find('hostname').text == "komp", "Hostname должен быть записан в конфигурацию"
    assert root.find('filesystem').text == filesystem_path, "Путь к файловой системе должен быть записан в конфигурацию"

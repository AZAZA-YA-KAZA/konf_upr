import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from main import main
from graph_builder import GraphBuilder


# Тест для обработки недостаточного числа аргументов
def test_main_missing_arguments():
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        main(['main.py'])
        output = mock_stdout.getvalue()
        assert 'Указаны не все данные' in output


# Тест для обработки FileNotFoundError при открытии файла конфигурации
def test_main_file_not_found():
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        with patch('xml.etree.ElementTree.parse', side_effect=FileNotFoundError):
            main(['script.py', 'config.xml', '3'])
        output = mock_stdout.getvalue()
        assert 'Не удаётся открыть конфигурационный файл' in output


# Тест для обработки AttributeError при отсутствии параметров в XML
def test_main_invalid_xml():
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            mock_tree = MagicMock()
            mock_root = MagicMock()
            mock_parse.return_value = mock_tree
            mock_tree.getroot.return_value = mock_root
            mock_root.find.side_effect = AttributeError  # Имитируем ошибку при парсинге XML

            main(['script.py', 'config.xml', '3'])
        output = mock_stdout.getvalue()
        assert 'Неверные параметры конфигурации' in output


# Тест для успешного выполнения, проверка правильности построения графа
@patch('graph_builder.GraphBuilder.build_graph')
@patch('graph_builder.GraphBuilder.draw_graph')
def test_main_success(mock_draw_graph, mock_build_graph):
    mock_build_graph.return_value = None  # Эмулируем успешное построение графа
    mock_draw_graph.return_value = None  # Эмулируем успешную отрисовку

    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        main(['script.py', 'config.xml', '3'])

    mock_build_graph.assert_called_once()  # Проверяем, что метод build_graph был вызван
    mock_draw_graph.assert_called_once()  # Проверяем, что метод draw_graph был вызван


# Тест для метода clear_cache
@patch('os.listdir')
@patch('shutil.rmtree')
@patch('os.makedirs')
def test_clear_cache(mock_makedirs, mock_rmtree, mock_listdir):
    # Эмулируем отсутствие каталога 'cache'
    mock_listdir.return_value = []
    # Вызываем метод clear_cache
    GraphBuilder.clear_cache()
    # Проверяем, что директория cache была создана
    mock_makedirs.assert_called_once_with('cache', exist_ok=True)
    # Эмулируем существование каталога 'cache'
    mock_listdir.return_value = ['cache']

    # Вызываем метод clear_cache снова
    GraphBuilder.clear_cache()
    # Убедимся, что создается заново
    mock_makedirs.assert_called_with('cache', exist_ok=True)  # Этот вызов должен быть вызван после удаления

# Тест для метода build_graph с максимальной глубиной
@patch('graph_builder.GraphBuilder._build_graph')
def test_build_graph_max_depth(mock_build_graph):
    # Эмулируем успешный вызов рекурсивного метода build_graph
    graph_code = '@startuml\n\n\nartifact_1: 1.0\n\n@enduml'
    mock_build_graph.return_value = graph_code

    package = {'group': 'group', 'artifact': 'artifact', 'version': '1.0'}
    code = 'output.puml'
    max_depth = 3

    builder = GraphBuilder()
    builder.build_graph(code, package, max_depth)

    # Проверяем, что файл был записан
    with open(code, 'r') as f:
        content = f.read()
        assert '@startuml' in content
        assert '@enduml' in content
        assert 'artifact_1' in content


# Тест для метода _build_graph
@patch('graph_builder.GraphBuilder.load_xml')
def test_build_graph_logic(mock_load_xml):
    package = {'group': 'group', 'artifact': 'artifact', 'version': '1.0'}
    builder = GraphBuilder()

    # Подготовим мок XML данных
    mock_pom = MagicMock()
    mock_load_xml.return_value = mock_pom
    mock_pom.findall.return_value = []
    # Проверяем, что строится правильный граф
    result = builder._build_graph(package, current_depth=0, max_depth=3)
    assert 'artifact' in result
    assert '1.0' in result
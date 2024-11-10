from sys import argv
from graph_builder import GraphBuilder
import xml.etree.ElementTree as et


def main(args):
    if len(args) < 3:
        print('Указаны не все данные')
        return

    #Путь к конф файлу
    config_path = args[1]
    max_depth = args[2]
    try:
        root = et.parse(config_path).getroot()
    except FileNotFoundError:
        print('Не удаётся открыть конфигурационный файл')
        return

    #Считываем параметры конф файла
    package = dict()
    try:
        p_uml = root.find('PlantUml').text
        package['group'] = root.find('groupId').text
        package['artifact'] = root.find('artifactId').text
        package['version'] = root.find('version').text
        code = root.find('code').text
    except AttributeError:
        print('Неверные параметры конфигурации')
        return

    #Очистка кеша
    if len(args) > 3 and args[3] == '--clear-cache':
        GraphBuilder.clear_cache()

    #Построение графа с учетом глубины
    builder = GraphBuilder()
    builder.build_graph(code, package, max_depth=max_depth)
    GraphBuilder.draw_graph(code, p_uml)


if __name__ == '__main__':
    main(argv)

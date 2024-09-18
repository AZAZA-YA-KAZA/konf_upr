# # import zipfile
# # import xml.etree.ElementTree as ET
# #
# #
# # def ls(a):
# #     pass
# #
# # def test_ls():
# #     res = ls(123)
# #     assert res == a
# #
# #
# # with zipfile.ZipFile('ex1.zip', 'a') as zip:
# #     root = ET.Element('config')
# #
# #     while True:
# #         comand = input('$ ')
# #         if comand == 'exit':
# #             break
# #         elif comand == 'test':
# #             print('Da')
# #         elif comand.startswith('ls '):
# #             ls(1)
# #         else:
# #             print('ti_durakk')
#
# import os
# import zipfile
# import xml.etree.ElementTree as ET
#
#
# class VirtualShell:
#     def __init__(self, config_file):
#         # Чтение конфигурационного файла
#         self.config_file = config_file
#         self.zip = zipfile.ZipFile(config_file, 'a')
#         self.filesystem = {}
#         # self.current_directory = "/"
#         # self.load_filesystem(self.vfs_path)
#
#     def read_config(self, config_file):
#         # Открываем файл в режиме чтения
#         with self.zip_ref.open(config_file, "r") as f:
#             # Возвращаем содержимое файла
#             return f.read()
#
#
#     def ls(self):
#         # Список файлов в текущем каталоге
#         files = [f for f in self.filesystem if f.startswith(self.current_directory)]
#         for file in files:
#             print(os.path.basename(file))
#
#     def cd(self, path):
#         # Изменение текущего каталога
#         new_path = os.path.join(self.current_directory, path)
#         if new_path in self.filesystem:
#             self.current_directory = new_path
#         else:
#             print(f"cd: {path}: No such file or directory")
#
#     def clear(self):
#         os.system('cls' if os.name == 'nt' else 'clear')
#
#     def du(self):
#         # Подсчет общего объема файлов в текущем каталоге
#         total_size = sum(
#             len(self.filesystem[file]) for file in self.filesystem if file.startswith(self.current_directory))
#         print(f"Total size: {total_size} bytes")
#
#     def run(self):
#         # Запуск командного интерфейса
#         while True:
#             command = input(f"{self.hostname}:{self.current_directory}$ ")
#             if command == "exit":
#                 break
#             elif command == "ls":
#                 self.ls()
#             elif command.startswith("cd"):
#                 _, path = command.split(" ", 1)
#                 self.cd(path)
#             elif command == "clear":
#                 self.clear()
#             elif command == "du":
#                 self.du()
#             else:
#                 print(f"{command}: command not found")
#
#
# if __name__ == "__main__":
#     name = input("Enter name of computer ")# получение имени компьютера
#     shell = VirtualShell('conf.xml', name)#Создание эмулятора
#     shell.run()#запуск


import os
import zipfile
import xml.etree.ElementTree as ET


class VirtualShell:
    def __init__(self, config_file):
        # Чтение конфигурационного файла
        self.read_config(config_file)
        # Распаковка виртуальной файловой системы в память
        self.filesystem = []
        self.current_directory = "/"
        self.load_filesystem("ex1.zip")

    def read_config(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()
        self.nam = root.find('hostname').text
        self.vfs_path = root.find('filesystem').text

    def load_filesystem(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            for file in zip_file.namelist():
                self.filesystem.append(file)

    def ls(self, dir):
        # Список файлов в текущем каталоге
        files = []
        for i in range(len(self.filesystem)):
            if dir == 'ex1.zip':
                files.append(self.filesystem[i][self.filesystem[i].rfind("/"):])
            elif self.filesystem[i].find(dir+"/") != -1 and (len(self.filesystem[:self.filesystem[i].find(dir+"/")]) == 0):
                files.append(self.filesystem[i][self.filesystem[i].find(dir)+len(dir):])
        for file in files:
            print(os.path.basename(file), end=" ")
        print()

    def cd(self, path):
        # Изменение текущего каталога
        fil = ""
        for i in range(len(self.filesystem)):
            if self.filesystem[i][:self.filesystem[i].find("/")] == path:
                fil = self.filesystem[i]
        if "".join(fil) != "":
            self.current_directory = "/"+path
        elif path == 'ex1.zip':
            self.current_directory = "/"
        else:
            print(f"cd: {path}: No such file or directory")

    def clear(self):
        print("Работает в консоли, не в PyCharm")
        os.system('cls')

    def du(self, start_path="ex1.zip"):
        # Подсчет общего объема файлов в текущем каталоге
        total_size = 0
        # Проверяем, является ли путь файлом
        if os.path.isfile(start_path):
            total_size = os.path.getsize(start_path)
        else:
            # Если это каталог, рекурсивно обходим все файлы в нем
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        print(f"Total size: {total_size} bytes")

    def run(self):
        # Запуск командного интерфейса
        while True:
            command = input(f"{self.nam}:{self.current_directory}$ ")
            if command == "exit":
                break
            elif command.startswith("ls"):
                if len(command.split()) > 1:
                    _, pu = command.split(" ", 1)
                else:
                    pu = "ex1.zip"
                self.ls(pu)
            elif command.startswith("cd"):
                if len(command.split()) > 1:
                    _, path = command.split(" ", 1)
                else:
                    path = "ex1.zip"
                self.cd(path)
            elif command == "clear":
                self.clear()
            elif command == "du":
                self.du()
            else:
                print(f"{command}: command not found")


def write_config(filesystem_path, output_file):
    # Создаем корневой элемент <config>
    root = ET.Element("config")
    # Добавляем элемент
    nam = input("Enter name of computer ")
    hostname_elem = ET.SubElement(root, 'hostname')
    hostname_elem.text = nam

    # Добавляем элемент <filesystem>
    filesystem_elem = ET.SubElement(root, "filesystem")
    filesystem_elem.text = filesystem_path

    # Создаем дерево XML и записываем в файл
    tree = ET.ElementTree(root)
    with open(output_file, "wb") as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)


if __name__ == "__main__":
    script_path = os.path.abspath('ex1.zip')
    write_config(script_path, "config.xml")
    shell = VirtualShell('config.xml')
    shell.run()

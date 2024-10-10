import os
import zipfile
import xml.etree.ElementTree as ET


class VirtualShell:

    def __init__(self, config_file=None):
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
                self.filesystem.append(file+"/")
                if not file.endswith('/'):
                    directory = '/'.join(file.split('/')[:-1]) + '/'
                    if directory not in self.filesystem:
                        self.filesystem.append(directory+"/")

    def ls(self, dir):
        # Список файлов в текущем каталоге
        files = []
        for i in range(len(self.filesystem)):
            if dir == '/':
                if self.filesystem[i][:self.filesystem[i].find("/")+1] not in files:
                    files.append(self.filesystem[i][:self.filesystem[i].find("/")+1])
            elif self.filesystem[i].find(dir) != -1 and (len(self.filesystem[i][self.filesystem[i].find(dir)+len(dir):]) != 0):
                files.append(self.filesystem[i][self.filesystem[i].find(dir)+len(dir):])
        for file in files:
            print(file[:-1], end=" ")
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
                self.ls(self.current_directory[1:]+"/")
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

def sam():
    script_path = os.path.abspath('ex1.zip')
    write_config(script_path, "config.xml")
    shell = VirtualShell('config.xml')
    shell.run()


if __name__ == "__main__":
    sam()

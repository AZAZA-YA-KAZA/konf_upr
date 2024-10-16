# Задание 1 - Разработка эмулятора
## Вариант №9
## 1. Постановка задачи:
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС. Эмулятор должен запускаться из реальной командной строки, а файл с виртуальной файловой системой не нужно распаковывать у пользователя. Эмулятор принимает образ виртуальной файловой системы в виде файла формата **zip**. Эмулятор должен работать в режиме **CLI**.
### Конфигурационный файл имеет формат xml и содержит:
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
### Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
1. clear.
2. du.
Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 3 теста.
## 2. Запуск
Для автоматической сборки запустите файл bash.sh

Перед запуском необходимо клонировать репозиторий в среду разработки
Запуск main.py: python main.py
```Bash
python main.py
```
```Bash
pytest test_virtualshell.py
```
Запуск тестов
# Необходимые библиотеки и их установка
```Bash
pip install pytest
```
библиотека для тестов
## 2. Функции настройки:
1. def read_config(self, config_file): - Чтение xml файла 
2. def load_filesystem(self, zip_path): - Чтение zip файла
3. def ls(self, dir): - Список файлов в текущем каталоге
4. def cd(self, path): - Изменение текущего каталога
5. def clear(self): - Очищение консоли
6. def du(self, start_path="ex1.zip"): - Подсчет общего объема файлов в текущем каталоге
7. def run(self): - Запуск командного интерфейса
8. def write_config(filesystem_path, output_file): - Создание xml файла
## 3. Описание команд для сборки проекта
1. ls - Вывод файлов (после команды вводить либо директорию, либо ничего)
2. cd - Смена каталога (после команды вводить либо директорию, либо ничего)
3. exit - Выход из эмулятора (после команды ничего не вводить)
4. clear - Очистка консоли (после команды ничего не вводить)
5. du - Объем файлов в каталоге (после команды вводить либо директорию, либо ничего)
## 3. Тестирование
### 1. ls
![image](https://github.com/user-attachments/assets/0216eb59-044a-4138-9308-7a7af03640e7)
![image](https://github.com/user-attachments/assets/85d31635-e518-4972-a8f3-ab7e82190cb0)
### 2. cd
![image](https://github.com/user-attachments/assets/69530154-3160-4070-9e35-bb52a1dc5db3)
### 3. exit - Выход из эмулятора
![image](https://github.com/user-attachments/assets/c1c2d849-366e-4b62-8303-7a2e7744f071)
### 4. clear - Очистка консоли
![image](https://github.com/user-attachments/assets/3909f8d2-92b9-46a7-8e6c-fc40704312e9)
### 5. du - Объем файлов в каталоге
![image](https://github.com/user-attachments/assets/2129d2dc-e7a7-462e-baec-eb126438f592)
## Общие тесты через pytest
![image](https://github.com/user-attachments/assets/01d2809d-ae88-4632-a7ac-649553d11846)


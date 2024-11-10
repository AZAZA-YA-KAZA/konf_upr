## Задание 2 - Разработка инструмента командной строки для визуализации графа зависимостей
## Вариант №9
## Постановка задачи
Разработать инструмент командной строки для визуализации графа 
зависимостей, включая транзитивные зависимости. Сторонние средства для 
получения зависимостей использовать нельзя.

Зависимости определяются по имени пакета языка Java (Maven). Для 
описания графа зависимостей используется представление PlantUML. 
Визуализатор должен выводить результат на экран в виде графического 
изображения графа.


Ключами командной строки задаются:

• Путь к программе для визуализации графов.

• Имя анализируемого пакета.

• Максимальная глубина анализа зависимостей.

Все функции визуализатора зависимостей должны быть покрыты тестами.

# 1. Запуск
Для автоматической сборки запустите файл bash.sh
Перед запуском необходимо клонировать репозиторий в среду разработки
```
git clone <ссылка на репозиторий>
```
# Необходимые библиотеки и их установка
```Bash
pip install pytest
```
библиотека для тестов
# Переход в директорию
```shell
cd konf_upr_2
```
# Установка зависимостей
```shell
pip install -r requirements.txt
```
# Запуск программы
```shell
python main.py pom.xml 5
```
# Тестирование
```shell
pytest -v
```
# Конфигурационный файл
Пример файла:
```xml
<config>
    <PlantUml>PlantUml/plantuml-1.2024.7.jar</PlantUml>
    <code>PlantUml/graph_2.txt</code>
    <groupId>aws.smithy.kotlin</groupId>
    <artifactId>http-jvm</artifactId>
    <version>1.2.10</version>
</config>
```
Где:

- **PlantUml** - Путь к программе отрисовки графа
- **code** - Путь к файлу-результату в виде кода
- **groupId**, **artifactId**, **version** - Характеристики пакета с сайта [Maven](https://mvnrepository.com/)

## 2. Функции настройки:
1. def clear_cache(): Очистка кеша
2. def load_xml(self, package: dict[str, str]): Загрузка пакетов
4. def build_graph(self, code: str, package: dict[str, str], max_depth: int = None): Запись файла .txt
5. def buildgraph(self, package: dict[str, str], current_depth: int = 0, max_depth: int = None): Построение структуры файла .txt
6. def fix_version(self, version): Версия конфигурации
7. def draw_graph(code, p_uml): Генерация диаграммы UML
## 3. Тестирование
![image](https://github.com/user-attachments/assets/08cdcbad-d129-4383-ad17-06ce116f9d98)
# Примеры работы
### 1. python main.py pom.xml 1
![image](https://github.com/user-attachments/assets/26ad7e87-1610-4f49-8b61-c40f94c67532)
### 2. python main.py conf.xml 3
![image](https://github.com/user-attachments/assets/af9e60fa-0a57-4136-932f-bc22c4cffa80)
### 3. exit - Выход из эмулятора
![image](https://github.com/user-attachments/assets/c1c2d849-366e-4b62-8303-7a2e7744f071)
### 4. clear - Очистка консоли
![image](https://github.com/user-attachments/assets/3909f8d2-92b9-46a7-8e6c-fc40704312e9)
### 5. du - Объем файлов в каталоге
![image](https://github.com/user-attachments/assets/2129d2dc-e7a7-462e-baec-eb126438f592)
## Общие тесты через pytest
![image](https://github.com/user-attachments/assets/01d2809d-ae88-4632-a7ac-649553d11846)

from sys import argv


def down_inf(file):
    toml_data = {}
    section = None
    current_array = None

    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.rstrip()  # Убираем символы переноса строки
                if not line:
                    continue  # Пропускаем пустые строки и комментарии
                # Преобразование однострочных комментариев в структуру с %
                if line.lstrip().startswith('#'):
                    comment = line.lstrip()[1:].strip()
                    if comment:
                        if section not in toml_data:
                            toml_data[section] = []
                        toml_data[section].append(f'%{comment}')
                    continue

                # Разделение секции (если строка начинается с имени секции)
                if line[0] != " " and line[0] != "-":
                    section = line.strip()[:-1]
                    if section not in toml_data:
                        toml_data[section] = []
                    toml_data[section].append(f"{section} ->")  # Секцию записываем как "section ->"
                    continue

                line = line.lstrip()
                # Если строка начинается с "-", это элемент массива
                if line.startswith("-"):
                    value = line[1:].strip()  # Убираем дефис и пробел
                    toml_data[section].append("  "+value)
                    continue

                # Если массив завершился, добавляем закрывающий символ ">>"
                if current_array is not None:
                    toml_data[section].append(">>")
                    current_array = None

                # Разделение ключа и значения (для словаря и констант)
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    # Если значение пустое, это начало словаря
                    if value == "":
                        toml_data[section].append(f"{key} -> {{")
                        continue

                    # Запись ключа -> значения для констант
                    toml_data[section].append(f"{key} -> {value}")
                else:
                    # Если нет ":" - это ошибка или ошибка в формате
                    raise SyntaxError(f"Ошибка синтаксиса на строке {line_number}: '{line}'")

            # Закрытие открытых словарей
            if current_array is not None:
                toml_data[section].append(">>")
                current_array = None

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")

    return toml_data

def generate_custom_config(toml_data):
    lines = []

    def process_value(value):
        if isinstance(value, str):
            # Проверка, является ли строка числом
            try:
                if '.' in value:
                    return float(value)  # Если есть точка, преобразуем в float
                else:
                    return int(value)  # Иначе преобразуем в int
            except ValueError:
                # Если не число, проверяем, содержит ли строка буквы
                if any(char.isalpha() for char in value):  # Проверка на наличие букв
                    return f'[[{value}]]'  # Оборачиваем в [[ ]]
                return f'"{value}"'  # Если не буквы, возвращаем как строку
        elif isinstance(value, list):
            # Обработка списка, чтобы каждый элемент был в отдельных двойных квадратных скобках
            return ', '.join([f'[[{item}]]' for item in value])
        else:
            return str(value)

    for key, value in toml_data.items():
        if isinstance(value, dict):
            lines.append(f"{key} = {{")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, list):
                    # Если sub_value - это список, то обрабатываем его отдельно
                    formatted_value = ', '.join([f'[[{item}]]' for item in sub_value])
                    lines.append(f"    {sub_key} = list({formatted_value});")
                else:
                    lines.append(f"    {sub_key} = {process_value(sub_value)};")
            lines.append("}")
        else:
            lines.append(f"var {key} = {process_value(value)};")

    return "\n".join(lines).replace('"', '')


def main(args):
    if len(args) < 3:
        print('Указаны не все данные')
        return
    #Путь к файлу
    input_path = args[1]
    output_path = args[2]
    info = down_inf(input_path)
    if info is None:
        return  # Если есть синтаксическая ошибка, выходим
    for key in info:
        for i in info[key]:
            print(i)
    try:
        with open(output_path, 'w') as f:
            for key in info:
                for i in info[key]:
                    print(i)
                    f.write(i+'\n')
    except Exception as e:
        print(f"Ошибка при записи в файл '{output_path}': {e}")


if __name__ == "__main__":
    main(argv)
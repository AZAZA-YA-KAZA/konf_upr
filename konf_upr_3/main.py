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
                    comment = line.replace('#', '%', 1)
                    if comment:
                        if section not in toml_data:
                            toml_data[section] = []
                        toml_data[section].append(comment)
                    continue

                # Разделение секции (если строка начинается с имени секции)
                if line[0] != " " and line[0] != "-":
                    if len(toml_data) > 0:
                        toml_data[section].append("}")
                    section = line[:-1]
                    if section not in toml_data:
                        toml_data[section] = []
                    toml_data[section].append(f"{section} -> {{")  # Секцию записываем как "section ->"
                    continue

                # Если строка начинается с "-", это элемент массива
                if line.lstrip().startswith("-"):
                    if current_array is None:
                        toml_data[section][-1] = toml_data[section][-1][:-1]+"<<"
                        current_array = value
                    value = line.replace('- ', '', 1) # Убираем дефис
                    toml_data[section].append(value)
                    continue
                # Если массив завершился, добавляем закрывающий символ ">>"
                if current_array is not None:
                    toml_data[section].append(">>")
                    current_array = None

                # Разделение ключа и значения (для словаря и констант)
                if ':' in line:
                    key, value = line.split(':', 1)

                    # Если значение пустое, это начало словаря
                    if value == "":
                        toml_data[section].append(f"{key} -> {{")
                        continue

                    # Запись ключа -> значения для констант
                    toml_data[section].append(f"{key} -> {value}")
                else:
                    # Если нет ":" - это ошибка или ошибка в формате
                    raise SyntaxError(f"Ошибка синтаксиса на строке {line_number}: '{line}'")

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")

    # Если массив завершился, добавляем закрывающий символ ">>"
    if current_array is not None:
        toml_data[section].append(">>")
    toml_data[section].append("}")

    return toml_data

def write_obr(file):
    list = []
    t = ""
    for key in file:
        f = False
        ff = False
        for i in file[key]:
            if '>>' in i:
                f = False
                ff = False
                t += i
                list.append(t)
                t = ""
                continue
            if f:
                if not ff:
                    t += i.strip()
                    ff = True
                else:
                    t+= ', ' + i.strip()
                continue
            else:
                t = i
            if '-> <<' in i:
                f = True
                continue
            list.append(t)
    return list


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
    info = write_obr(info)
    try:
        with open(output_path, 'w') as f:
            for i in info:
                f.write(i+'\n')
    except Exception as e:
        print(f"Ошибка при записи в файл '{output_path}': {e}")


if __name__ == "__main__":
    main(argv)
import csv
import struct
from sys import argv

# Таблица операций
INSTRUCTIONS = {
    99: "LOAD_CONST",  # Загрузка константы
    96: "LOAD_MEM",  # Чтение значения из памяти
    1: "STORE_MEM",  # Запись значения в память
    82: "BSWAP",  # Унарная операция: BSWAP
}


# Функция для выполнения команды
def execute_command(command, memory):
    if command >> 9 != 82:
        opcode = command >> 25  # Опкод занимает первые 7 бит
        if opcode == 99:  # LOAD_CONST
            b = (command >> 21) & 0xF  # Адрес регистра для результата
            c = command & 0xFFF  # Константа или адрес
            memory[b] = c
            return f"LOAD_CONST: R[{b}] = {c}"

        elif opcode == 96:  # LOAD_MEM
            b = (command >> 21) & 0xF  # Адрес регистра для результата
            c = command & 0xFFF  # Константа или адрес
            memory[b] = memory.get(c, 0)  # Чтение из памяти по адресу C
            return f"LOAD_MEM: R[{b}] = MEM[{c}] = {memory[b]}"

        elif opcode == 1:  # STORE_MEM
            b = (command >> 5) & 0xFFF  # Адрес регистра для результата
            c = command & 0xF  # Константа или адрес
            memory[c] = memory.get(b, 0)  # Запись в память по адресу C
            return f"STORE_MEM: MEM[{c}] = R[{b}] = {memory[c]}"
    else:  # BSWAP
        opcode = command >> 9  # Опкод занимает первые 7 бит
        b = (command >> 5) & 0xF  # Адрес регистра для результата
        c = (command >>1)& 0xF  # адрес
        memory[b] = memory.get(b, 0)  # Инвертирование байтов
        return f"BSWAP: R[{c}] = R[{b}] = {memory[b]}"
    return f"Unknown opcode: {opcode}"


# Интерпретатор
def interpreter(input_file, memory_range, output_file):
    memory = {i: 0 for i in range(memory_range[0], memory_range[1] + 1)}  # Инициализация памяти

    with open(input_file, "rb") as infile, open(output_file, "w", newline="") as csvfile:
        log_writer = csv.writer(csvfile)
        log_writer.writerow(["Command", "Memory State"])
        while True:
            byte = infile.read(4)  # Чтение 4 байт за раз
            if len(byte) < 2:
                break  # Если прочитано меньше 4 байт, выходим из цикла
            if len(byte)==2:
                command = int(bytes(reversed(byte)).hex()[-16:], 16)
            else:
                command = int(byte.hex()[-16:], 16)  # Преобразование в целое число (big-endian)
            result = execute_command(command, memory)
            log_writer.writerow([result, memory.copy()])  # Запись состояния памяти после выполнения команды


# Вызов интерпретатора
if __name__ == "__main__":
    # Чтение результата из бинарного файла
    if len(argv) < 4:
        print("Недостаточно аргументов. Укажите входной файл, диапазон памяти и выходной файл.")
    else:
        input_file = argv[1]
        memory_range = list(map(int, argv[3].split("-")))
        output_file = argv[2]
        interpreter(input_file, memory_range, output_file)
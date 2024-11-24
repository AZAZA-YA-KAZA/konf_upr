import csv
import struct
from sys import argv

# Таблица операций
INSTRUCTIONS = {
    "LOAD_CONST": 99,
    "LOAD_MEM": 96,
    "STORE_MEM": 1,
    "BSWAP": 82,
}


# Функция сборки команды
def assemble_command(instruction, operands):
    opcode = INSTRUCTIONS[instruction]
    binary_data = bytearray()
    log_data = []
    if instruction == "LOAD_CONST":
        b, c = operands
        word = (opcode << 25) | (b << 21) | (c) #(30-7 и тд)
        binary_data.extend(reversed(word.to_bytes(4, byteorder='little')))
        log_data.append([instruction, opcode, b, c, f"0x{hex(word)}"])
    elif instruction == "LOAD_MEM":
        b, c = operands
        word = (opcode << 25) | (b << 21) | c
        binary_data.extend(reversed(word.to_bytes(4, byteorder='little')))
        log_data.append([instruction, opcode, b, c, f"0x{binary_data[-6:].hex()}"])
    elif instruction == "STORE_MEM":
        b, c = operands
        word = (opcode << 25) | (b << 5) | c
        binary_data.extend(reversed(word.to_bytes(4, byteorder='little')))
        log_data.append([instruction, opcode, b, f"{c}=0x{binary_data[-6:].hex()}"])
    #инвертирование порядка байтов
    elif instruction == "BSWAP":
        b, c = operands
        if b < 4:
            word = (opcode << 9) | (b << 5) | (c << 1)
        else:
            word = c
        binary_data.extend(word.to_bytes(2, byteorder='little'))
        log_data.append([instruction, opcode, b, c, f"0x{binary_data[-6:].hex()}"])
    else:
        raise ValueError(f"Unknown instruction: {instruction}")
    return binary_data, log_data


# Ассемблер
def assembler(arg):
    if len(arg) < 3:
        print('Указаны не все данные')
        return
    input_file = arg[1]
    output_file = arg[2]
    log_file = arg[3]
    with (open(input_file, "r") as infile,
          open(output_file, "wb") as outfile,
          open(log_file, "w", newline="") as logfile):
        log_writer = csv.writer(logfile) #Создание объекта записи CSV
        for line in infile:
            parts = line.strip().split()
            instruction = parts[0]
            operands = list(map(int, parts[1:]))
            binary, log = assemble_command(instruction, operands)
            outfile.write(binary) # Запись бинарных данных в выходной файл
            for i in log:
                print(i)
            log_writer.writerows(log) #Запись лога


# Тестовая программа для выполнения BSWAP над вектором длины 4
def test_bswap():
    vector = [11810, 14102, 31103, 9718]  # Исходный вектор
    print("Исходный вектор:", [hex(x) for x in vector])
    # Создаем команды для BSWAP для каждого элемента вектора
    commands = []
    for i in range(len(vector)):
        commands.append(f"BSWAP {i+4} {vector[i]}")
    # Записываем команды в файл для ассемблера
    with open("commands.txt", "w") as f:
        for command in commands:
            f.write(command + "\n")

    # Запускаем ассемблер
    assembler(["assembler.py", "commands.txt", "output_comm.bin", "log_com.csv"])

# Вызов ассемблера
if __name__ == "__main__":
    assembler(argv)
    test_bswap()

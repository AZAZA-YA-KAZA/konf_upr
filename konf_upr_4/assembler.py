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
    if instruction in ["LOAD_CONST", "LOAD_MEM"]:
        b, c = operands
        return struct.pack("<I", (opcode << 24) | (b << 20) | c)
    elif instruction == "STORE_MEM":
        b, c = operands
        return struct.pack("<I", (opcode << 24) | (b << 6) | c)
    elif instruction == "BSWAP":
        b, c = operands
        return struct.pack("<I", (opcode << 24) | (b << 16) | c)
    else:
        raise ValueError(f"Unknown instruction: {instruction}")


# Ассемблер
def assembler(arg):
    if len(arg) < 3:
        print('Указаны не все данные')
        return
    input_file = arg[1]
    output_file = arg[2]
    log_file = arg[3]
    with (open(input_file, "r") as infile,
          open(output_file, "w", newline="") as outfile,
          open(log_file, "w", newline="") as logfile):
        log_writer = csv.writer(logfile)
        for line in infile:
            parts = line.strip().split()
            instruction = parts[0]
            operands = list(map(int, parts[1:]))
            binary = assemble_command(instruction, operands)
            outfile.write(binary)
            log_writer.writerow([line.strip(), binary.hex()])


# Вызов ассемблера
if __name__ == "__main__":
    assembler(argv)

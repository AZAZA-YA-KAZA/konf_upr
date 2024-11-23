import struct
import sys
import csv

# Память и регистры
REGISTERS = [0] * 32
MEMORY = [0] * 1024


# Интерпретация команды
def execute_command(binary):
    opcode = (binary >> 24) & 0xFF
    if opcode == 99:  # LOAD_CONST
        b = (binary >> 20) & 0xF
        c = binary & 0xFFFFF
        REGISTERS[b] = c
    elif opcode == 96:  # LOAD_MEM
        b = (binary >> 20) & 0xF
        c = binary & 0xFFFFF
        REGISTERS[b] = MEMORY[c]
    elif opcode == 1:  # STORE_MEM
        b = (binary >> 6) & 0x3FFFF
        c = binary & 0x3F
        MEMORY[b] = REGISTERS[c]
    elif opcode == 82:  # BSWAP
        b = (binary >> 5) & 0xF
        c = binary & 0xF
        REGISTERS[c] = int.from_bytes(REGISTERS[b].to_bytes(4, "little"), "big")
    else:
        raise ValueError(f"Unknown opcode: {opcode}")


# Интерпретатор
def interpreter(binary_file, result_file, memory_range):
    with open(binary_file, "rb") as bfile:
        while chunk := bfile.read(4):
            binary = int.from_bytes(chunk, "little")
            execute_command(binary)

    start, end = map(int, memory_range.split(":"))
    with open(result_file, "w", newline="") as rfile:
        writer = csv.writer(rfile)
        writer.writerow(["Address", "Value"])
        for i in range(start, end + 1):
            writer.writerow([i, MEMORY[i]])


# Вызов интерпретатора
if __name__ == "__main__":
    binary_path = sys.argv[1]
    result_path = sys.argv[2]
    memory_range = sys.argv[3]
    interpreter(binary_path, result_path, memory_range)

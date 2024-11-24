cd konf_upr_4
pytest test.py
python assembler.py program.txt output.bin log.csv
python interpretator.py output.bin result.csv 0-600
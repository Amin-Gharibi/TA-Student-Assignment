# GROUP PAIRS AND PERSIAN EVAL OF ENGLISH NAMES
NAMES_EVALS = {
    # SAMPLE DATA:
    # "Zahra Nazari": "زهرا نظری - نرگس سارایی",
    # "amir davari": "امیر داوری",
}

# NAMES OF STUDENTS WHO UPLOADED THE CURRENT HW
current_names = [
    # SAMPLE DATA:
    # "Soheil Ramedan",
    # "حسین نامجو",
]

with open('./students.txt', 'w') as file:
    print("Writing Names to the file...")
    for name in current_names:
        file.write(NAMES_EVALS.get(name, name) + '\n')
    print("Writing Names done...")

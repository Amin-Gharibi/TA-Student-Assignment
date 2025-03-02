# TA-Student Assignment System

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

A Python application for automatically assigning students to Teaching Assistants (TAs) for academic presentations or meetings, with time slot scheduling and optimization.

## 📝 Description

This tool helps course administrators efficiently assign students to TAs for presentations, evaluations, or meetings while:
- Ensuring balanced workload among TAs
- Preventing students from being assigned to the same TA multiple times
- Creating an organized schedule with appropriate time slots
- Generating professional Excel reports

## ✨ Features

- **Smart Assignment Algorithm**: Balances TA workload and considers previous assignments
- **Time Slot Scheduling**: Automatically assigns specific time slots based on TA availability
- **Excel Reporting**: Generates professional Excel reports with multiple views:
  - Full assignment details (student, TA, start time, end time)
  - Private assignment list (student-TA pairings only)
  - Summary statistics for each TA
- **Fallback Text Output**: Creates simple text files when Excel generation fails
- **Support for Persian Font**: Uses Vazirmatn font for better display of Persian text (when available)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Amin-Gharibi/TA-Student-Assignment.git
cd TA-Student-Assignment
```

2. Install dependencies using Poetry:
```bash
poetry install
```

Alternatively, you can install dependencies using pip:
```bash
pip install pandas openpyxl
```

## 📊 Input File Formats

### Students File (`students.txt`)
Simple text file with one student name per line:
```
Student1
Student2
Student3
```

### TAs File (`tas.txt`)
Each line contains TA name, start time, and end time (comma-separated):
```
TA1, 09:00, 12:00
TA2, 10:30, 14:30
TA3, 13:00, 17:00
```

### Previous Assignments Files (optional)
Files containing previous student-TA assignments to avoid repetition:
```
Student1, TA1
Student2, TA3
```

## 🔧 Configuration

Configuration constants are located in `main.py`:

```python
PRESENTATION_TIME: int = 30  # in minutes
TA_FILEPATH: str = './tas.txt'
STUDENTS_FILEPATH: str = './students.txt'
PREVIOUS_ASSIGNMENT_FILES: List[str] = []
FONT_FILEPATH: str = './Vazirmatn-Regular.ttf'
```

## 📋 Usage

Run the application:

```bash
python main.py
```

## 📁 Output Files

The program generates:

1. **assignment_results.xlsx**: Excel file with multiple sheets
   - Full Assignments: Complete details including time slots
   - Private Assignments: Only student-TA pairings
   - Summary: Statistics for each TA

2. **private-result.txt**: Simple text file with student-TA pairings

## 🧠 How It Works

1. **Input Parsing**: Reads student names and TA availability
2. **Previous Assignment Analysis**: Considers past assignments to avoid repetition
3. **Assignment Algorithm**: 
   - Attempts to assign students to TAs they haven't had before
   - Balances workload across TAs
   - Respects TA time constraints
4. **Schedule Generation**: Creates specific time slots for each student
5. **Report Creation**: Generates Excel and text output files

## 📁 Project Structure

- **main.py**: Entry point and configuration constants
- **parsers.py**: Functions for parsing input files
- **assignment_algo.py**: Core assignment algorithm
- **util.py**: Utilities for Excel report generation
- **eval_student_names.py**: Helper for student name evaluation

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Amin-Gharibi/TA-Student-Assignment/issues).

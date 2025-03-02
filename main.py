from typing import List
from parsers import parse_student_file, parse_ta_file, parse_previous_assignments
from assignment_algo import balanced_assignment

# CONSTANTS
PRESENTATION_TIME: int = 30  # in minutes
TA_FILEPATH: str = './tas.txt'
STUDENTS_FILEPATH: str = './students.txt'
PREVIOUS_ASSIGNMENT_FILES: List[str] = []
FONT_FILEPATH: str = './Vazirmatn-Regular.ttf'


def main() -> None:
    # Parse input files
    students = parse_student_file(STUDENTS_FILEPATH)
    tas, availability, ta_start_times = parse_ta_file(TA_FILEPATH)
    previous_assignments = parse_previous_assignments(PREVIOUS_ASSIGNMENT_FILES)

    if not students:
        print("Error: No students found.")
        return

    if not tas:
        print("Error: No TAs found.")
        return

    print(f"Found {len(students)} students and {len(tas)} TAs.")

    # Run the assignment algorithm
    assignments = balanced_assignment(
        students,
        tas,
        availability.copy(),
        ta_start_times,
        previous_assignments
    )

    # Print summary
    print("\nAssignment Summary:")
    for ta, assigned_students in assignments.items():
        print(f"{ta}: {len(assigned_students)} students")


if __name__ == "__main__":
    main()

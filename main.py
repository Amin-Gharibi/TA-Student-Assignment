from typing import List

# CONSTANTS
PRESENTATION_TIME: int = 30  # in minutes
TA_FILEPATH: str = './tas.txt'
STUDENTS_FILEPATH: str = './students.txt'
PREVIOUS_ASSIGNMENT_FILES: List[str] = ['./prev-hw1.txt']
FONT_FILEPATH: str = './Vazirmatn-Regular.ttf'


def main() -> None:
    from parsers import parse_student_file, parse_ta_file, parse_previous_assignments
    # Parse input files
    students = parse_student_file(STUDENTS_FILEPATH)
    tas, availability, ta_time_slots = parse_ta_file(TA_FILEPATH)
    from assignment_algo import balanced_assignment
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
        ta_time_slots,
        previous_assignments
    )

    # Print summary
    print("\nAssignment Summary:")
    for ta, assigned_students in assignments.items():
        print(f"{ta}: {len(assigned_students)} students")


if __name__ == "__main__":
    main()

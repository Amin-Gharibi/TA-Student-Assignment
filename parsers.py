from collections import defaultdict
from typing import Dict, List, Set, Tuple
from datetime import datetime



def parse_ta_file(filename: str) -> Tuple[List[str], Dict[str, int], Dict[str, datetime]]:
    """
    Reads TA information from a file and calculates available time in minutes.

    Args:
        filename: Path to the TA file

    Returns:
        Tuple containing:
        - List of TA names
        - Dictionary mapping TA names to available minutes
        - Dictionary mapping TA names to their start times
    """
    tas: List[str] = []
    availability: Dict[str, int] = {}
    ta_start_times: Dict[str, datetime] = {}  # Store TA start times for scheduling

    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) != 3:
                    continue

                ta_name, start_time, end_time = parts
                start_dt = datetime.strptime(start_time, "%H:%M")
                end_dt = datetime.strptime(end_time, "%H:%M")
                available_minutes = (end_dt - start_dt).seconds // 60

                tas.append(ta_name)
                availability[ta_name] = available_minutes
                ta_start_times[ta_name] = start_dt
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return [], {}, {}
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return [], {}, {}

    return tas, availability, ta_start_times

def parse_student_file(filename: str) -> List[str]:
    """
    Reads student names from a file.

    Args:
        filename: Path to the student file

    Returns:
        List of student names
    """
    students: List[str] = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                students.append(line.strip())
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

    return students

def parse_previous_assignments(filenames: List[str]) -> Dict[str, Set[str]]:
    """
    Parses previous assignment files to track which TA each student has already been assigned to.

    Args:
        filenames: List of paths to previous assignment files

    Returns:
        Dictionary mapping students to sets of TAs they've been assigned to before
    """
    previous_assignments: Dict[str, Set[str]] = defaultdict(set)

    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    if len(parts) >= 2:
                        student, ta = parts[0], parts[1]
                        previous_assignments[student].add(ta)
        except FileNotFoundError:
            print(f"Warning: Previous assignment file {filename} not found.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return previous_assignments

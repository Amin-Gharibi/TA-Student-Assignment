from collections import defaultdict
from typing import Dict, List, Set, Tuple
from datetime import datetime


def parse_ta_file(filename: str) -> Tuple[List[str], Dict[str, int], Dict[str, List[Tuple[datetime, datetime]]]]:
    """
    Reads TA information from a file and calculates available time in minutes.
    Each TA can have multiple time slots with dates.

    Args:
        filename: Path to the TA file

    Returns:
        Tuple containing:
        - List of TA names
        - Dictionary mapping TA names to available minutes
        - Dictionary mapping TA names to their list of tuples (date_time_start, date_time_end)
    """
    tas: List[str] = []
    availability: Dict[str, int] = {}
    ta_time_slots: Dict[str, List[Tuple[datetime, datetime]]] = defaultdict(list)

    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) != 4:  # TA name, date, start time, end time
                    print(
                        f"Warning: Invalid format in line: {line.strip()}. Expected: 'TA name, YYYY-MM-DD, HH:MM, HH:MM'")
                    continue

                ta_name, date_str, start_time, end_time = parts

                try:
                    # Parse the date and times
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    start_dt = datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")
                    end_dt = datetime.strptime(f"{date_str} {end_time}", "%Y-%m-%d %H:%M")

                    # Calculate available minutes for this slot
                    available_minutes = (end_dt - start_dt).seconds // 60

                    # Add TA to the list if not already added
                    if ta_name not in tas:
                        tas.append(ta_name)
                        availability[ta_name] = available_minutes
                    else:
                        # Add additional available minutes for existing TA
                        availability[ta_name] += available_minutes

                    # Add the time slot to the TA's schedule
                    ta_time_slots[ta_name].append((start_dt, end_dt))

                except ValueError as e:
                    print(f"Error parsing date/time in line: {line.strip()}. Error: {e}")
                    continue

    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return [], {}, defaultdict(list)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return [], {}, defaultdict(list)

    return tas, availability, ta_time_slots


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
from collections import defaultdict
from typing import List, Dict, Set
from datetime import datetime, timedelta
import random
from main import PRESENTATION_TIME
from util import create_excel_output


def balanced_assignment(
        students: List[str],
        tas: List[str],
        availability: Dict[str, int],
        ta_start_times: Dict[str, datetime],
        previous_assignments: Dict[str, Set[str]]
) -> Dict[str, List[str]]:
    """
    Assigns students to TAs while ensuring they are not assigned to the same TA as before.

    Args:
        students: List of student names
        tas: List of TA names
        availability: Dictionary mapping TA names to available minutes
        ta_start_times: Dictionary mapping TA names to their start times
        previous_assignments: Dictionary mapping students to sets of TAs they've been assigned to

    Returns:
        Dictionary mapping TAs to lists of assigned students
    """
    assignment: Dict[str, List[str]] = defaultdict(list)
    ta_load: Dict[str, int] = {ta: 0 for ta in tas}  # Keep track of assigned students
    ta_current_time: Dict[str, datetime] = ta_start_times.copy()  # Track the next available time for each TA

    # Prepare data for Excel export
    excel_data: List[Dict[str, str]] = []

    for student in students:
        # Find TAs that the student hasn't had before and who have enough time
        eligible_tas = [ta for ta in tas if
                        ta not in previous_assignments[student] and
                        availability[ta] >= PRESENTATION_TIME]  # Need at least PRESENTATION_TIME minutes

        if not eligible_tas:
            # Fallback to any TA with enough time
            eligible_tas = [ta for ta in tas if availability[ta] >= PRESENTATION_TIME]

        if not eligible_tas:
            print(f"Warning: No available TAs left for {student}")
            continue

        # Sort by load to balance assignments, and break ties randomly
        random.shuffle(eligible_tas)
        selected_ta = min(eligible_tas, key=lambda ta: ta_load[ta])

        # Assign student
        assignment[selected_ta].append(student)
        ta_load[selected_ta] += 1
        availability[selected_ta] -= PRESENTATION_TIME  # Reduce available time by PRESENTATION_TIME minutes per student

        # Calculate presentation time slots
        start_time = ta_current_time[selected_ta].strftime("%H:%M")
        ta_current_time[selected_ta] += timedelta(minutes=PRESENTATION_TIME)
        end_time = ta_current_time[selected_ta].strftime("%H:%M")

        # Add to Excel data
        excel_data.append({
            "Student": student,
            "TA": selected_ta,
            "Start Time": start_time,
            "End Time": end_time
        })

    # Create Excel file with multiple sheets
    create_excel_output(excel_data, assignment)

    return assignment

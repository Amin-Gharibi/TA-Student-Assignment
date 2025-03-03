from collections import defaultdict
from typing import List, Dict, Set, Tuple
from datetime import datetime, timedelta
import random
from main import PRESENTATION_TIME
from util import create_excel_output


def balanced_assignment(
        students: List[str],
        tas: List[str],
        availability: Dict[str, int],
        ta_time_slots: Dict[str, List[Tuple[datetime, datetime]]],
        previous_assignments: Dict[str, Set[str]]
) -> Dict[str, List[str]]:
    """
    Assigns students to TAs while ensuring they are not assigned to the same TA as before.

    Args:
        students: List of student names
        tas: List of TA names
        availability: Dictionary mapping TA names to available minutes
        ta_time_slots: Dictionary mapping TA names to their list of date-time slots (start, end)
        previous_assignments: Dictionary mapping students to sets of TAs they've been assigned to

    Returns:
        Dictionary mapping TAs to lists of assigned students
    """
    assignment: Dict[str, List[str]] = defaultdict(list)
    ta_load: Dict[str, int] = {ta: 0 for ta in tas}  # Keep track of assigned students

    # Track the current slot and position within each TA's time slots
    ta_current_slot: Dict[str, int] = {ta: 0 for ta in tas}  # Current time slot index
    ta_current_position: Dict[str, datetime] = {}  # Current position within the slot

    # Initialize starting positions for each TA's first time slot
    for ta in tas:
        if ta_time_slots[ta]:
            ta_current_position[ta] = ta_time_slots[ta][0][0]  # Start time of first slot

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
        availability[selected_ta] -= PRESENTATION_TIME  # Reduce available time by PRESENTATION_TIME minutes

        # Get the current slot and start time
        current_slot_index = ta_current_slot[selected_ta]
        current_slot = ta_time_slots[selected_ta][current_slot_index]
        current_slot_start, current_slot_end = current_slot

        # Get the current time position within the slot
        current_position = ta_current_position[selected_ta]

        # Extract the date and start time
        date_str = current_position.strftime("%Y-%m-%d")
        start_time = current_position.strftime("%H:%M")

        # Update the current position for the TA
        ta_current_position[selected_ta] += timedelta(minutes=PRESENTATION_TIME)

        # Check if we've exceeded the current time slot's end time
        # If yes, move to the next time slot
        if ta_current_position[selected_ta] > current_slot_end and current_slot_index + 1 < len(
                ta_time_slots[selected_ta]):
            # Move to next time slot
            ta_current_slot[selected_ta] += 1
            current_slot_index = ta_current_slot[selected_ta]
            ta_current_position[selected_ta] = ta_time_slots[selected_ta][current_slot_index][0]

        # Add to Excel data - include date and start time (no end time)
        excel_data.append({
            "Student": student,
            "TA": selected_ta,
            "Date": date_str,
            "Start Time": start_time
        })

    # Create Excel file with multiple sheets
    create_excel_output(excel_data, assignment)

    return assignment

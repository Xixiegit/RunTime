import datetime
import os
import json
import time

print("COlection started ")

# Function to get the active window title
def get_active_window_title():
    active_window = None
    try:
        import win32gui
        active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except ImportError:
        pass
    return active_window

# Function to create or update sorted_user_data.json
def update_sorted_user_data(file_name, today, sorted_data):
    year = today.year
    month = today.strftime("%B")
    day = today.day

    if year not in sorted_data:
        sorted_data[year] = {"months": {}}

    if month not in sorted_data[year]["months"]:
        sorted_data[year]["months"][month] = {"days": {}}

    if day not in sorted_data[year]["months"][month]["days"]:
        sorted_data[year]["months"][month]["days"][day] = []

    # Write sorted_data to the specified file
    with open(file_name, 'w') as sorted_file:
        json.dump(sorted_data, sorted_file, indent=2)

# Function to track program usage and write to file
def track_program_usage(file_name, sorted_data):
    active_app = None
    segment_start_time = None
    last_update_time = datetime.datetime.now()  # Initialize last update time
    while True:
        current_time = datetime.datetime.now()
        if (current_time - last_update_time).seconds >= 1:  # Update file every minute
            last_update_time = current_time

            # Update sorted_user_data.json
            update_sorted_user_data(file_name, last_update_time, sorted_data)

        today = datetime.datetime.now()
        current_app = get_active_window_title()
        if active_app != current_app:
            # If the activity changes, update the duration of the previous segment
            if active_app is not None and segment_start_time is not None:
                end_time = datetime.datetime.now()
                duration = (end_time - segment_start_time).total_seconds()
                log_entry = {
                    "start_time": segment_start_time.strftime("%H:%M:%S"),
                    "end_time": end_time.strftime("%H:%M:%S"),
                    "program": active_app,
                    "duration": round(duration)
                }
                update_sorted_user_data(file_name, segment_start_time, sorted_data)
                sorted_data[segment_start_time.year]["months"][segment_start_time.strftime("%B")]["days"][segment_start_time.day].append(log_entry)

            # Update the active app and start a new segment
            active_app = current_app
            segment_start_time = datetime.datetime.now()

        else:
            # Update the duration of the current segment while the activity remains the same
            if segment_start_time is not None:
                end_time = datetime.datetime.now()
                duration = (end_time - segment_start_time).total_seconds()
                # Update the duration of the current segment
                if active_app is not None:
                    log_entry = {
                        "start_time": segment_start_time.strftime("%H:%M:%S"),
                        "end_time": end_time.strftime("%H:%M:%S"),
                        "program": active_app,
                        "duration": round(duration)
                    }
                    update_sorted_user_data(file_name, segment_start_time, sorted_data)
                    sorted_data[segment_start_time.year]["months"][segment_start_time.strftime("%B")]["days"][segment_start_time.day].append(log_entry)

        time.sleep(1)  # Add a short delay to reduce CPU usage

# Initialize sorted data
sorted_data = {}

# Specify the file name
file_name = "sorted_user_data.json"

# Start tracking program usage
track_program_usage(file_name, sorted_data)

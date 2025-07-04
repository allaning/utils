# This script converts a Google Calendar exported as an .ics file into a
# human readable format.

import icalendar
import pytz
from datetime import datetime, date
import sys

def parse_ics_to_human_readable(ics_file_path, output_file_path=None):
    """
    Parses an .ics file, sorts events by date/time, and extracts data
    into a human-readable text format.

    Args:
        ics_file_path (str): The path to the .ics file.
        output_file_path (str, optional): The path to the output text file.
                                          If None, prints to console.
    """
    try:
        with open(ics_file_path, 'rb') as f:
            gcal = icalendar.Calendar.from_ical(f.read())
    except FileNotFoundError:
        print(f"Error: The file '{ics_file_path}' was not found.")
        return
    except Exception as e:
        print(f"Error reading or parsing ICS file: {e}")
        return

    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary_prop = component.get('summary')
            start_prop = component.get('dtstart')
            end_prop = component.get('dtend')
            description_prop = component.get('description')
            location_prop = component.get('location')
            uid_prop = component.get('uid')

            # Extract the actual value, handling different types
            summary = str(summary_prop) if summary_prop else 'No Title'
            description = str(description_prop) if description_prop else ''
            location = str(location_prop) if location_prop else ''
            uid = str(uid_prop) if uid_prop else 'No UID'

            # Get the raw datetime/date object for sorting
            sort_key_dt = None
            if start_prop:
                dt_obj = start_prop.dt
                if isinstance(dt_obj, datetime):
                    sort_key_dt = dt_obj
                elif isinstance(dt_obj, date):
                    # For all-day events (date objects), create a datetime at midnight for sorting
                    sort_key_dt = datetime(dt_obj.year, dt_obj.month, dt_obj.day, 0, 0, 0)
                    # Optional: If you want to localize all-day events to a specific timezone for sorting
                    # from pytz import timezone
                    # local_tz = timezone('America/New_York') # Or your desired timezone
                    # sort_key_dt = local_tz.localize(sort_key_dt)


            events.append({
                'sort_key': sort_key_dt, # This will be used for sorting
                'summary': summary.strip(),
                'start_prop': start_prop, # Keep original prop to format later
                'end_prop': end_prop,     # Keep original prop to format later
                'description': ' '.join(description.split()), # Cleaned description
                'location': location.strip(),
                'uid': uid.strip()
            })

    # Sort events by their 'sort_key' (start date/time)
    # Events without a start date will be at the beginning if sort_key is None
    # We can filter them out or handle them specifically if needed
    events.sort(key=lambda x: x['sort_key'] if x['sort_key'] is not None else datetime.min)

    output_lines = []
    output_lines.append(f"--- Calendar Events from: {ics_file_path} (Sorted by Date/Time) ---")
    output_lines.append("")

    event_count = 0
    for event in events:
        event_count += 1
        #output_lines.append(f"Event {event_count}:")
        output_lines.append(f"  Title: {event['summary']}")

        # Re-process start and end properties for formatting
        start_prop = event['start_prop']
        end_prop = event['end_prop']

        if start_prop:
            dt_start = start_prop.dt
            if isinstance(dt_start, datetime):
                if dt_start.tzinfo is None or dt_start.utcoffset() is None:
                    output_lines.append(f"  Start: {dt_start.strftime('%Y-%m-%d %H:%M:%S')} (Local Time/No TZ info)")
                else:
                    output_lines.append(f"  Start: {dt_start.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            else: # It's a date object (all-day event)
                output_lines.append(f"  Start: {dt_start.strftime('%Y-%m-%d')} (All Day Event)")

        if end_prop:
            dt_end = end_prop.dt
            if isinstance(dt_end, datetime):
                if dt_end.tzinfo is None or dt_end.utcoffset() is None:
                    output_lines.append(f"  End: {dt_end.strftime('%Y-%m-%d %H:%M:%S')} (Local Time/No TZ info)")
                else:
                    output_lines.append(f"  End: {dt_end.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            else: # It's a date object (all-day event)
                output_lines.append(f"  End: {dt_end.strftime('%Y-%m-%d')} (All Day Event)")


        if event['location']:
            output_lines.append(f"  Location: {event['location']}")
        if event['description']:
            output_lines.append(f"  Description: {event['description']}")

        #output_lines.append(f"  UID: {event['uid']}")
        output_lines.append("-" * 40) # Separator for events

    output_lines.append(f"\n--- End of Calendar Events ---")

    output_content = "\n".join(output_lines)

    if output_file_path:
        try:
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(output_content)
            print(f"Successfully extracted events to: {output_file_path}")
        except Exception as e:
            print(f"Error writing to output file '{output_file_path}': {e}")
    else:
        print(output_content)

# --- How to use the script ---
if __name__ == "__main__":
    # sys.argv is a list of command-line arguments.
    # sys.argv[0] is the script name itself.
    # sys.argv[1] would be the first argument provided by the user.
    if len(sys.argv) < 2:
        print("Usage: python your_script_name.py <path_to_ics_file> [output_file.txt]")
        print("Example: python ics_parser.py my_calendar.ics")
        print("Example: python ics_parser.py /path/to/my_calendar.ics output.txt")
        sys.exit(1) # Exit with an error code

    ics_file_to_parse = sys.argv[1]
    output_text_file = None

    if len(sys.argv) >= 3:
        output_text_file = sys.argv[2]

    print(f"--- Parsing and processing '{ics_file_to_parse}' ---")
    parse_ics_to_human_readable(ics_file_to_parse, output_text_file)


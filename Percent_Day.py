"""
Percent of Day Calculator
CLI with a clearer layout, quick tips, and a visual day progress bar.
"""

from datetime import datetime
from typing import Tuple


MINUTES_IN_DAY = 24 * 60
LINE_WIDTH = 64


try:
    # Use color when available; otherwise fall back to plain text.
    from colorama import Fore, Style, init as colorama_init

    colorama_init(autoreset=True)
    COLOR_ENABLED = True
except Exception:
    COLOR_ENABLED = False


def colorize(text: str, color: str) -> str:
    if not COLOR_ENABLED:
        return text
    return f"{color}{text}{Style.RESET_ALL}"


def divider(char: str = "-", width: int = LINE_WIDTH) -> str:
    return char * width


def parse_time(time_str: str) -> Tuple[int, int]:
    """
    Parse and validate an HH:MM time string.
    """
    parts = time_str.split(":")
    if len(parts) != 2:
        raise ValueError("Time must be in HH:MM format")

    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        raise ValueError("Hours and minutes must be numbers")

    if hours < 0 or hours >= 24:
        raise ValueError("Hours must be between 00 and 23")
    if minutes < 0 or minutes >= 60:
        raise ValueError("Minutes must be between 00 and 59")

    return hours, minutes


def calculate_day_state(time_str: str) -> dict:
    """
    Return a dictionary with the parsed time and day progress metrics.
    """
    hours, minutes = parse_time(time_str)
    minutes_passed = hours * 60 + minutes
    percentage = (minutes_passed / MINUTES_IN_DAY) * 100
    minutes_remaining = MINUTES_IN_DAY - minutes_passed

    return {
        "hours": hours,
        "minutes": minutes,
        "minutes_passed": minutes_passed,
        "minutes_remaining": minutes_remaining,
        "percentage": percentage,
    }


def calculate_day_percentage(time_str: str) -> float:
    """
    Public API retained for compatibility; returns only the percentage.
    """
    return calculate_day_state(time_str)["percentage"]


def progress_bar(percentage: float, width: int = 36) -> str:
    """
    Render a simple progress bar showing how much of the day has passed.
    """
    clamped = max(0.0, min(percentage, 100.0))
    filled = int(round((clamped / 100) * width))
    return f"[{'#' * filled}{'.' * (width - filled)}] {clamped:6.2f}%"


def format_minutes_as_time(minutes: int) -> str:
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m"


def print_header() -> None:
    print(divider("="))
    print(" Percent of Day Calculator ".center(LINE_WIDTH, " "))
    print(divider("="))
    print("Enter a time in 24-hour HH:MM. Leave blank for current time.")
    print("Type 'q' or 'quit' to exit.")
    print(divider("-"))
    print("Examples: 07:15   14:30   23:59")
    print(divider("-"))


def print_result(state: dict, used_current_time: bool) -> None:
    print()
    label = "Now" if used_current_time else f"{state['hours']:02d}:{state['minutes']:02d}"
    header = colorize(f" Result for {label} ", Fore.CYAN if COLOR_ENABLED else "")
    print(header)
    print(divider())
    print(progress_bar(state["percentage"]))
    print(f"Passed     : {format_minutes_as_time(state['minutes_passed'])}")
    print(f"Remaining  : {format_minutes_as_time(state['minutes_remaining'])}")
    print(f"Minutes    : {state['minutes_passed']} passed | {state['minutes_remaining']} left")
    print(divider())
    print()


def main():
    print_header()

    while True:
        try:
            raw = input("Time (HH:MM | blank for now | q to quit): ").strip()
            if raw.lower() in {"q", "quit", "exit"}:
                break

            used_current_time = False
            if raw == "" or raw.lower() == "now":
                now = datetime.now()
                raw = f"{now.hour:02d}:{now.minute:02d}"
                used_current_time = True

            state = calculate_day_state(raw)
            print_result(state, used_current_time)

            continue_choice = input("Calculate another time? (y/n): ").strip().lower()
            if continue_choice not in {"y", "yes"}:
                break
            print()

        except ValueError as e:
            print(colorize(f"Error: {e}", Fore.RED if COLOR_ENABLED else ""))
            print("Please try again.\n")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(colorize(f"Unexpected error: {e}", Fore.RED if COLOR_ENABLED else ""))
            print("Please try again.\n")

    print("Thank you for using Percent of Day Calculator!")


if __name__ == "__main__":
    main()


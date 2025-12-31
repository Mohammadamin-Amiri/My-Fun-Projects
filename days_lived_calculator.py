from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATE_FORMATS = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']
MOTIVATION = "You still have wonderfull days to experience... and also some shitty days, let's be realistic"


def parse_date(date_str: str) -> datetime:
    """Parse a date string using accepted formats."""
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError("Invalid date format")


def get_date_input(prompt):
    """Retain CLI helper (unused in GUI) for compatibility."""
    while True:
        try:
            date_str = input(prompt)
            return parse_date(date_str)
        except ValueError:
            print()
            print("  Invalid date format. Please try again.")
            print("  Accepted formats: YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY")
            print()


def calculate_days_lived(birth_date, current_date):
    """Calculate the number of days between birth date and current date."""
    if current_date < birth_date:
        raise ValueError("Current date cannot be before birth date!")

    delta = current_date - birth_date
    return delta.days


def main():
    root = tk.Tk()
    root.title("Days Lived Calculator")
    root.resizable(False, False)

    # Color palette and typography
    BG = "#0f172a"          # Deep navy background
    CARD_BG = "#111827"     # Slightly lighter card background
    PANEL_BG = "#1f2937"    # Panel background
    ACCENT = "#38bdf8"      # Light blue accent
    ACCENT_ALT = "#a855f7"  # Purple accent
    TEXT_PRIMARY = "#e5e7eb"  # Light text
    TEXT_SECONDARY = "#cbd5e1"

    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD_BG)
    style.configure("Panel.TFrame", background=PANEL_BG)
    style.configure("Heading.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY, font=("Segoe UI", 16, "bold"))
    style.configure("Subheading.TLabel", background=CARD_BG, foreground=TEXT_SECONDARY, font=("Segoe UI", 10))
    style.configure("Section.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY, font=("Segoe UI", 11, "bold"))
    style.configure("Body.TLabel", background=CARD_BG, foreground=TEXT_PRIMARY, font=("Segoe UI", 10))
    style.configure("Muted.TLabel", background=CARD_BG, foreground=TEXT_SECONDARY, font=("Segoe UI", 9))
    style.configure("Accent.TLabel", background=PANEL_BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))
    style.configure("AccentBody.TLabel", background=PANEL_BG, foreground=TEXT_PRIMARY, font=("Segoe UI", 10))
    style.configure("TSeparator", background=ACCENT)
    style.configure("TEntry", fieldbackground="#0b1220", foreground=TEXT_PRIMARY, insertcolor=TEXT_PRIMARY)
    style.map("Accent.TButton", background=[("!disabled", ACCENT), ("pressed", ACCENT_ALT)], foreground=[("disabled", "#6b7280"), ("!disabled", BG)])
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 6), borderwidth=0)
    style.configure("Results.TLabelframe", background=PANEL_BG, foreground=TEXT_PRIMARY, borderwidth=0)
    style.configure("Results.TLabelframe.Label", background=PANEL_BG, foreground=ACCENT, font=("Segoe UI", 11, "bold"))

    main_frame = ttk.Frame(root, style="TFrame", padding="18 18 18 18")
    main_frame.grid(row=0, column=0, sticky="nsew")

    card = ttk.Frame(main_frame, style="Card.TFrame", padding="18 18 18 18")
    card.grid(row=0, column=0, sticky="nsew")

    ttk.Label(card, text="Days Lived Calculator", style="Heading.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
    ttk.Label(
        card,
        text="Enter your birth date and today's date to see how many days you've lived.",
        style="Subheading.TLabel",
    ).grid(row=1, column=0, columnspan=2, pady=(6, 12), sticky="w")

    ttk.Separator(card).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

    ttk.Label(card, text="Enter Your Dates", style="Section.TLabel").grid(row=3, column=0, columnspan=2, sticky="w")
    ttk.Label(
        card,
        text="Accepted formats: YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY",
        style="Muted.TLabel",
    ).grid(row=4, column=0, columnspan=2, pady=(2, 12), sticky="w")

    ttk.Label(card, text="Birth date", style="Body.TLabel").grid(row=5, column=0, sticky="e", padx=(0, 10))
    birth_var = tk.StringVar()
    birth_entry = ttk.Entry(card, textvariable=birth_var, width=26, justify="left")
    birth_entry.grid(row=5, column=1, sticky="w")

    ttk.Label(card, text="Current date", style="Body.TLabel").grid(row=6, column=0, sticky="e", padx=(0, 10), pady=(8, 0))
    current_var = tk.StringVar()
    current_entry = ttk.Entry(card, textvariable=current_var, width=26, justify="left")
    current_entry.grid(row=6, column=1, sticky="w", pady=(8, 0))

    ttk.Separator(card).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(14, 12))

    result_frame = ttk.LabelFrame(card, text="Results", style="Results.TLabelframe", padding="14 12 14 12")
    result_frame.grid(row=8, column=0, columnspan=2, sticky="ew")

    result_var = tk.StringVar(value="You have lived for: --")
    detail_var = tk.StringVar(value="Today is day number -- in your life.")
    message_var = tk.StringVar(value="")

    ttk.Label(result_frame, textvariable=result_var, style="Accent.TLabel").grid(row=0, column=0, sticky="w")
    ttk.Label(result_frame, textvariable=detail_var, style="AccentBody.TLabel").grid(row=1, column=0, sticky="w", pady=(6, 4))
    ttk.Label(result_frame, textvariable=message_var, style="AccentBody.TLabel", wraplength=320, justify="left").grid(row=2, column=0, sticky="w")

    def calculate():
        birth_input = birth_var.get().strip()
        current_input = current_var.get().strip()

        if not birth_input or not current_input:
            messagebox.showerror("Missing information", "Please enter both dates to continue.")
            return

        try:
            birth_date = parse_date(birth_input)
            current_date = parse_date(current_input)
            days_lived = calculate_days_lived(birth_date, current_date)
        except ValueError as exc:
            messagebox.showerror("Invalid date", str(exc))
            return

        result_var.set(f"You have lived for: {days_lived:,} days")
        detail_var.set(f"Today is day number {days_lived:,} in your life.")
        message_var.set(MOTIVATION)

    calculate_btn = ttk.Button(card, text="Calculate", style="Accent.TButton", command=calculate)
    calculate_btn.grid(row=9, column=0, columnspan=2, pady=(14, 0), ipadx=10)

    birth_entry.focus()
    root.mainloop()


if __name__ == "__main__":
    main()

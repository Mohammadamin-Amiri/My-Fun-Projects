import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

# Visual constants
WINDOW_BG = "#0e1117"
CARD_BG = "#161b22"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#9da9b7"
ACCENT = "#58a6ff"
ERROR = "#ff7b72"
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10)
FONT_VALUE = ("Segoe UI", 11, "bold")


def calculate_year_percentage(date_str):
    """Parse a date string and return percentage, day of year, days in year, and year."""
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
    date_obj = None

    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue

    if date_obj is None:
        raise ValueError(
            "Unable to read that date. Try formats like 2025-03-15 or 15-03-2025."
        )

    day_of_year = date_obj.timetuple().tm_yday

    year = date_obj.year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_year = 366
    else:
        days_in_year = 365

    percentage = (day_of_year / days_in_year) * 100
    return percentage, day_of_year, days_in_year, year


class PercentYearApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Percent of Year")
        self.configure(bg=WINDOW_BG)
        self.geometry("520x360")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        container = tk.Frame(self, bg=WINDOW_BG, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        card = tk.Frame(
            container,
            bg=CARD_BG,
            bd=0,
            highlightthickness=1,
            highlightbackground="#1f2933",
            relief="ridge",
        )
        card.pack(fill="both", expand=True, pady=(0, 6))

        # Header
        header = tk.Frame(card, bg=CARD_BG, padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="Percent of Year", bg=CARD_BG, fg=TEXT_PRIMARY, font=FONT_TITLE).pack(anchor="w")
        tk.Label(
            header,
            text="See how far through the year a date is.",
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=FONT_SUBTITLE,
        ).pack(anchor="w", pady=(4, 0))

        # Input area
        input_area = tk.Frame(card, bg=CARD_BG, padx=18, pady=10)
        input_area.pack(fill="x")
        tk.Label(
            input_area,
            text="Date (YYYY-MM-DD, DD-MM-YYYY, or MM/DD/YYYY)",
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=FONT_LABEL,
        ).pack(anchor="w")

        self.date_var = tk.StringVar()
        entry = tk.Entry(
            input_area,
            textvariable=self.date_var,
            bg="#0b0f14",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            font=FONT_VALUE,
            width=32,
        )
        entry.pack(anchor="w", pady=(6, 2))
        entry.bind("<Return>", lambda _: self.calculate())

        btn = tk.Button(
            input_area,
            text="Calculate",
            command=self.calculate,
            bg=ACCENT,
            fg="#0b0f14",
            activebackground="#7db7ff",
            activeforeground="#0b0f14",
            relief="flat",
            padx=14,
            pady=6,
            font=FONT_VALUE,
        )
        btn.pack(anchor="w", pady=(10, 0))

        # Results card section
        results = tk.Frame(card, bg=CARD_BG, padx=18, pady=14)
        results.pack(fill="both", expand=True)

        self.progress_label = tk.Label(
            results, text="", bg=CARD_BG, fg=TEXT_PRIMARY, font=FONT_VALUE
        )
        self.progress_label.pack(anchor="w", pady=(4, 4))

        self.progress = ttk.Progressbar(
            results,
            orient="horizontal",
            mode="determinate",
            length=400,
            maximum=100,
        )
        self.progress.pack(anchor="w", pady=(2, 10))

        # Configure custom style for progress bar
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#0b0f14",
            background=ACCENT,
            bordercolor="#0b0f14",
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )
        self.progress.configure(style="Custom.Horizontal.TProgressbar")

        # Info lines
        self.year_info = tk.Label(results, text="", bg=CARD_BG, fg=TEXT_SECONDARY, font=FONT_LABEL, justify="left")
        self.year_info.pack(anchor="w", pady=(6, 0))

        # Footer hint
        footer = tk.Label(
            self,
            text="Tip: Hit Enter to calculate quickly.",
            bg=WINDOW_BG,
            fg="#6b7685",
            font=("Segoe UI", 9),
        )
        footer.pack(pady=(2, 0))

    def calculate(self):
        date_input = self.date_var.get().strip()
        if not date_input:
            messagebox.showerror("Missing date", "Please enter a date first.")
            return

        try:
            percentage, day_of_year, days_in_year, year = calculate_year_percentage(
                date_input
            )
        except ValueError as err:
            messagebox.showerror("Invalid date", str(err))
            return
        except Exception as err:
            messagebox.showerror("Unexpected error", str(err))
            return

        self.progress["value"] = percentage
        self.progress_label.config(text=f"{percentage:0.2f}% of {year} complete")

        leap = "Yes" if days_in_year == 366 else "No"
        self.year_info.config(
            text=(
                f"Year: {year}\n"
                f"Day: {day_of_year} of {days_in_year}\n"
                f"Leap Year: {leap}"
            )
        )


if __name__ == "__main__":
    app = PercentYearApp()
    app.mainloop()

import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Track expression and result strings
        self.expression = ""
        self.expression_var = tk.StringVar(value="0")
        self.result_var = tk.StringVar(value="0")

        self.create_display()
        self.create_buttons()

    def create_display(self):
        """Create the stacked expression/result display."""
        display_frame = ttk.Frame(self.root, padding=(14, 16))
        display_frame.grid(row=0, column=0, sticky="ew")
        display_frame.columnconfigure(0, weight=1)

        expression_label = ttk.Label(
            display_frame,
            textvariable=self.expression_var,
            style="Expression.TLabel",
            anchor="e",
        )
        expression_label.grid(row=0, column=0, sticky="ew")

        result_label = ttk.Label(
            display_frame,
            textvariable=self.result_var,
            style="Result.TLabel",
            anchor="e",
        )
        result_label.grid(row=1, column=0, sticky="ew", pady=(6, 0))

    def create_buttons(self):
        """Create calculator buttons."""
        button_frame = ttk.Frame(self.root, padding=(14, 14))
        button_frame.grid(row=1, column=0, sticky="nsew")
        button_frame.columnconfigure(tuple(range(4)), weight=1)
        button_frame.rowconfigure(tuple(range(5)), weight=1)

        buttons = [
            ['C', 'DEL', '/', '*'],
            ['7', '8', '9', '-'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '='],
            ['0', '.', '(', ')'],
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text in ['/', '*', '-', '+']:
                    style = 'Operator.TButton'
                elif text == '=':
                    style = 'Accent.TButton'
                elif text in ['C', 'DEL']:
                    style = 'Clear.TButton'
                else:
                    style = 'TButton'

                btn = ttk.Button(
                    button_frame,
                    text=text,
                    width=8,
                    style=style,
                    command=lambda t=text: self.button_click(t),
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    def button_click(self, char):
        """Handle button clicks."""
        if char == 'C':
            self.expression = ""
            self.refresh_display("0")
        elif char == 'DEL':
            if self.expression:
                self.expression = self.expression[:-1]
                self.refresh_display()
        elif char == '=':
            try:
                result = eval(self.expression)
                self.expression = str(result)
                self.refresh_display(str(result))
            except Exception:
                self.result_var.set("Error")
                self.expression = ""
                self.expression_var.set("0")
        else:
            if self.result_var.get() == "0" and char not in ['+', '-', '*', '/', '(', ')']:
                self.expression = char
            else:
                self.expression += char
            self.refresh_display()

    def refresh_display(self, result_override=None):
        """Update both expression and result readouts."""
        self.expression_var.set(self.expression if self.expression else "0")
        if result_override is not None:
            self.result_var.set(result_override)
        else:
            self.result_var.set(self.expression if self.expression else "0")

def main():
    root = tk.Tk()

    # Configure styles for different button types
    style = ttk.Style()
    style.theme_use('clam')
    background = "#111827"
    surface = "#1f2937"
    surface_lift = "#374151"
    accent = "#10b981"
    operator = "#06b6d4"
    warning = "#fbbf24"

    root.configure(bg=background)
    style.configure('TFrame', background=background)

    style.configure('Expression.TLabel', background=background,
                    foreground="#9ca3af", font=('Segoe UI', 12))
    style.configure('Result.TLabel', background=background,
                    foreground="#f9fafb", font=('Segoe UI', 28, 'bold'))
    style.configure('TButton', font=('Segoe UI', 14), padding=10,
                    background=surface, foreground="#f9fafb", borderwidth=0)
    style.map('TButton', background=[('active', surface_lift)],
              relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
    style.configure('Operator.TButton', background=surface, foreground=operator)
    style.map('Operator.TButton', background=[('active', "#0ea5e9")],
              foreground=[('active', "#f9fafb")])
    style.configure('Accent.TButton', background=accent, foreground="#ffffff")
    style.map('Accent.TButton', background=[('active', "#0d9e6f")])
    style.configure('Clear.TButton', background=surface, foreground=warning)
    style.map('Clear.TButton', background=[('active', surface_lift)],
              foreground=[('active', "#f9fafb")])

    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

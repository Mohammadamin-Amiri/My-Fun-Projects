import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Main container to give the UI breathing room
        self.container = ttk.Frame(self.root, style="Main.TFrame", padding=(18, 20))
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)

        # Track expression and result strings
        self.expression = ""
        self.expression_var = tk.StringVar(value="0")
        self.result_var = tk.StringVar(value="0")

        self.create_display()
        self.create_buttons()

    def create_display(self):
        """Create the stacked expression/result display."""
        display_frame = ttk.Frame(self.container, style="Display.TFrame", padding=(16, 18))
        display_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        display_frame.columnconfigure(0, weight=1)

        title = ttk.Label(
            display_frame,
            text="Aurora Calc",
            style="Title.TLabel",
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        expression_label = ttk.Label(
            display_frame,
            textvariable=self.expression_var,
            style="Expression.TLabel",
            anchor="e",
        )
        expression_label.grid(row=1, column=0, sticky="ew", pady=(10, 2))

        result_label = ttk.Label(
            display_frame,
            textvariable=self.result_var,
            style="Result.TLabel",
            anchor="e",
        )
        result_label.grid(row=2, column=0, sticky="ew")

    def create_buttons(self):
        """Create calculator buttons."""
        button_frame = ttk.Frame(self.container, style="ButtonArea.TFrame", padding=(10, 12))
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
                    style = 'Keypad.TButton'

                btn = ttk.Button(
                    button_frame,
                    text=text,
                    style=style,
                    command=lambda t=text: self.button_click(t),
                )
                btn.grid(row=i, column=j, padx=4, pady=4, sticky=(tk.W, tk.E, tk.N, tk.S))

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
    palette = {
        "background": "#050915",
        "card": "#0f172a",
        "raised": "#1a2335",
        "hover": "#1f2b3f",
        "text": "#e2e8f0",
        "muted": "#94a3b8",
        "accent": "#f97316",
        "accent_hover": "#ea580c",
        "operator": "#22d3ee",
        "operator_active": "#67e8f9",
        "warning": "#fbbf24",
    }

    root.configure(bg=palette["background"], padx=10, pady=10)
    style.configure('TFrame', background=palette["background"])

    style.configure('Main.TFrame', background=palette["card"])
    style.configure('Display.TFrame', background=palette["card"])
    style.configure('ButtonArea.TFrame', background=palette["card"])

    style.configure('Title.TLabel', background=palette["card"],
                    foreground=palette["muted"], font=('Segoe UI Semibold', 11))
    style.configure('Expression.TLabel', background=palette["card"],
                    foreground=palette["muted"], font=('Segoe UI', 12))
    style.configure('Result.TLabel', background=palette["card"],
                    foreground=palette["text"], font=('Segoe UI Semibold', 30))

    base_padding = (12, 14)
    style.configure('Keypad.TButton', font=('Segoe UI Semibold', 14), padding=base_padding,
                    background=palette["raised"], foreground=palette["text"],
                    borderwidth=0, relief='flat')
    style.map('Keypad.TButton',
              background=[('active', palette["hover"]), ('pressed', palette["hover"])],
              foreground=[('disabled', "#475569")])

    style.configure('Operator.TButton', font=('Segoe UI Semibold', 14), padding=base_padding,
                    background=palette["raised"], foreground=palette["operator"],
                    borderwidth=0, relief='flat')
    style.map('Operator.TButton',
              background=[('active', palette["operator"]), ('pressed', palette["operator"])],
              foreground=[('active', palette["card"])])

    style.configure('Accent.TButton', font=('Segoe UI Semibold', 14), padding=base_padding,
                    background=palette["accent"], foreground=palette["card"],
                    borderwidth=0, relief='flat')
    style.map('Accent.TButton',
              background=[('active', palette["accent_hover"]), ('pressed', palette["accent_hover"])],
              foreground=[('active', palette["card"])])

    style.configure('Clear.TButton', font=('Segoe UI Semibold', 14), padding=base_padding,
                    background=palette["raised"], foreground=palette["warning"],
                    borderwidth=0, relief='flat')
    style.map('Clear.TButton',
              background=[('active', palette["hover"]), ('pressed', palette["hover"])],
              foreground=[('active', palette["card"])])

    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

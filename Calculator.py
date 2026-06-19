import tkinter as tk

class Calculator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("350x450")
        self.root.resizable(True, True)

        # State variables
        self.result_shown = False

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        #Create and arrange all UI components
        #  Display Frame 
        display_frame = tk.Frame(self.root, bg="black", height=80)
        display_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        display_frame.pack_propagate(False)

        self.display_var = tk.StringVar()
        self.display_var.set("0")

        self.entry = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24),
            bg="black",
            fg="white",
            justify="right",
            insertbackground="white"
        )
        self.entry.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.entry.focus_set()

        # Keyboard bindings
        self.entry.bind("<Return>", self.calculate)
        self.entry.bind("<KeyPress-c>", self.clear_all)
        self.entry.bind("<KeyPress-C>", self.clear_all)
        self.entry.bind("<BackSpace>", self.backspace)
        self.entry.bind("<Key>", self.on_key_press)

        #  Buttons Frame 
        button_frame = tk.Frame(self.root, bg="lightgray")
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button layout 
        buttons_layout = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+']
        ]

        # Configure grid weights for resizing
        for col in range(4):
            button_frame.grid_columnconfigure(col, weight=1)
        for row in range(len(buttons_layout)):
            button_frame.grid_rowconfigure(row, weight=1)

        # Create buttons dynamically
        for row_idx, row in enumerate(buttons_layout):
            for col_idx, text in enumerate(row):
                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=("Arial", 16),
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

    # Event Handlers 

    def button_click(self, char: str):
        #Handle button clicks and key presses for digits and operators
        current = self.display_var.get()

        # Special buttons
        if char == 'C':
            self.clear_all()
            return
        if char == '=':
            self.calculate()
            return

        # Reset display if a result was shown
        if self.result_shown:
            if char.isdigit() or char == '.':
                self.display_var.set(char)
                self.result_shown = False
                return
            else:
                self.result_shown = False

        # Prevent invalid starting characters
        if not current or current == '0':
            if char in '*/':
                return
            if char in '+-' and current == '0':
                self.display_var.set(char)
                return
            if char.isdigit():
                self.display_var.set(char)
                return

        # Prevent consecutive operators
        if char in '+-*/' and current[-1] in '+-*/':
            self.display_var.set(current[:-1] + char)
            return

        # Prevent multiple dots in the same number
        if char == '.':
            parts = current.split()
            if parts:
                last_num = parts[-1]
                if '.' in last_num:
                    return

        # Append character
        self.display_var.set(current + char)

    def calculate(self, event=None):
        #Evaluate the mathematical expression and display the result
        expr = self.display_var.get().strip()

        if not expr or expr in '+-*/':
            return "break"

        # Replace display symbols with Python operators
        expr = expr.replace('×', '*').replace('÷', '/')

        # Validate allowed characters
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expr):
            self.display_var.set("Error")
            self.result_shown = True
            return "break"

        try:
            result = eval(expr)
            # Clean up floating point results
            if isinstance(result, float):
                result = round(result, 10)
                if result.is_integer():
                    result = int(result)
            self.display_var.set(str(result))
            self.result_shown = True
        except ZeroDivisionError:
            self.display_var.set("Division by zero")
            self.result_shown = True
        except SyntaxError:
            self.display_var.set("Invalid expression")
            self.result_shown = True
        except Exception:
            self.display_var.set("Error")
            self.result_shown = True

        return "break"

    def clear_all(self, event=None):
        #Reset the display to zero
        self.display_var.set("0")
        self.result_shown = False
        return "break"

    def backspace(self, event=None):
        #Remove the last character from the display.
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")
            self.result_shown = False
        return "break"

    def on_key_press(self, event):
        """
        Intercept keyboard input to prevent double insertion.
        Only digits and allowed operators are passed to button_click.
        """
        char = event.char
        if char.isdigit() or char in '+-*/.':
            self.button_click(char)
            return "break"
        elif char:
            # Block any other character (letters, spaces, etc.)
            return "break"



if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

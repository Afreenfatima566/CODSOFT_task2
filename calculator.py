import tkinter as tk
from tkinter import font

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x550")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.current_input = "0"
        self.previous_input = ""
        self.operation = ""
        self.reset_on_next_input = False
        
        # Create display
        self.display_font = font.Font(family="Arial", size=28, weight="bold")
        self.display = tk.Entry(
            root, 
            font=self.display_font, 
            justify="right", 
            bd=0, 
            bg="#222222", 
            fg="#ffffff", 
            insertbackground="#ffffff",
            readonlybackground="#222222"
        )
        self.display.insert(0, self.current_input)
        self.display.config(state="readonly")
        self.display.pack(fill="x", padx=20, pady=20, ipady=20)
        
        # Create button frame
        button_frame = tk.Frame(root, bg="#2b2b2b")
        button_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        
        # Button definitions
        buttons = [
            ['C', 0, 0, 1, 'special'],
            ['⌫', 0, 1, 1, 'special'],
            ['÷', 0, 2, 1, 'operation'],
            ['×', 0, 3, 1, 'operation'],
            ['7', 1, 0, 1, ''],
            ['8', 1, 1, 1, ''],
            ['9', 1, 2, 1, ''],
            ['-', 1, 3, 1, 'operation'],
            ['4', 2, 0, 1, ''],
            ['5', 2, 1, 1, ''],
            ['6', 2, 2, 1, ''],
            ['+', 2, 3, 1, 'operation'],
            ['1', 3, 0, 1, ''],
            ['2', 3, 1, 1, ''],
            ['3', 3, 2, 1, ''],
            ['=', 3, 3, 1, 'operation'],
            ['0', 4, 0, 2, ''],
            ['.', 4, 2, 1, ''],
            ['%', 4, 3, 1, 'operation']
        ]
        
        # Create buttons
        self.button_font = font.Font(family="Arial", size=18, weight="bold")
        for text, row, col, colspan, style in buttons:
            btn = tk.Button(
                button_frame, 
                text=text, 
                font=self.button_font,
                command=lambda t=text: self.on_button_click(t)
            )
            
            # Style buttons based on type
            if style == 'operation':
                btn.configure(bg="#ff9500", fg="#ffffff", activebackground="#ffbb66")
            elif style == 'special':
                btn.configure(bg="#a5a5a5", fg="#000000", activebackground="#d0d0d0")
            else:
                btn.configure(bg="#3a3a3a", fg="#ffffff", activebackground="#5a5a5a")
            
            btn.configure(
                relief="flat", 
                bd=0, 
                highlightthickness=0,
                height=2
            )
            btn.grid(
                row=row, 
                column=col, 
                columnspan=colspan, 
                sticky="nsew", 
                padx=5, 
                pady=5
            )
    
    def on_button_click(self, text):
        if text in '0123456789':
            self.input_digit(text)
        elif text == '.':
            self.input_decimal()
        elif text in ['+', '-', '×', '÷']:
            self.set_operation(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '%':
            self.percentage()
    
    def update_display(self):
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
        self.display.config(state="readonly")
    
    def input_digit(self, digit):
        if self.reset_on_next_input:
            self.current_input = "0"
            self.reset_on_next_input = False
        
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.update_display()
    
    def input_decimal(self):
        if self.reset_on_next_input:
            self.current_input = "0"
            self.reset_on_next_input = False
        
        if '.' not in self.current_input:
            self.current_input += '.'
            self.update_display()
    
    def set_operation(self, op):
        if self.operation and not self.reset_on_next_input:
            self.calculate()
        
        self.previous_input = self.current_input
        self.operation = op
        self.reset_on_next_input = True
    
    def calculate(self):
        if not self.operation or self.reset_on_next_input:
            return
        
        try:
            current = float(self.current_input)
            previous = float(self.previous_input)
            
            if self.operation == '+':
                result = previous + current
            elif self.operation == '-':
                result = previous - current
            elif self.operation == '×':
                result = previous * current
            elif self.operation == '÷':
                if current == 0:
                    self.display.config(state="normal")
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Error")
                    self.display.config(state="readonly")
                    self.clear()
                    return
                result = previous / current
            
            # Format result
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
            
            self.current_input = str(result)
            self.update_display()
            self.reset_on_next_input = True
            self.operation = ""
            
        except Exception as e:
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.display.config(state="readonly")
            self.clear()
    
    def clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = ""
        self.reset_on_next_input = False
        self.update_display()
    
    def backspace(self):
        if self.reset_on_next_input:
            return
            
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        
        self.update_display()
    
    def percentage(self):
        try:
            value = float(self.current_input) / 100
            if value.is_integer():
                value = int(value)
            else:
                value = round(value, 10)
            self.current_input = str(value)
            self.update_display()
        except:
            self.display.config(state="normal")
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.display.config(state="readonly")
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
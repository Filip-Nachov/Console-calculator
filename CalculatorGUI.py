import tkinter as tk
from tkinter import messagebox
import math
import os

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("580x580")  # Set the window size
        self.history_file = "history.txt"
        self.history = self.load_history(self.history_file)
        self.memory = 0
        self.create_widgets()

        # Bind keyboard events
        self.root.bind('<Key>', self.key_press_event)
        self.root.bind('<BackSpace>', self.handle_backspace)

    def create_widgets(self):
        self.entry = tk.Entry(self.root, width=30, borderwidth=5, font=('Arial', 24))
        self.entry.grid(row=0, column=0, columnspan=5, pady=20, ipady=20)

        buttons = [
            ('MRC', 1, 0), ('M-', 1, 1), ('M+', 1, 2), ('SQRT', 1, 3), ('MOD', 1, 4),
            ('LOG', 2, 0), ('EXP', 2, 1), ('SIN', 2, 2), ('COS', 2, 3), ('TAN', 2, 4),
            ('-->', 3, 0), ('7', 3, 1), ('8', 3, 2), ('9', 3, 3), ('/', 3, 4),
            ('CE', 4, 0), ('4', 4, 1), ('5', 4, 2), ('6', 4, 3), ('*', 4, 4),
            ('AC', 5, 0), ('1', 5, 1), ('2', 5, 2), ('3', 5, 3), ('-', 5, 4),
            ('0', 6, 0), ('00', 6, 1), ('.', 6, 2), ('=', 6, 3), ('+', 6, 4)
            
        ]

        for (text, row, col) in buttons:
            # Adjust button styles based on text
            if text in ['CE', 'AC']:
                button = tk.Button(self.root, text=text, width=7, height=2, command=lambda t=text: self.button_click(t), bg='lightcoral', fg='white')
            elif text.isdigit() or text == '.':
                button = tk.Button(self.root, text=text, width=7, height=2, command=lambda t=text: self.button_click(t), bg='black', fg='white')
            else:
                button = tk.Button(self.root, text=text, width=7, height=2, command=lambda t=text: self.button_click(t), bg='dimgray', fg='white')
            
            button.grid(row=row, column=col, padx=5, pady=5)
            button.config(font=('Arial', 14), relief='raised', bd=5)

    def button_click(self, text):
        if text == '=':
            self.calculate()
        elif text == 'SQRT':
            self.single_operand_operation('SQRT')
        elif text == 'LOG':
            self.single_operand_operation('LOG')
        elif text == 'EXP':
            self.single_operand_operation('EXP')
        elif text == 'SIN':
            self.single_operand_operation('SIN')
        elif text == 'COS':
            self.single_operand_operation('COS')
        elif text == 'TAN':
            self.single_operand_operation('TAN')
        elif text == 'M+':
            self.store_memory('M+')
        elif text == 'M-':
            self.store_memory('M-')
        elif text == 'MRC':
            self.recall_memory()
        elif text == 'MOD':
            self.add_operator('%')
        elif text == '-->':
            self.handle_backspace()  # Trigger backspace action
        elif text == 'CE':
            self.clear_entry()
        elif text == 'AC':
            self.clear_all()
        else:
            self.entry.insert(tk.END, text)

    def calculate(self):
        try:
            expression = self.entry.get().replace('%', '/100')
            result = eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
            self.add_to_history(f"{expression} = {result}\n")
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")

    def single_operand_operation(self, op):
        try:
            num = float(self.entry.get())
            if op == 'SQRT':
                result = math.sqrt(num)
            elif op == 'LOG':
                result = math.log(num)
            elif op == 'EXP':
                result = math.exp(num)
            elif op == 'SIN':
                result = math.sin(math.radians(num))
            elif op == 'COS':
                result = math.cos(math.radians(num))
            elif op == 'TAN':
                result = math.tan(math.radians(num))
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
            self.add_to_history(f"{op}({num}) = {result}\n")
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")

    def store_memory(self, operation):
        try:
            if operation == 'M+':
                self.memory += float(self.entry.get())
            elif operation == 'M-':
                self.memory -= float(self.entry.get())
            messagebox.showinfo("Memory", f"Memory updated: {self.memory}")
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")

    def recall_memory(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.memory)

    def show_history(self):
        history_text = "".join(self.history)
        messagebox.showinfo("History", history_text if history_text else "No history available")

    def clear_history(self):
        self.history.clear()
        self.save_history(self.history_file, self.history)
        messagebox.showinfo("History", "History cleared")

    def load_history(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return file.readlines()
        return []

    def save_history(self, filename, history):
        with open(filename, 'w') as file:
            file.writelines(history)

    def add_to_history(self, entry):
        self.history.append(entry)
        self.save_history(self.history_file, self.history)

    def add_operator(self, operator):
        self.entry.insert(tk.END, operator)

    def handle_backspace(self, event=None):
        self.entry.delete(len(self.entry.get()) - 1, tk.END)

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.memory = 0

    def key_press_event(self, event):
        key = event.char

        # Check if the key is a digit or a valid operator
        if key.isdigit() or key == '.':
            # Allow digits and decimal point to be inserted
            self.entry.insert(tk.END, key)
        
        # Handle valid operators
        elif key in ['+', '-', '*', '/', '%']:
            current_text = self.entry.get()

            # Check if the current text is not empty and the last character is not an operator
            if current_text and current_text[-1] not in ['+', '-', '*', '/', '%']:
                # Insert the operator
                self.entry.insert(tk.END, key)
        
        # Handle Enter key for calculation
        elif key == '\r':
            self.calculate()

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

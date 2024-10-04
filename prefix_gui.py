import tkinter as tk

# Define colors
BACKGROUND_COLOR = '#fff4f4'
TEXT_COLOR = '#000000'
BUTTON_COLOR = '#d8e1cb'
ENTRY_COLOR = '#fce5cd'

class Stack:
    def __init__(self, size):
        self.size = size
        self.arr1 = [None] * size
        self.top = -1

    def top_ele(self):
        if self.top == -1:
            return None
        return self.arr1[self.top]

    def push(self, ele):
        if self.top >= self.size - 1:
            print("Stack Overflow!")
        else:
            self.top += 1
            self.arr1[self.top] = ele

    def pop(self):
        if self.top < 0:
            print("Stack Underflow!")
            return None
        else:
            popped_element = self.arr1[self.top]
            self.top -= 1
            return popped_element

    def traverse(self):
        elements = []
        for i in range(0, self.top + 1):
            elements.append(self.arr1[i])
        return elements

def infix_to_postfix(string):
    symbol = Stack(len(string))
    expression = Stack(len(string))
    steps = []

    for i in string:
        if i == '(':
            symbol.push(i)
        elif i in ('^', '*', '/', '+', '-'):
            if i == '^':
                while symbol.top_ele() == '^':
                    expression.push(symbol.pop())
                symbol.push(i)
            elif i in ('*', '/'):
                while symbol.top_ele() in ('^', '*', '/'):
                    expression.push(symbol.pop())
                symbol.push(i)
            elif i in ('+', '-'):
                while symbol.top_ele() in ('+', '-', '*', '/', '^'):
                    expression.push(symbol.pop())
                symbol.push(i)
        elif i == ')':
            while symbol.top_ele() != '(':
                expression.push(symbol.pop())
            symbol.pop()
        else:
            expression.push(i)

        steps.append((list(symbol.traverse()), list(expression.traverse())))

    while symbol.top != -1:
        expression.push(symbol.pop())
        steps.append((list(symbol.traverse()), list(expression.traverse())))

    return steps

def infix_to_prefix(string):
    # Reverse the string and convert parentheses
    rev_string = string[::-1]
    rev_string = ''.join('(' if ch == ')' else ')' if ch == '(' else ch for ch in rev_string)

    symbol = Stack(len(rev_string))
    expression = Stack(len(rev_string))
    steps = []

    for i in rev_string:
        current_char_text.delete(1.0, tk.END)  # Clear the text widget
        current_char_text.insert(tk.END, i)  # Insert the current character
        if i == '(':
            symbol.push(i)
        elif i == ')':
            while symbol.top_ele() is not None and symbol.top_ele() != '(':
                expression.push(symbol.pop())
            if symbol.top_ele() == '(':
                symbol.pop()
        elif i in '^*/+-':
            while (symbol.top_ele() is not None and
                   symbol.top_ele() != '(' and
                   ((i in '+-' and symbol.top_ele() in '*/^') or
                    (i in '*/' and symbol.top_ele() in '^') or
                    (i in '^' and symbol.top_ele() in '*/'))):
                expression.push(symbol.pop())
            symbol.push(i)
        else:
            expression.push(i)

        steps.append((list(symbol.traverse()), list(expression.traverse())))

    while symbol.top != -1:
        expression.push(symbol.pop())
        steps.append((list(symbol.traverse()), list(expression.traverse())))

    # Reverse the result for prefix
    intermediate = []
    while expression.top != -1:
        intermediate.append(expression.pop())
    prefix = "".join(intermediate)

    return steps, prefix[::-1]  # Reverse the result for prefix

def on_button_click():
    input_expression = input_field.get()
    if var.get() == 1:  # Checkbox is selected, perform postfix conversion
        steps = infix_to_postfix(input_expression)
        output1.delete(1.0, tk.END)
        output2.delete(1.0, tk.END)
        current_char_text.delete(1.0, tk.END)
        horizontal_output.delete(1.0, tk.END)
        for i in input_field.get():
            current_char_text.insert(tk.END,i+'\n')
        for step in steps:
            symbols, expressions = step
            output1.insert(tk.END, " ".join(map(str, symbols)) + '\n')
            output2.insert(tk.END, " ".join(map(str, expressions)) + '\n')
        horizontal_output.insert(tk.END, " ".join(map(str, steps[-1][1])))
    else:  # Checkbox is not selected, perform prefix conversion
        steps, prefix = infix_to_prefix(input_expression)
        prefix_rev=prefix[::-1]
        output1.delete(1.0, tk.END)
        output2.delete(1.0, tk.END)
        current_char_text.delete(1.0, tk.END)
        horizontal_output.delete(1.0, tk.END)
        for i in input_field.get()[::-1]:
            current_char_text.insert(tk.END,i+'\n')
        for step in steps:
            symbols, expressions = step
            output1.insert(tk.END, " ".join(map(str, symbols)) + '\n')
            output2.insert(tk.END, " ".join(map(str, expressions)) + '\n')
        horizontal_output.insert(tk.END, prefix_rev)

# Initialize the main window
root = tk.Tk()
root.title("Infix to Postfix/Prefix")
root.geometry('650x600')
root.resizable(0, 0)
root.configure(bg=BACKGROUND_COLOR)

# Create input field and button at the top
input_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
input_frame.pack(pady=5)

input_field = tk.Entry(input_frame, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR)
input_field.pack(side=tk.LEFT, padx=(20, 5), ipadx=30)

button = tk.Button(input_frame, text="Submit", command=on_button_click, bg=BUTTON_COLOR, fg='#ffffff')
button.pack(side=tk.LEFT, padx=(30, 10))

# Create a frame for the checkboxes
checkbox_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
checkbox_frame.pack(pady=5)

# Checkbox for postfix/prefix
var = tk.IntVar(value=1)
checkbox_postfix = tk.Checkbutton(checkbox_frame, text="Postfix", variable=var, onvalue=1, offvalue=0, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
checkbox_postfix.pack(side=tk.LEFT, padx=(20, 5))

checkbox_prefix = tk.Checkbutton(checkbox_frame, text="Prefix", variable=var, onvalue=0, offvalue=1, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
checkbox_prefix.pack(side=tk.LEFT, padx=(20, 5))

# Create a frame for the output fields
output_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
output_frame.pack(pady=10)

# Frame for current character and vertical outputs
current_char_and_outputs_frame = tk.Frame(output_frame, bg=BACKGROUND_COLOR)
current_char_and_outputs_frame.pack(side=tk.LEFT, padx=10)

# Frame for current character display
output_fields_frame = tk.Frame(current_char_and_outputs_frame, bg=BACKGROUND_COLOR)
output_fields_frame.pack(side=tk.LEFT, padx=10)

current_char_text = tk.Text(output_fields_frame, height=25, width=20, bg=ENTRY_COLOR, fg=TEXT_COLOR, wrap='none')
current_char_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

current_char_horizontal_scrollbar = tk.Scrollbar(output_fields_frame, orient=tk.HORIZONTAL, command=current_char_text.xview)
current_char_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
current_char_text.config(xscrollcommand=current_char_horizontal_scrollbar.set)

current_char_vertical_scrollbar = tk.Scrollbar(output_fields_frame, orient=tk.VERTICAL, command=current_char_text.yview)
current_char_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
current_char_text.config(yscrollcommand=current_char_vertical_scrollbar.set)

# Output fields for steps
output1 = tk.Text(output_fields_frame, height=25, width=20, bg=ENTRY_COLOR, fg=TEXT_COLOR, wrap='none')
output1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output1_horizontal_scrollbar = tk.Scrollbar(output_fields_frame, orient=tk.HORIZONTAL, command=output1.xview)
output1_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
output1.config(xscrollcommand=output1_horizontal_scrollbar.set)

output1_vertical_scrollbar = tk.Scrollbar(output_fields_frame, orient=tk.VERTICAL, command=output1.yview)
output1_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output1.config(yscrollcommand=output1_vertical_scrollbar.set)

# Second output field for expressions
output2 = tk.Text(output_fields_frame, height=25, width=20, bg=ENTRY_COLOR, fg=TEXT_COLOR, wrap='none')
output2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output2_horizontal_scrollbar = tk.Scrollbar(output_fields_frame, orient=tk.HORIZONTAL, command=output2.xview)
output2_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
output2.config(xscrollcommand=output2_horizontal_scrollbar.set)

output2_vertical_scrollbar = tk.Scrollbar(output_fields_frame, orient=tk.VERTICAL, command=output2.yview)
output2_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output2.config(yscrollcommand=output2_vertical_scrollbar.set)

# Output field for final result
horizontal_output_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
horizontal_output_frame.pack(pady=10)

horizontal_output = tk.Text(horizontal_output_frame, height=2, width=60, bg=ENTRY_COLOR, fg=TEXT_COLOR, wrap='none')
horizontal_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

horizontal_output_horizontal_scrollbar = tk.Scrollbar(horizontal_output_frame, orient=tk.HORIZONTAL, command=horizontal_output.xview)
horizontal_output_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
horizontal_output.config(xscrollcommand=horizontal_output_horizontal_scrollbar.set)

horizontal_output_vertical_scrollbar = tk.Scrollbar(horizontal_output_frame, orient=tk.VERTICAL, command=horizontal_output.yview)
horizontal_output_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
horizontal_output.config(yscrollcommand=horizontal_output_vertical_scrollbar.set)

root.mainloop()
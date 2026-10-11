import ast 
import operator 
import math 
import tkinter as tk

# TKinter
window = tk.Tk()
window.title("Calculator")

SYMBOL_TO_MATH = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

NAME_TO_MATH = {
    "sqrt": math.sqrt,
    "abs": abs,
}

KEYPAD_ROWS = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "(", ")"],
    ["+", "**", "%", ","], 
]

def solve (piece):
    if isinstance(piece, ast.Expression):
        return solve(piece.body)
    if isinstance(piece, ast.Constant):
        return piece.value 
    if isinstance(piece, ast.BinOp):
        left_value = solve(piece.left)
        right_value = solve(piece.right)
        do_math = SYMBOL_TO_MATH[type(piece.op)]
        return do_math(left_value, right_value)
    if isinstance(piece, ast.UnaryOp):
        number = solve(piece.operand)
        return -(number)
    if isinstance(piece, ast.Call):
        name = piece.func.id
        do_math = NAME_TO_MATH[name]
        numbers = []
        for arg in piece.args:
            numbers.append(solve(arg))
        return do_math(*numbers)
    raise ValueError("Invalid my boi")

#tree = ast.parse("-5", mode="eval")
#print(solve(tree))

#print(solve(ast.parse("sqrt(16)", mode="eval")))
#print(solve(ast.parse("abs(-5)", mode="eval")))
#print(solve(ast.parse("sqrt(2 + 2)", mode="eval")))
#print(solve(ast.parse("sqrt(abs(-9))", mode="eval")))

ALLOWED_CHARACTERS = "0123456789+-*/%.(), "
for name in NAME_TO_MATH:
    ALLOWED_CHARACTERS += name

def only_allowed(new_text):
    for character in new_text:
        if character not in ALLOWED_CHARACTERS:
            return False
    return True

check_command = window.register(only_allowed)

display_box = tk.Entry(window, font=("Arial", 20), justify="right", width=12, validate="key", validatecommand=(check_command, "%P"))
display_box.grid(row = 0, column = 0, columnspan=4, padx=5, pady=5)

answer_label = tk.Label(window, text="", font=("Arial", 12))
answer_label.grid(row=1, column=0, columnspan=4)



#Building the Keypad
def clear_display():
    display_box.delete(0, tk.END)
    answer_label.config(text="")

def add_to_display(label):
    display_box.insert(tk.END, label)

def format_anser(answer):
    if isinstance(answer, float) and answer.is_integer():
        return int(answer)


def on_equals():
    text = display_box.get()
    try:
        tree = ast.parse(text, mode="eval")
        answer = solve(tree)
        answer_label.config(text="= " + str(answer))
    except ZeroDivisionError:
        answer_label.config(text="Cannot divide by zero")
    except (SyntaxError, ValueError, KeyError, TypeError):
        answer_label.config(text="Invalid expression")

def delete_last():
    display_box.delete(len(display_box.get()) - 1)

for row_number, row_labels in enumerate(KEYPAD_ROWS):
    for column_number, label in enumerate(row_labels):
        tk.Button(
            window,
            text=label,
            width=5,
            height=2,
            command=lambda text=label: add_to_display(text)
        ).grid(row=row_number + 2, column=column_number)

# Extra calculator actions
tk.Button(window, text="C", width=5, height=2, command=clear_display).grid(row=7, column=0)
tk.Button(window, text="⌫", width=5, height=2, command=delete_last).grid(row=7, column=1)
tk.Button(window, text="=", width=11, height=2, command=on_equals).grid(row=7, column=2, columnspan=2)

for column in range(4):
    window.columnconfigure(column, weight=1)
window.bind("<Return>", lambda event: on_equals())
window.mainloop()
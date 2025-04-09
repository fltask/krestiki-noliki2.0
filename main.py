import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
# Увеличиваем высоту окна, чтобы появилась кнопка сброса снизу
window.geometry("300x400")

current_player = "X"
buttons = []

def reset_game():
    global current_player
    current_player = "X"  # начинаем с игрока "X"
    # Проходим по всем кнопкам и очищаем их содержимое, а также возвращаем стандартный вид
    for row in buttons:
        for btn in row:
            btn.config(text="", bg="SystemButtonFace", state=tk.NORMAL)

def check_winner():
    # Проверка строк и столбцов
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return True
    # Проверка диагоналей
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True
    return False

def on_click(row, col):
    global current_player

    # Если клетка уже заполнена, выходим из функции
    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player

    if check_winner():
        messagebox.showinfo("Игра окончена", f"Игрок {current_player} победил!")
        # После победы можно отключить все кнопки
        for r in buttons:
            for btn in r:
                btn.config(state=tk.DISABLED)
        return

    # Проверка на ничью: если все кнопки заполнены и победителя нет
    if all(btn["text"] != "" for row in buttons for btn in row):
        messagebox.showinfo("Игра окончена", "Ничья!")
        return

    # Смена игрока
    current_player = "0" if current_player == "X" else "X"

# Создаем игровое поле из 3х3 кнопок
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

# Добавление кнопки сброса внизу игрового поля
reset_button = tk.Button(window, text="Сбросить игру", font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, pady=10)

window.mainloop()

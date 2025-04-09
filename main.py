import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("320x480")
window.resizable(False, False)
window.configure(bg="#f0f0f0")  # Светлый фон окна

current_player = "X"
buttons = []

# Заголовок игры
title_label = tk.Label(window, text="Крестики-нолики", font=("Helvetica", 20, "bold"),
                       bg="#f0f0f0", fg="#333333")
title_label.pack(pady=10)

# Фрейм для игрового поля
grid_frame = tk.Frame(window, bg="#f0f0f0")
grid_frame.pack()

# Метка состояния игры (кто ходит, победитель, ничья и т.д.)
status_label = tk.Label(window, text="Ходит игрок X", font=("Helvetica", 14),
                        bg="#f0f0f0", fg="#555555")
status_label.pack(pady=5)


def reset_game():
    global current_player
    current_player = "X"
    status_label.config(text="Ходит игрок X")
    # Очищаем все кнопки и возвращаем им исходный вид
    for row in buttons:
        for btn in row:
            btn.config(text="", bg="#ffffff", state=tk.NORMAL)


def check_winner():
    # Проверяем строки и столбцы
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return buttons[i][0]["text"]
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return buttons[0][i]["text"]
    # Проверяем диагонали
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return buttons[0][0]["text"]
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return buttons[0][2]["text"]
    return None


def on_click(row, col):
    global current_player

    # Если клетка уже занята, выходим из функции
    if buttons[row][col]["text"] != "":
        return

    # Отрисовка хода с различием по цвету для каждого игрока
    if current_player == "X":
        buttons[row][col].config(text="X", fg="#1E90FF")
    else:
        buttons[row][col].config(text="0", fg="#32CD32")

    # Проверяем наличие победителя
    winner = check_winner()
    if winner:
        messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")
        status_label.config(text=f"Победитель: {winner}")
        # Деактивируем игровое поле после победы
        for r in buttons:
            for btn in r:
                btn.config(state=tk.DISABLED)
        return

    # Проверяем ничью
    if all(btn["text"] != "" for row in buttons for btn in row):
        messagebox.showinfo("Игра окончена", "Ничья!")
        status_label.config(text="Ничья!")
        return

    # Переключаем игрока
    current_player = "0" if current_player == "X" else "X"
    status_label.config(text=f"Ходит игрок {current_player}")


# Создаем игровое поле (3х3 кнопок)
for i in range(3):
    row_buttons = []
    for j in range(3):
        btn = tk.Button(grid_frame, text="", font=("Helvetica", 24, "bold"),
                        width=4, height=2, bg="#ffffff", relief="raised", bd=3,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(btn)
    buttons.append(row_buttons)

# Кнопка для начала новой игры
reset_button = tk.Button(window, text="Новая игра", font=("Helvetica", 14),
                         bg="#FFDEAD", fg="#8B4513", command=reset_game)
reset_button.pack(pady=10)

window.mainloop()

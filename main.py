import tkinter as tk
from tkinter import messagebox

# Глобальные переменные для подсчёта побед игроков в турнире
wins_X = 0  # Количество побед игрока, играющего за "X"
wins_0 = 0  # Количество побед игрока, играющего за "0"
current_player = None  # Текущий игрок ("X" или "0"), определяется после выбора символа
player_symbol = None  # Символ, выбранный игроком ("X" или "0")

# Создание главного окна приложения
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("320x580")  # Устанавливаем размер окна
window.resizable(False, False)  # Запрещаем изменение размеров окна
window.configure(bg="#f0f0f0")  # Задаём цвет фона окна

# ============================
# Фрейм для выбора символа
# ============================
# Этот фрейм будет показываться первым, чтобы игрок выбрал, за кого играть
selection_frame = tk.Frame(window, bg="#f0f0f0")
# Размещаем фрейм выбора в главном окне с отступами
selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Метка с предложением выбрать символ
sel_label = tk.Label(selection_frame, text="Выберите, за кого играть:",
                     font=("Helvetica", 14), bg="#f0f0f0")
# Размещаем метку, объединяя 2 столбца
sel_label.grid(row=0, column=0, columnspan=2, pady=10)

# Фрейм для кнопок выбора символа
btn_frame = tk.Frame(selection_frame, bg="#f0f0f0")
btn_frame.grid(row=1, column=0, columnspan=2, pady=5)

# Кнопка для выбора символа "X"
x_button = tk.Button(btn_frame, text="Играть за X", font=("Helvetica", 12),
                     width=10, command=lambda: start_game("X"))
x_button.grid(row=0, column=0, padx=5, pady=5)

# Кнопка для выбора символа "0"
o_button = tk.Button(btn_frame, text="Играть за 0", font=("Helvetica", 12),
                     width=10, command=lambda: start_game("0"))
o_button.grid(row=0, column=1, padx=5, pady=5)

# ============================
# Фрейм для игрового поля
# ============================
# Этот фрейм содержит заголовок игры, метки статуса и счета, а также игровое поле (3х3)
game_frame = tk.Frame(window, bg="#f0f0f0")
# Размещаем game_frame, но изначально скрываем его (используем grid_remove)
game_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
game_frame.grid_remove()

# Заголовок игры
title_label = tk.Label(game_frame, text="Крестики-нолики", font=("Helvetica", 20, "bold"),
                       bg="#f0f0f0", fg="#333333")
title_label.grid(row=0, column=0, columnspan=3, pady=5)

# Метка для отображения текущего состояния игры (например, чей ход или победитель)
status_label = tk.Label(game_frame, text="", font=("Helvetica", 14),
                        bg="#f0f0f0", fg="#555555")
status_label.grid(row=1, column=0, columnspan=3, pady=5)

# Метка для отображения счета турнира
score_label = tk.Label(game_frame, text="", font=("Helvetica", 14, "bold"),
                       bg="#f0f0f0", fg="#000000")
score_label.grid(row=2, column=0, columnspan=3, pady=5)

# Фрейм для игрового поля (сетка 3х3)
grid_frame = tk.Frame(game_frame, bg="#f0f0f0")
grid_frame.grid(row=3, column=0, columnspan=3, pady=10)

# Список для хранения кнопок игрового поля
buttons = []


# ===========================================
# Функция обновления метки счета
# ===========================================
def update_score_label():
    """
    Обновляет текст метки счета с текущими результатами.
    """
    score_label.config(text=f"Счет: X - {wins_X}  0 - {wins_0}")


# ===========================================
# Функция сброса игрового поля
# ===========================================
def reset_board(next_start=None):
    """
    Очищает все кнопки игрового поля, чтобы начать новый раунд.

    Параметры:
      next_start: Опционально, задает, кто начинает следующий раунд.
                  Если не задан, по умолчанию начинается игрок "X".
    """
    global current_player
    for row in buttons:
        for btn in row:
            btn.config(text="", bg="#ffffff", state=tk.NORMAL)
    current_player = next_start if next_start else "X"
    status_label.config(text=f"Ходит игрок {current_player}")


# ===========================================
# Функция блокировки игрового поля
# ===========================================
def disable_board():
    """
    Деактивирует все кнопки игрового поля, чтобы предотвратить дальнейшие ходы.
    """
    for row in buttons:
        for btn in row:
            btn.config(state=tk.DISABLED)


# ===========================================
# Функция проверки победителя с выделением выигрышной комбинации
# ===========================================
def check_winner():
    """
    Проверяет игровое поле на наличие трёх одинаковых символов подряд и выделяет выигрышную комбинацию.

    Возвращает:
      Символ победителя ("X" или "0"), если такая комбинация найдена.
      Иначе возвращает None.
    """
    # Проверка строк
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            # Выделяем выигрышную строку, изменяя фон кнопок
            for btn in buttons[i]:
                btn.config(bg="#ffeb99")  # светло-жёлтый фон
            return buttons[i][0]["text"]
    # Проверка столбцов
    for i in range(3):
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            # Выделяем выигрышный столбец
            for j in range(3):
                buttons[j][i].config(bg="#ffeb99")
            return buttons[0][i]["text"]
    # Проверка главной диагонали
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        # Выделяем главную диагональ
        for i in range(3):
            buttons[i][i].config(bg="#ffeb99")
        return buttons[0][0]["text"]
    # Проверка второстепенной диагонали
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        # Выделяем второстепенную диагональ
        buttons[0][2].config(bg="#ffeb99")
        buttons[1][1].config(bg="#ffeb99")
        buttons[2][0].config(bg="#ffeb99")
        return buttons[0][2]["text"]

    return None


# ===========================================
# Функция обработки кликов по игровому полю
# ===========================================
def on_click(row, col):
    """
    Обрабатывает клик по кнопке игрового поля.

    Параметры:
      row: Номер строки кнопки
      col: Номер столбца кнопки
    """
    global current_player, wins_X, wins_0

    # Если клетка уже занята, выходим из функции
    if buttons[row][col]["text"] != "":
        return

    # Отрисовываем ход игрока с различной раскраской:
    if current_player == "X":
        buttons[row][col].config(text="X", fg="#1E90FF")
    else:
        buttons[row][col].config(text="0", fg="#32CD32")

    # Проверяем наличие победителя после сделанного хода
    winner = check_winner()
    if winner:
        # Если найден победитель, обновляем счет
        if winner == "X":
            wins_X += 1
        else:
            wins_0 += 1

        update_score_label()
        messagebox.showinfo("Раунд окончен", f"Раунд выиграл игрок {winner}!")

        # Если один из игроков набрал 3 победы, завершаем турнир
        if wins_X == 3 or wins_0 == 3:
            messagebox.showinfo("Турнир окончен", f"Победитель турнира: {winner}")
            disable_board()
            status_label.config(text=f"Турнир окончен. Победитель: {winner}")
            return

        # Если турнир не завершён, начинаем новый раунд.
        reset_board(next_start=winner)
        return

    # Проверка на ничью: если все кнопки заполнены, а победителя нет
    if all(btn["text"] != "" for row in buttons for btn in row):
        messagebox.showinfo("Раунд окончен", "Ничья!")
        # При ничье можно чередовать первого игрока в следующем раунде
        next_start = "0" if current_player == "X" else "X"
        reset_board(next_start=next_start)
        return

    # Меняем текущего игрока: если до этого был "X", то теперь "0", и наоборот
    current_player = "0" if current_player == "X" else "X"
    status_label.config(text=f"Ходит игрок {current_player}")


# ===========================================
# Функция создания игрового поля (сетки 3х3)
# ===========================================
def create_board():
    """
    Создает 3 строки по 3 кнопки в каждой и добавляет их во фрейм grid_frame.
    Кнопки сохраняются в списке buttons для дальнейшей работы.
    """
    for i in range(3):
        row_buttons = []  # Список кнопок текущей строки
        for j in range(3):
            # Создание кнопки с начальным пустым текстом
            btn = tk.Button(grid_frame,
                            text="",
                            font=("Helvetica", 24, "bold"),
                            width=4,
                            height=2,
                            bg="#ffffff",  # Белый фон кнопки
                            relief="raised",  # Тип рамки кнопки
                            bd=3,
                            command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i, column=j, padx=5, pady=5)
            row_buttons.append(btn)
        buttons.append(row_buttons)


# ===========================================
# Функция сброса турнира
# ===========================================
def reset_tournament():
    """
    Обнуляет счет турнира и запускает новый раунд.
    """
    global wins_X, wins_0, current_player
    wins_X = 0
    wins_0 = 0
    update_score_label()
    reset_board(next_start="X")


# ===========================================
# Функция старта игры после выбора символа
# ===========================================
def start_game(chosen):
    """
    Запускает игру после того, как игрок выбрал символ.

    Параметры:
      chosen: выбранный игроком символ ("X" или "0")
    """
    global player_symbol, current_player
    player_symbol = chosen  # Сохраняем выбор игрока
    current_player = "X"  # Игра всегда начинается с "X"

    # Обновляем метку статуса в зависимости от выбора символа
    if player_symbol == "X":
        status_label.config(text="Ваш ход (вы играете за X)")
    else:
        status_label.config(text="Ход противника (вы играете за 0)")

    update_score_label()  # Отображаем начальный счет (0:0)

    # Скрываем фрейм выбора символа и показываем фрейм игры
    selection_frame.grid_remove()
    game_frame.grid()  # Делаем видимым фрейм игры


# ===========================================
# Основной запуск приложения
# ===========================================
# Сначала отображаем фрейм выбора символа
selection_frame.grid()
# Создаем игровое поле (кнопки 3х3) внутри game_frame
create_board()

# Кнопка для сброса турнира, расположенная в главном окне вне фреймов
reset_button = tk.Button(window, text="Новая игра", font=("Helvetica", 14),
                         bg="#FFDEAD", fg="#8B4513", command=reset_tournament)
reset_button.grid(row=2, column=0, pady=10)

# Запуск главного цикла обработки событий
window.mainloop()

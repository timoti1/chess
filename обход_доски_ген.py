import gui
import time
import random

популяция = []
численность_популяции = 110


def фитнес(генотип_агента):
    все_множество_клеток = {(i, j) for i in range(1, 9) for j in range(1, 9)}
    теоретически_возможные_движения = список_ходов_фигуры(gui.get_selected_figure())

    множество_достижимых_клеток = set()
    удачных_ходов = 0
    for x, y in генотип_агента:
        if not (1 <= x <= 8 and 1 <= y <= 8):
            return удачных_ходов

        if (x, y) in множество_достижимых_клеток:
            return удачных_ходов

        удачных_ходов += 1
        множество_достижимых_клеток.add((x, y))

    return удачных_ходов


def список_ходов_фигуры(фигура):
    возможные_движения = []

    if  фигура == 'король':
        возможные_движения = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]

    if  фигура == 'конь':
        возможные_движения = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    if  фигура == 'ладья':
        for i in range(1, 8):
            if i != 0:
                возможные_движения.append((i, 0))
                возможные_движения.append((-i, 0))
                возможные_движения.append((0, i))
                возможные_движения.append((0, -i))

    if  фигура == 'ферзь':
        for i in range(1, 8):
            возможные_движения.append((i, 0))
            возможные_движения.append((-i, 0))
            возможные_движения.append((0, i))
            возможные_движения.append((0, -i))
            возможные_движения.append((-i, -i))
            возможные_движения.append((i, -i))
            возможные_движения.append((i, i))
            возможные_движения.append((-i, i))

    return возможные_движения


def создание_начальной_популяции():
    global популяция, численность_популяции

    популяция = []
    теоретически_возможные_движения = список_ходов_фигуры(gui.get_selected_figure())

    for i in range(численность_популяции):
        ген = gui.начальная_клетка
        геном = [ген]

        for j in range(63):
            случайный_ход = random.choice(теоретически_возможные_движения)
            ген = (ген[0] + случайный_ход[0], ген[1] + случайный_ход[1])
            геном.append(ген)

        популяция.append(геном)


def список_лучших(количество):
    метрики = []
    for агент in популяция:
        метрики.append((фитнес(агент), агент))
    #     print(фитнес(агент), end=' ')
    # print()

    лучшие_метрики = sorted(метрики, key = lambda метрика: метрика[0])[-количество:]

    return [метрика[1] for метрика in лучшие_метрики]


def список_потомков(родители, плодовитость):
    потомки = []

    теоретически_возможные_движения = список_ходов_фигуры(gui.get_selected_figure())

    for родитель in родители:
        фитнес_родителя = фитнес(родитель)

        for i in range(плодовитость):
            наследственность = random.randint(1, фитнес_родителя)

            геном = родитель[:наследственность]
            ген = геном[-1]
            #продолжим геном от родителя случайными генами потомства
            for j in range(64 - наследственность):
                случайный_ход = random.choice(теоретически_возможные_движения)
                ген = (ген[0] + случайный_ход[0], ген[1] + случайный_ход[1])

                #пробуем до 8 раз выбрать случайный ген так, чтобы он был валидным
                попытка = 1
                while ((попытка <= 8) and not (1 <= ген[0] <= 8 and 1 <= ген[1] <= 8)) or (ген in геном):
                    попытка += 1
                    случайный_ход = random.choice(теоретически_возможные_движения)
                    ген = (ген[0] + случайный_ход[0], ген[1] + случайный_ход[1])

                геном.append(ген)

            потомки.append(геном)

    return потомки


def эволюция(число_поколений):
    global популяция

    создание_начальной_популяции()
    for i in range(число_поколений):
        лидеры = список_лучших(5)
        потомки = список_потомков(лидеры, 21)

        if i%10 == 0 and gui.get_debug():
            print('Поколение {}. Фитнес лидера {}'.format(i, фитнес(лидеры[-1])))

        популяция = random.sample(лидеры + потомки, k = численность_популяции)
        if фитнес(лидеры[-1]) == 64:
            if gui.get_debug():
                print('Решение найдено: {}'.format(лидеры[-1]))

            if gui.get_animate():
                показать_путь(лидеры[-1])

            return


def показать_путь(геном):
    if gui.get_animate():
        # gui.highlight_cell(*потенциально_достижимая_клетка, 'yellow', kind='dot')
        x_from, y_from = геном[0]
        for i, ген in enumerate(геном[1:]):
            x_to, y_to = ген

            gui.draw_arrow(x_from, y_from, x_to, y_to, 'lightgray')
            gui.draw_text(x_to, y_to, i + 2)
            time.sleep(gui.get_delay())

            x_from, y_from = x_to, y_to


def btn_click(event):
    start_time = time.time()

    gui.кнопка_расчитать.unbind('<Button-1>')
    gui.clear_board()

    эволюция(1000000)

    gui.кнопка_расчитать.bind('<Button-1>', btn_click)



if __name__ == '__main__':
    # рисуем доску
    gui.размер_доски = 600
    gui.init_gui(info_panel = True)
    gui.draw_board()
    gui.draw_start_point(1, 1)

    gui.кнопка_расчитать.bind('<Button-1>', btn_click)

    gui.окно.mainloop()


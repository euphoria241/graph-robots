import math
import Robot
import PySimpleGUI as sg
import time
import re
import hashlib

a, b, c, d, e, f, g, h, t = range(9)

matr = [
    {b: 1, c: 1, d: 1, e: 1, f: 1},  # a
    {c: 1, e: 1},  # b
    {d: 1},  # c
    {e: 1},  # d
    {f: 1},  # e
    {c: 1, g: 1, h: 1},  # f
    {f: 1, h: 1},  # g
    {f: 1, g: 1},  # h
    {} # t
]
matr = [
    {b: 1, c: 1},  # a
    {a: 1, c: 1},  # b
    {a: 1, b: 1, d: 1},  # c
    {c: 1, e: 1},  # d
    {d: 1, f: 1},  # e
    {e: 1, g: 1},  # f
    {f: 1}  # g
]
layout = [
    [sg.Text('Введите количество роботов (2 или 3): '), sg.InputText()
     ],
    [sg.Text('Введите начальную позицию 1-го робота (от 0 до 6) '), sg.InputText()
     ],
    [sg.Text('Введите начальную позицию 2-го робота (от 0 до 6) '), sg.InputText()
     ],
    [sg.Text('Введите скорость 1-го робота (1 или 2):'), sg.InputText()
     ],
    [sg.Text('Введите скорость 2-го робота (1 или 2):'), sg.InputText()
     ],
    [sg.Output(size=(88, 20))],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Robot', layout)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event=='Submit':


        n = len(matr)
        for i in range(len(matr)):
            for j in matr[i].keys():
                matr[j].update({i: matr[i].get(j)})

#print("Введите количество роботов (2 или 3): ")
#m = int(input())


        m=values[0]
        print(m)
        if not (m == 2 or m == 3):
            print("Что ты ввел")
        robots = []
      #  time.sleep(10)
        for i in range(1, m + 1):
            point=values[1]
     #       if point >= n:
      #          print("Начальная вершина не может быть больше количества вершин")
  #  print("Введите скорость ", i, "-го робота (1 или 2): ")
            speed=values[2]
  #  speed = int(input())
    #        if not (speed == 1 or speed == 2):
     #           print("Скорость не может быть другой кроме 1 или 2")
            robot = Robot.Robot(i, point, speed, 0)
            robots.append(robot)
        f = True
        print("222222222222222222222222222222222222222222222222222222222222222222")
        if len(robots) == 2:
            if robots[0].can_meet_two_robot(robots[1], matr) == True:
                fl = False
                sum = 0
                while not fl:
                    weight, road = robots[0].Dijkstra(matr)
                    weight_rb1, road_rb1 = robots[1].Dijkstra(matr)
                    weight = [x / robots[0].speed for x in weight]
                    weight_rb1 = [x / robots[1].speed for x in weight_rb1]
                    print(weight, road)
                    print(weight_rb1, road_rb1)
                    fl, p, p1, w = robots[0].meet_point_two_robot(robots[1], matr)
                    if fl:
                        sum += w
                        print("Встреча в точке:", p)
                        print("Добавили ещё тиков времени:", w)
                    elif not fl and p != math.inf:
                        sum += w
                        print("Первый робот в точке: ", p1, " ; Второй в точке: ", p)
                        print("Добавили ещё тиков времени:", w)
                    else:
                        print("Мы попали в петлю")
                        break
                if not fl:
                    print("точно петля")
                else:
                    print("В итоге прошло столько то времени", sum)
            else:
             print("Кидаем сообщение нельзя встретиться")
        elif len(robots) == 3:
            if robots[0].can_meet_three_robot(robots[1],robots[2], matr) == True:
                print("Тут творим")

            else:
                print("Кидаем сообщение нельзя")
window.close()
# ------------------------------------------------
# Класс для работы с роботом
#
#
# (C) 2020 Группа 4, Москва, Россия
#
#
import math
import queue


class Robot(object):
    def __init__(self, number, point, speed, vertex):
        """
        Создается робот с параметрами
        :param number: номер робота
        :param point: точка в которой находится робот сейчас
        :param speed: скорость робота
        :param vertex: оставшийся путь до вершины
        """
        self.number = number
        self.point = point
        self.speed = speed
        self.vertex = vertex

    def Dijkstra(self, matrix):
        """
        Алгоритм Дейекстры
        :param matrix: список смежностей графа
        :return road: список хранящий путь до вершины
        :return: weight_road: список весов для всех вершин
        """

        """
        :param n: количество вершин в графе
        :param queue_vertex: очередь вершин для перебора (изнчально пустой)
        :param visited_vertex: список вершин, которые ещё не были в очереди (изначально все true)
        :param weight_road: список минимальных путей до вершины (изначально все inf)
        :param road: список вершин откуда мы попали в эту стартовая -1 (остальные inf)
        """

        # Начальные параметры для алгоритма
        n = len(matrix)
        queue_vertex = queue.Queue()
        visited_vertex = [True] * n
        weight_road = [math.inf] * n
        weight_road[self.point] = self.vertex
        road = [math.inf] * n
        road[self.point] = -1

        # Добавление в очередь начальной точки и выполнение основного алгоритма
        queue_vertex.put(self.point)
        while not queue_vertex.empty():
            vertex = queue_vertex.get()
            if visited_vertex[vertex]:
                for i in matrix[vertex].keys():
                    if matrix[vertex][i] + weight_road[vertex] < weight_road[i]:
                        weight_road[i] = matrix[vertex][i] + weight_road[vertex]
                        road[i] = vertex
                    queue_vertex.put(i)
                visited_vertex[vertex] = False

        # Возвращаем кортеж списка всех весов и путей из вершины во все остальные
        return weight_road, road

    def info(self):
        """
        Информация о объекте Robot, его номер, скорость и его позиция и остаток пути до вершины
        """
        print("Info about Robot")
        print("Number of Robot: "       + str(self.number))
        print("Speed of Robot: "        + str(self.speed))
        print("Point when robot stay: " + str(self.point))
        print("Length to vertex: "      + str(self.vertex))
        return True

    def can_meet_two_robot(self, robot1, matrix):
        """
        Проверка на существование пути между роботами
        :param robot1: Второй робот для проверки
        :param matrix: Граф представленный списком смежностей
        :return: True если существует, иначе False если нету пути
        """
        weight, road = robot1.Dijkstra(matrix)
        if weight[self.point] != math.inf:
            return True
        else:
            return False

    def can_meet_three_robot(self, robot1, robot2, matrix):
        """
        Проверка на существование пути между  тремя роботами
        :param robot1: Второй робот
        :param robot2: Третий робот
        :param matrix: Граф представленный списком смежностей
        :return: True если существует, иначе False если нету пути
        """
        weight, road = robot1.Dijkstra(matrix)
        if weight[self.point] != math.inf and weight[robot2.point] != math.inf:
            return True
        else:
            return False

    def meet_point_two_robot(self, robot1, matrix):
        """
        Поиск место встречи двух роботов, если невозможно сближаются
        :param robot1: Второй робот
        :param matrix: Входная матрица
        :return: (True, False) - нашли решение, точка второго робота, точка первого, сколько прошло тиков
        """
        weight, road = self.Dijkstra(matrix)
        weight_rb1, road_rb1 = robot1.Dijkstra(matrix)
        weight = [x/self.speed for x in weight]
        weight_rb1 = [x/robot1.speed for x in weight_rb1]
        min_time, point_meet = math.inf, math.inf
        min_time_zero, point_meet_zero = math.inf, math.inf
        for i in range(len(matrix)):
            if weight[i] != math.inf and weight_rb1[i] != math.inf:
                if abs(weight[i] - weight_rb1[i]) < min_time and weight[i] != 0 and weight_rb1[i] != 0:
                    min_time = abs(weight[i] - weight_rb1[i])
                    point_meet = i
                elif weight[i] == 0 and weight_rb1[i] == 0:
                    min_time = 0
                    point_meet = i
                elif abs(weight[i] - weight_rb1[i]) < min_time:
                    point_meet_zero = i
        if min_time == 0:
            print("min_time == 0")
            return True, point_meet, point_meet, weight[point_meet]
        elif min_time != math.inf:
            if min(weight[point_meet], weight_rb1[point_meet]) == weight[point_meet]:
                self.point = point_meet
                self.vertex = 0
                last, k = point_meet, road_rb1[point_meet]
                while True:
                    if weight_rb1[k] > weight[point_meet]:
                        last, k = k, road_rb1[k]
                    elif weight_rb1[k] == weight[point_meet]:
                        robot1.point = k
                        robot1.vertex = 0
                        return False, point_meet, k, weight[point_meet]
                    elif k != -1:
                        robot1.point = last
                        robot1.vertex = matrix[k][last] - (weight[point_meet] - weight_rb1[k])*robot1.speed
                        return False, point_meet, last, weight[point_meet]
                    else:
                        robot1.point = last
                        robot1.vertex = robot1.vertex - (weight[point_meet] - weight_rb1[k])*robot1.speed
                        return False, point_meet, last, weight[point_meet]
            elif min(weight[point_meet], weight_rb1[point_meet]) == weight_rb1[point_meet]:
                robot1.point = point_meet
                robot1.vertex = 0
                last, k = point_meet, road[point_meet]
                while True:
                    if weight[k] > weight_rb1[point_meet]:
                        last, k = k, road[k]
                    elif weight[k] == weight_rb1[point_meet]:
                        self.point = k
                        self.vertex = 0
                        return False, k, point_meet, weight_rb1[point_meet]
                    elif k != -1:
                        self.point = last
                        self.vertex = matrix[k][last] - (weight_rb1[point_meet] - weight[k])*self.speed
                        return False, last, point_meet, weight_rb1[point_meet]
                    else:
                        self.point = last
                        self.vertex = self.vertex - (weight_rb1[point_meet] - weight[k])*self.speed
                        return False, last, point_meet, weight_rb1[point_meet]
        else:
            if self.speed == robot1.speed:
                return False, math.inf, math.inf, point_meet_zero
            elif max(self.speed, robot1.speed) == self.speed and weight[point_meet_zero] == 0:
                return True, point_meet_zero, point_meet_zero, matrix[point_meet_zero][road_rb1[point_meet_zero]]
            elif max(self.speed, robot1.speed) == self.speed and weight[point_meet_zero] != 0:
                return True, road[point_meet_zero], road[point_meet_zero], matrix[road[point_meet]][point_meet_zero]
            elif max(self.speed, robot1.speed) == robot1.speed and weight_rb1[point_meet_zero] == 0:
                return True, point_meet_zero, point_meet_zero, matrix[point_meet_zero][road[point_meet_zero]]
            elif max(self.speed, robot1.speed) == robot1.speed and weight_rb1[point_meet_zero] != 0:
                return True, road_rb1[point_meet_zero], road_rb1[point_meet_zero], matrix[road_rb1[point_meet]][point_meet_zero]

        return False, math.inf, math.inf, 0

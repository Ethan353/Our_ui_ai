import random
from base import BaseAgent, TurnData, Action


class Node:
    def __init__(self, content, childs: list, cordinate: tuple, row):
        self.cordinate = cordinate
        self.content = content
        self.actionSrc = None
        self.actionGoal = None
        self.parentSrc = -1
        self.parentGoal = -1

        self.childs = childs
        self.index = row * cordinate[0] + cordinate[1]


class Graph:
    def __init__(self, rows, cols, mapp):
        self.index_based_dict = {}
        self.childs_list = []
        self.mapp = mapp
        self.rows = rows
        self.cols = cols

    def fillChilds(self):
        for r in range(self.rows):
            for c in range(self.cols):
                childs = []
                if self.mapp[r][c] == "*":
                    continue
                else:
                    if r + 1 < self.rows:
                        if self.mapp[r+1][c] != "*":
                            ind = self.rows * (r+1) + c
                            childs.append(ind)
                    if r - 1 > -1:
                        if self.mapp[r-1][c] != "*":
                            ind = self.rows * (r-1) + c
                            childs.append(ind)
                    if c + 1 < self.cols:
                        if self.mapp[r][c+1] != "*":
                            ind = self.rows * r + c + 1
                            childs.append(ind)
                    if c - 1 > -1:
                        if self.mapp[r][c-1] != "*":
                            ind = self.rows * r + c - 1
                            childs.append(ind)

                    newNode = Node(self.mapp[r][c], childs, (r, c), self.rows)
                    self.index_based_dict[(self.rows * r) + c] = newNode
                    self.childs_list.append(childs)


class UninformedSearch:
    def __init__(self, g: Graph):
        self.graphSize = g.rows * g.cols
        self.g = g

        self.frontierStart = [False for _ in range(self.graphSize)]
        self.frontierGoal = [False for _ in range(self.graphSize)]

        self.queueStart = []
        self.queueGoal = []

    def intersect(self):
        for i in range(self.g.rows * (self.g.rows-1) + (self.g.cols-1)):
            if self.frontierStart[i] and self.frontierGoal[i]:
                return i
        return -1

    def takeAction(self, pre: int, current: int):
        c0 = self.g.index_based_dict[pre].cordinate
        c1 = self.g.index_based_dict[current].cordinate
        if c0[0] - 1 == c1[0]:
            # return Action.UP
            return "UP"
        if c0[0] + 1 == c1[0]:
            # return Action.DOWN
            return "DOWN"
        if c0[1] - 1 == c1[1]:
            # return Action.LEFT
            return "LEFT"
        if c0[1] + 1 == c1[1]:
            # return Action.RIGHT
            return "RIGHT"

    def oneLayerBFS(self):
        tempQueue = []
        while len(self.queueStart) != 0:
            current = self.queueStart.pop(0)
            # self.frontierStart[current] = True
            children = self.g.index_based_dict[current].childs
            for child in children:
                if not self.frontierStart[child]:
                    tempQueue.append(child)
                    self.frontierStart[child] = True
                    self.g.index_based_dict[child].parentSrc = current
                    self.g.index_based_dict[child].actionSrc = self.takeAction(current, child)

        for item in tempQueue:
            self.queueStart.append(item)

        tempQueue = []
        while len(self.queueGoal) != 0:
            current = self.queueGoal.pop(0)
            # self.frontierGoal[current] = True
            children = self.g.index_based_dict[current].childs
            for child in children:
                if not self.frontierGoal[child]:
                    tempQueue.append(child)
                    self.frontierGoal[child] = True
                    self.g.index_based_dict[child].parentGoal = current
                    self.g.index_based_dict[child].actionGoal = self.takeAction(current, child)

        for item in tempQueue:
            self.queueGoal.append(item)

    def actReverse(self, act: Action):
        if act == "DOWN":
            # return Action.UP
            return "UP"
        if act == "UP":
            # return Action.DOWN
            return "DOWN"
        if act == "RIGHT":
            # return Action.LEFT
            return "LEFT"
        if act == "LEFT":
            # return Action.RIGHT
            return "RIGHT"

    def bidirectionalSearch(self, start: int, goal: int):
        self.frontierStart[start] = True
        self.frontierGoal[goal] = True

        self.queueStart.append(start)
        self.queueGoal.append(goal)

        intersect_index = self.intersect()
        print("intersect", intersect_index)
        while True:
            self.oneLayerBFS()
            intersect_index = self.intersect()
            if intersect_index != -1:
                break
        print("intersect", intersect_index)

        answer1 = []
        temp_it = intersect_index
        while temp_it != start:
            print(temp_it)
            answer1.insert(0, self.g.index_based_dict[temp_it].actionSrc)
            temp_it = self.g.index_based_dict[temp_it].parentSrc

        answer2 = []
        temp_it = intersect_index
        while temp_it != goal:
            print(temp_it)
            answer2.append(self.actReverse(self.g.index_based_dict[temp_it].actionGoal))
            temp_it = self.g.index_based_dict[temp_it].parentGoal

        answer = answer1 + answer2

        return answer


def findInAgents(turn_data: TurnData, x, y):
    for i in range(len(turn_data.agent_data)):
        if turn_data.agent_data[i].position[0] == x and turn_data.agent_data[i].position[1] == y:
            return i
    return -1


def printMap(turn_data: TurnData):
    for i in range(len(turn_data.map)):
        for j in range(len(turn_data.map[i])):
            found = findInAgents(turn_data, i, j)
            if found != -1:
                print(chr(ord('A') + found), end="")
            else:
                print(turn_data.map[i][j], end="")
        print()
    print(".....................")


class Agent(BaseAgent):
    def __init__(self):
        super().__init__()

    def do_turn(self, turn_data: TurnData) -> Action:
        printMap(turn_data)
        if self.boolCheck:
            agent_cordinate = turn_data.agent_data[0].position
            diamond_cordinate = ()
            for_break = False
            for r in range(len(turn_data.map)):
                for c in range(len(turn_data.map[r])):
                    if turn_data.map[r][c] == '1':
                        diamond_cordinate = (r, c)
                        for_break = True
                        break
                if for_break:
                    break
            g = Graph(len(turn_data.map), len(turn_data.map[0]), turn_data.map)
            g.fillChilds()
            algorithm = UninformedSearch(g)
            start = agent_cordinate[0] * len(turn_data.map) + agent_cordinate[1]
            print(diamond_cordinate)
            goal = diamond_cordinate[0] * len(turn_data.map) + diamond_cordinate[1]
            self.solution = algorithm.bidirectionalSearch(start, goal)
            print(self.solution)
            self.boolCheck = False
            act = self.solution.pop()
            if act == "DOWN":
                return Action.DOWN
            if act == "UP":
                return Action.UP
            if act == "RIGHT":
                return Action.RIGHT
            if act == "LEFT":
                return Action.LEFT

        else:
            if self.solution:
                act = self.solution.pop()
                if act == "DOWN":
                    return Action.DOWN
                if act == "UP":
                    return Action.UP
                if act == "RIGHT":
                    return Action.RIGHT
                if act == "LEFT":
                    return Action.LEFT
            else:
                return Action.UP


if __name__ == '__main__':
    winner = Agent().play()
    print("WINNER: " + winner)

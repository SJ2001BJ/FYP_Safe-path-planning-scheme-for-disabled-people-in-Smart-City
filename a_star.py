# a_star.py
import sys
import numpy as np
from map import MAP


class AStar:
    def __init__(self, map, heuristic_name):
        self.map = map
        self.open_set = []
        self.close_set = []
        self.start_point = None
        self.end_point = None
        self.heuristic_name = heuristic_name

    # 计算当前点的历史行驶距离
    def BaseCost(self, p):
        x_dis = abs(p.x - self.start_point.x)
        y_dis = abs(p.y - self.start_point.y)
        return x_dis + y_dis

    # 启发式函数-新
    def HeuristicCost(self, p):
        x_dis = abs(p.x - self.end_point.x)
        y_dis = abs(p.y - self.end_point.y)
        return min(x_dis, y_dis)

    # 启发式函数-曼哈顿距离
    def HeuristicCost_ManD(self, p):
        x_dis = abs(p.x - self.end_point.x)
        y_dis = abs(p.y - self.end_point.y)
        return x_dis + y_dis

    # 启发式函数-欧式距离
    def HeuristicCost_EucD(self, p):
        x_dis = abs(p.x - self.end_point.x) ** 2
        y_dis = abs(p.y - self.end_point.y) ** 2
        dis = np.sqrt(x_dis + y_dis)
        return dis

    # 启发式函数-切比雪夫距离
    def HeuristicCost_CheD(self, p):
        x_dis = abs(p.x - self.end_point.x)
        y_dis = abs(p.y - self.end_point.y)
        return max(x_dis, y_dis)

    # 启发式函数-对角线距离
    def HeuristicCost_DiaD(self, p):
        x_dis = abs(p.x - self.end_point.x)
        y_dis = abs(p.y - self.end_point.y)
        dis = np.sqrt(x_dis + y_dis)
        return dis

    # 启发式函数-加权曼哈顿距离
    def HeuristicCost_WManD(self, p):
        x_dis = 1.1 * abs(p.x - self.end_point.x)
        y_dis = 1.2 * abs(p.y - self.end_point.y)
        return max(x_dis, y_dis)

    # 启发式函数-加权欧式距离
    def HeuristicCost_WEucD(self, p):
        x_dis = 1.1 * abs(p.x - self.end_point.x) ** 2
        y_dis = 1.2 * abs(p.y - self.end_point.y) ** 2
        dis = np.sqrt(x_dis + y_dis)
        return dis

    # 总成本
    def TotalCost(self, p):
        # weight = p.weight * 10
        # if self.heuristic_name == "Hn":
        #     return self.BaseCost(p) + self.HeuristicCost(p) + weight
        # if self.heuristic_name == "Man":
        #     return self.BaseCost(p) + self.HeuristicCost_ManD(p) + weight
        # if self.heuristic_name == "Euc":
        #     return self.BaseCost(p) + self.HeuristicCost_EucD(p) + weight
        # if self.heuristic_name == "Che":
        #     return self.BaseCost(p) + self.HeuristicCost_CheD(p) + weight
        # if self.heuristic_name == "Dia":
        #     return self.BaseCost(p) + self.HeuristicCost_DiaD(p) + weight
        # if self.heuristic_name == "WMan":
        #     return self.BaseCost(p) + self.HeuristicCost_WManD(p) + weight
        # if self.heuristic_name == "WEuc":
        #     return self.BaseCost(p) + self.HeuristicCost_WEucD(p) + weight

        weight = p.weight * 10
        if self.heuristic_name == "Hn":
           # return p.area * 10 * (self.BaseCost(p) + self.HeuristicCost(p) + weight)   # 根据区域给节点赋予不同的权重,区域影响作为系数存在
           return self.BaseCost(p) + self.HeuristicCost(p) + weight + p.area * 10
        if self.heuristic_name == "Man":
            return self.BaseCost(p) + self.HeuristicCost_ManD(p) + weight
        if self.heuristic_name == "Euc":
            return self.BaseCost(p) + self.HeuristicCost_EucD(p) + weight + p.area * 10
        if self.heuristic_name == "Che":
            return self.BaseCost(p) + self.HeuristicCost_CheD(p) + weight + p.area * 10
        if self.heuristic_name == "Dia":
            return self.BaseCost(p) + self.HeuristicCost_DiaD(p) + weight + p.area * 10
        if self.heuristic_name == "WMan":
            return self.BaseCost(p) + self.HeuristicCost_WManD(p) + weight + p.area * 10
        if self.heuristic_name == "WEuc":
            return self.BaseCost(p) + self.HeuristicCost_WEucD(p) + weight + p.area * 10

    # 判断点是否有效
    def IsValidPoint(self, x, y):
        if x < 0 or y < 0 or x >= X_MAX_LEN or y >= Y_MAX_LEN:
            return False
        if self.map.IsObstacle(x, y):
            return False
        return True

    # 判断点是否在open-set
    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    # 判断点是否在open-set
    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    # 判断点是否在close-set
    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    def IsStartPoint(self, p):
        return p.x == self.start_point.x and p.y == self.start_point.y

    def IsEndPoint(self, p):
        return p.x == self.end_point.x and p.y == self.end_point.y

    #
    def ProcessPoint(self, x, y, parent):
        if not self.IsValidPoint(x, y):
            return  # Do nothing for invalid point
        p = self.map.point_list[x][y]
        if self.IsInCloseList(p):
            return  # Do nothing for visited point
        if not self.IsInOpenList(p):
            p.parent = parent
            p.cost = self.TotalCost(p)
            p.area = p.get_point_area() #获取节点区域
            self.open_set.append(p)

    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = self.TotalCost(p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    # 获取求得路径
    def BuildPath(self, p):
        path = []
        while True:
            path.insert(0, (p.x, p.y))  # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        return path

    def set_start_point(self, x, y):
        if self.map.point_list[x][y].is_barrier:
            print("出发点和到达点请从以下列表中选择:")
            point_list = []
            for i in range(self.map.x_len):
                for j in range(self.map.y_len):
                    if self.map.point_list[i][j].is_barrier:
                        continue
                    point_list.append([i, j])
            print(point_list)
            assert False
        self.start_point = self.map.point_list[x][y]

    def set_end_point(self, x, y):
        if self.map.point_list[x][y].is_barrier:
            print("出发点和到达点请从以下列表中选择:")
            point_list = []
            for i in range(self.map.x_len):
                for j in range(self.map.y_len):
                    if self.map.point_list[i][j].is_barrier:
                        continue
                    point_list.append([i, j])
            print(point_list)
            assert False
        self.end_point = self.map.point_list[x][y]

    # 路径规划主入口
    def find_one_path(self):
        self.open_set = []
        self.close_set = []

        self.open_set.append(self.start_point)
        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return
            p = self.open_set[index]

            if self.IsEndPoint(p):
                return self.BuildPath(p)

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            # 4 adjacency search
            for step in [[0, 1], [0, -1],
                         [1, 0], [-1, 0]]:
            # # 8 adjacency search
            # for step in [[0, 1], [0, -1],
            #              [1, 0], [-1, 0],
            #              [1, 1], [-1, -1],
            #              [1, -1], [-1, 1]]:
            # 16 adjacency search
            # for step in [[0, 1], [0, -1],
            #              [1, 0], [-1, 0],
            #              [1, 1], [-1, -1],
            #              [1, -1], [-1, 1],
            #              [2, 1], [-2, -1],  # add 8 new direction
            #              [2, -1], [-2, 1],
            #              [1, 2], [-1, -2],
            #              [-1, 2], [1, -2]]:

                self.ProcessPoint(x + step[0], y + step[1], p)

    def check_path(self, one_path):
        for point in one_path:
            if self.map.point_list[point[0]][point[1]].is_barrier:
                print(point)
                return False
        return True


if __name__ == "__main__":
    # 地图最大长度，宽度
    X_MAX_LEN = 20
    Y_MAX_LEN = 20
    map_handle = MAP(x_len=X_MAX_LEN, y_len=Y_MAX_LEN)

    # 设置障碍点以及权重
    # for x in range(3, 11):
    #     map_handle.add_barrier_point(x, 10, 5)
    #     map_handle.add_barrier_point(10, x, 5)
    map_handle.add_barrier_point(16, 8, 2)
    map_handle.add_barrier_point(8, 10, 0)
    map_handle.add_barrier_point(11, 3, 1)
    map_handle.add_barrier_point(7, 9, 3)
    map_handle.add_barrier_point(12, 1, 5)
    map_handle.add_barrier_point(18, 9, 0)
    map_handle.add_barrier_point(4, 5, 3)
    map_handle.add_barrier_point(7, 8, 3)
    map_handle.add_barrier_point(8, 15, 2)
    map_handle.add_barrier_point(10, 14, 3)
    map_handle.add_barrier_point(17, 16, 0)
    map_handle.update_barrier_round()
    # 遍历所有的启发式方法
    for name in ['Hn', 'Man', 'Euc', 'Che', 'Dia', 'WMan', 'WEuc']:
        astar_handle = AStar(map=map_handle, heuristic_name='Hn')
        # astar_handle = AStar(map=map_handle, heuristic_name='Man')
        # astar_handle = AStar(map=map_handle, heuristic_name='Euc')
        # astar_handle = AStar(map=map_handle, heuristic_name='Che')
        # astar_handle = AStar(map=map_handle, heuristic_name='Dia')
        # 设置起点 终点
        start_point = [0, 1]
        end_point = [17, 12]
        astar_handle.set_start_point(start_point[0], start_point[1])
        astar_handle.set_end_point(end_point[0], end_point[1])
        map_handle.add_start_point(start_point[1], start_point[0])
        map_handle.add_end_point(end_point[1], end_point[0])
        # 计算路径
        one_path = astar_handle.find_one_path()
        assert astar_handle.check_path(one_path)
        print("Heuristic name:", 'Hn', "path len:", len(one_path))
        # print("Heuristic name:", 'Man', "path len:", len(one_path))
        # print("Heuristic name:", 'Euc', "path len:", len(one_path))
        # print("Heuristic name:", 'Che', "path len:", len(one_path))
        # print("Heuristic name:", 'Dia', "path len:", len(one_path))
        print(one_path)
        # 画图
        map_handle.add_path(one_path)
        map_handle.plot(_name='Hn')
        # map_handle.plot(_name='Man')
        # map_handle.plot(_name='Euc')
        # map_handle.plot(_name='Che')
        # map_handle.plot(_name='Dia')
        break

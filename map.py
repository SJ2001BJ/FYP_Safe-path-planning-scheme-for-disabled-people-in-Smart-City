from point import Point
import numpy as np
np.random.seed(2022)


class MAP:
    def __init__(self, x_len, y_len):
        self.x_len = x_len
        self.y_len = y_len
        self.point_list = [[Point(j, i) for i in range(y_len)] for j in range(x_len)]
        self.map_grid = np.ones((x_len, y_len), dtype=int) * 10


    def IsObstacle(self, x, y):
        return self.point_list[x][y].is_barrier

    def random_barrier(self, rate=0.1):
        barrier_point_num = int(self.x_len * self.y_len * rate)
        cur_num = 0
        while cur_num < barrier_point_num:
            x = np.random.randint(0, self.x_len)
            y = np.random.randint(0, self.y_len)
            self.point_list[x][y].is_barrier = True
            cur_num += 1
            self.map_grid[x][y] = 0

    def round_point(self, x, y, weight):
        _weight = weight
        idx = 1
        while _weight > 0:
            if 0 <= x - idx < self.x_len:
                if not self.point_list[x - idx][y].is_barrier:
                    self.point_list[x - idx][y].weight += weight - idx
            if 0 <= x + idx < self.x_len:
                if not self.point_list[x + idx][y].is_barrier:
                    self.point_list[x + idx][y].weight += weight - idx
            if 0 <= y + idx < self.x_len:
                if not self.point_list[x][y + idx].is_barrier:
                    self.point_list[x][y + idx].weight += weight - idx
            if 0 <= y - idx < self.x_len:
                if not self.point_list[x][y - idx].is_barrier:
                    self.point_list[x][y - idx].weight += weight - idx
            if 0 <= x - idx < self.x_len and 0 <= y - idx < self.x_len:
                if not self.point_list[x - idx][y - idx].is_barrier:
                    self.point_list[x - idx][y - idx].weight += weight - idx
            if 0 <= x - idx < self.x_len and 0 <= y + idx < self.x_len:
                if not self.point_list[x - idx][y + idx].is_barrier:
                    self.point_list[x - idx][y + idx].weight += weight - idx
            if 0 <= x + idx < self.x_len and 0 <= y - idx < self.x_len:
                if not self.point_list[x + idx][y - idx].is_barrier:
                    self.point_list[x + idx][y - idx].weight += weight - idx
            if 0 <= x + idx < self.x_len and 0 <= y + idx < self.x_len:
                if not self.point_list[x + idx][y + idx].is_barrier:
                    self.point_list[x + idx][y + idx].weight += weight - idx
            _weight -= 1
            idx += 1

    def add_barrier_point(self, x, y, weight):
        self.point_list[x][y].is_barrier = True
        self.map_grid[x][y] = 0
        self.point_list[x][y].weight = weight

    def update_barrier_round(self):
        for i in range(self.x_len):
            for j in range(self.y_len):
                if self.point_list[i][j].is_barrier:
                    self.round_point(i, j, self.point_list[i][j].weight)

    def add_start_point(self, x, y):
        self.map_grid[y][x] = 5

    def add_end_point(self, x, y):
        self.map_grid[y][x] = 5

    def add_path(self, path):
        for p in path[1:-1]:
            self.map_grid[p[0]][p[1]] = 3

    def plot(self, _name):
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(10, 10))
        plt.imshow(self.map_grid.T,
                   cmap=plt.cm.viridis,
                   interpolation='nearest',
                   vmin=0, vmax=10,
                   aspect='auto')
        plt.xlim(-1, self.x_len)  # 设置x轴范围
        plt.ylim(-1, self.y_len)  # 设置y轴范围
        my_x_ticks = np.arange(0, self.x_len, 1)
        my_y_ticks = np.arange(0, self.y_len, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)
        plt.savefig("{}.png".format(_name), dpi=300)
        plt.show()
        plt.close()




if __name__ == "__main__":
    map_handle = MAP(x_len=20, y_len=20)
    for x in range(3, 11):
        map_handle.add_barrier_point(x, 10)
        map_handle.add_barrier_point(10, x)
    map_handle.add_end_point(18, 18)
    map_handle.add_end_point(7, 8)
    map_handle.plot()
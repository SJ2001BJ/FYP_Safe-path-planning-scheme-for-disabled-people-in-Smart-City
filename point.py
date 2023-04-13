class Point:
    def __init__(self, x, y, weight=0, is_barrier=False):
        self.x = x
        self.y = y
        self.cost = 0
        self.parent = None
        self.weight = weight
        self.is_barrier = is_barrier
        self.area = self.get_point_area()   #增加一个属性表示节点所在的区域
        self.color = None
    def get_point_area(self):
        """
        根据坐标范围划分不同的区域，并为每个区域分配不同的权重
        """
        if self.x < 10 and self.y < 10:
            return 1
        elif self.x < 10 and self.y >= 10:
            return 9
        elif self.x >= 10 and self.y < 10:
            return 0.5
        else:
            return 0.2


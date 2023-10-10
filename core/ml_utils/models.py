class BoundingBox:
    def __init__(self, *res):
        self.x1, self.y1, self.x2, self.y2 = (
            int(res[0]),
            int(res[1]),
            int(res[2]),
            int(res[3]),
        )
        self.cen_x = int((self.x1 + self.x2) / 2)
        self.cen_y = int((self.y1 + self.y2) / 2)
        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1
        self.prob = res[4]
        self.label = res[5]
        self.area = self.w * self.h

    def display(self):
        print(f"Bounding box is [{self.x1}, {self.y1}, {self.x2}, {self.y2}]")
        print(f"Label is {self.label}")
        # print(f'Probability is {self.prob}')


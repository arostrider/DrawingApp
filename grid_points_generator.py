class GridPointsGenerator:
    X, Y = 0, 1

    def __init__(self, height, width, step_x, step_y):
        self.height = height
        self.width = width
        self.step_x = step_x
        self.step_y = step_y

        self.n_columns = int(self.width // self.step_x)
        self.n_rows = int(self.height // self.step_y)

    def __call__(self):
        for x in range(0, self.n_columns):
            for y in range(0, self.n_rows):
                yield x, y

    def generate_W_border_points(self):
        x = 0
        for y in range(0, self.height, self.step_y):
            yield x, y

    def generate_E_border_points(self):
        x = self.width
        for y in range(0, self.height, self.step_y):
            yield x, y

    def generate_N_border_points(self):
        y = 0
        for x in range(0, self.width, self.step_x):
            yield x, y

    def generate_S_border_points(self):
        y = self.height
        for x in range(0, self.width, self.step_x):
            yield x, y


if __name__ == '__main__':
    grid = GridPointsGenerator(100, 100, 0.5, 0.5)
    count = 0
    for point in grid():
        print(point)
        count += 1
    print(f'N of points from generator: {count}')

    print('W border points')
    print(grid.get_N_border_points())
    print(grid.get_S_border_points())

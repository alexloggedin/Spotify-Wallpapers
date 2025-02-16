import numpy as np
import random
import matplotlib.pyplot as plt

class Sampler():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_valid_point(self, grid, cellsize, gwidth, gheight, p, radius):
        if p[0] < 0 or p[0] >= self.width or p[1] < 0 or p[1] >= self.height:
            return False

        xindex = int(np.floor(p[0] / cellsize))
        yindex = int(np.floor(p[1] / cellsize))
        i0 = max(xindex - 1, 0)
        i1 = min(xindex + 1, gwidth - 1)
        j0 = max(yindex - 1, 0)
        j1 = min(yindex + 1, gheight - 1)

        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                if grid[i, j] is not None:
                    if np.linalg.norm(grid[i, j] - p) < radius:
                        return False

        return True

    def insert_point(self, grid, cellsize, point):
        xindex = int(np.floor(point[0] / cellsize))
        yindex = int(np.floor(point[1] / cellsize))
        grid[xindex, yindex] = point

    def sample(self, radius, k):
        N = 2
        points = []
        active = []
        p0 = np.array([random.uniform(0, self.width), random.uniform(0, self.height)])
        cellsize = np.floor(radius / np.sqrt(N))

        ncells_width = int(np.ceil(self.width / cellsize)) + 1
        ncells_height = int(np.ceil(self.height / cellsize)) + 1

        grid = np.full((ncells_width, ncells_height), None)

        self.insert_point(grid, cellsize, p0)
        points.append(p0)
        active.append(p0)

        while active:
            random_index = random.randint(0, len(active) - 1)
            p = active[random_index]

            found = False
            for tries in range(k):
                theta = random.uniform(0, 360)
                new_radius = random.uniform(radius, 2 * radius)
                pnew = np.array([p[0] + new_radius * np.cos(np.radians(theta)),
                                p[1] + new_radius * np.sin(np.radians(theta))])

                if not self.is_valid_point(grid, cellsize, ncells_width, ncells_height, pnew, radius):
                    continue

                points.append(pnew)
                self.insert_point(grid, cellsize, pnew)
                active.append(pnew)
                found = True
                break

            if not found:
                active.pop(random_index)

        return points


def test():
    width = 3000
    height = 2000
    s = Sampler(width, height)
    result = s.sample(180, 30)
    print(result)

    # Extract x and y coordinates from the points
    x_coords = [point[0] for point in result]
    y_coords = [point[1] for point in result]

    colors = np.random.rand(len(result), 3)

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the points as squares
    ax.scatter(x_coords, y_coords, s=32, c=colors, marker='s', edgecolors='black', linewidths=1)

    ax.set_title('Poisson Disk Sampling with Squares')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    plt.show()
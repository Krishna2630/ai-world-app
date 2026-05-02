import numpy as np

# smoothing function
def smooth(heightmap, iterations=3):
    for _ in range(iterations):
        heightmap = (
            np.roll(heightmap, 1, axis=0) +
            np.roll(heightmap, -1, axis=0) +
            np.roll(heightmap, 1, axis=1) +
            np.roll(heightmap, -1, axis=1) +
            heightmap
        ) / 5
    return heightmap


def generate_world(params):
    size = 64

    # base noise
    small = np.random.rand(size, size)
    small = smooth(small, 4)

    # large terrain shape
    large = np.random.rand(size, size)
    large = smooth(large, 8)

    # combine
    heightmap = 0.7 * small + 0.3 * large

    # normalize
    heightmap = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min())

    # objects
    trees, rocks, houses = [], [], []

    for _ in range(int(100 * abs(params["tree_density"]))):
        x, y = np.random.randint(0, size, 2)
        if heightmap[y][x] > 0.4:
            trees.append({"x": int(x), "y": int(y)})

    for _ in range(int(80 * abs(params["rock_density"]))):
        x, y = np.random.randint(0, size, 2)
        if heightmap[y][x] > 0.6:
            rocks.append({"x": int(x), "y": int(y)})

    for _ in range(int(10 * abs(params["house_density"]))):
        x, y = np.random.randint(0, size, 2)
        if 0.4 < heightmap[y][x] < 0.6:
            houses.append({"x": int(x), "y": int(y)})

    return {
        "heightmap": heightmap.tolist(),
        "trees": trees,
        "rocks": rocks,
        "houses": houses
    }
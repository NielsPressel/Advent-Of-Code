import os
import re
import numpy as np
from dataclasses import dataclass
from typing import NamedTuple


class Vector3D(NamedTuple):
    x: int
    y: int
    z: int

    def to_vector(self):
        return np.array([self.x, self.y, self.z], dtype=np.int64)


@dataclass
class Trajectory:
    position: Vector3D
    velocity: Vector3D

    def to_vectors(self):
        return self.position.to_vector(), self.velocity.to_vector()


def parse(line: str):
    regex = r"([-]?\d+),\s+([-]?\d+),\s+([-]?\d+)\s+@\s+([-]?\d+),\s+([-]?\d+),\s+([-]?\d+)"
    pattern = re.compile(regex)
    match = pattern.match(line)

    return Trajectory(Vector3D(int(match.group(1)), int(match.group(2)), int(match.group(3))), Vector3D(int(match.group(4)), int(match.group(5)), int(match.group(6))))


def intersect(t1: Trajectory, t2: Trajectory) -> bool:
    min_range = 200_000_000_000_000
    max_range = 400_000_000_000_000

    a = np.array([[t1.velocity.x, -t2.velocity.x],
                 [t1.velocity.y, -t2.velocity.y]])
    b = np.array([t2.position.x - t1.position.x,
                 t2.position.y - t1.position.y])

    if np.linalg.matrix_rank(a) < 2:
        return False

    time = np.linalg.solve(a, b)
    if time[0] < 0 or time[1] < 0:
        return False

    position = np.array([t1.position.x, t1.position.y]) + \
        time[0] * np.array([t1.velocity.x, t1.velocity.y])

    return min_range <= position[0] <= max_range and min_range <= position[1] <= max_range


def cross_matrix(vector):
    return np.array([[0, -vector[2], vector[1]], [vector[2], 0, -vector[0]], [-vector[1], vector[0], 0]], dtype=np.int64)


def solve_system(trajectories: list[Trajectory]):
    p0, v0 = trajectories[0].to_vectors()
    p1, v1 = trajectories[1].to_vectors()
    p2, v2 = trajectories[2].to_vectors()

    c1 = -np.cross(p0, v0) + np.cross(p1, v1)
    c2 = -np.cross(p0, v0) + np.cross(p2, v2)

    b1 = cross_matrix(v0) - cross_matrix(v1)
    b2 = cross_matrix(v0) - cross_matrix(v2)
    b3 = -cross_matrix(p0) + cross_matrix(p1)
    b4 = -cross_matrix(p0) + cross_matrix(p2)

    b5 = np.concatenate((b1, b2), axis=0)
    b6 = np.concatenate((b3, b4), axis=0)

    vec = np.concatenate((c1, c2), axis=None)
    mat = np.concatenate((b5, b6), axis=1)
    result = np.linalg.solve(mat, vec)

    return int(np.ceil(result[0] + result[1] + result[2]))


input_text = []

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(f"{dir_path}/input.txt", "r") as f:
    input_text = f.readlines()

input_text = list(map(lambda x: x.replace("\n", ""), input_text))

trajectories = []
for line in input_text:
    trajectories.append(parse(line))


count = 0
for i, t1 in enumerate(trajectories):
    for j, t2 in enumerate(trajectories):
        if i < j:
            if intersect(t1, t2):
                count += 1

print(f"Answer first part: {count}")
print(f"Answer second part: {solve_system(trajectories)}")

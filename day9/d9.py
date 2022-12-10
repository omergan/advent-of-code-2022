from dataclasses import dataclass
from math import copysign
from pathlib import Path
input_file = Path('input.txt').read_text()
commands = input_file.split('\n')

directions = {
    "R" : (1, 0),
    "L" : (-1, 0),
    "U" : (0, 1),
    "D" : (0, -1)
}

SIZE = 10

@dataclass
class Knot:
    id: int
    x: int = 0
    y: int = 0

    def increment(self, direction: tuple):
        self.x += direction[0]
        self.y += direction[1]

knots = [Knot(id=x) for x in range(SIZE)];
visited = set()

def update(head: Knot, tail:Knot) -> Knot:
    move_y = max(abs(head.y - tail.y) - 1, 0)
    move_x = max(abs(head.x - tail.x) - 1, 0)
    move = max(move_y, move_x)
        
    tail.y += copysign(move, head.y - tail.y) if head.y != tail.y else 0
    tail.x += copysign(move, head.x - tail.x) if head.x != tail.x else 0

    visited.add((tail.x, tail.y) if tail.id == SIZE-1 else (0,0))
    return Knot(id=tail.id, x=tail.x, y=tail.y)

def simulate()-> int:
    for c in commands:
        direction, steps = tuple(c.split(" "))
        steps = int(steps)
        for _ in range(steps):
            knots[0].increment(directions[direction])
            for i in range(1, SIZE):
                knots[i] = update(knots[i-1], knots[i])
    return len(visited)

if __name__ == '__main__':
    print(simulate())

from __future__ import annotations

import vector as v
from typing import List, Hashable, Callable, Tuple, TypeVar, Union


colour = Tuple[int, int, int]
ball_state = Tuple[Union[v.Vector2, v.Vector3], colour]


class DataStoringObject:
    T = TypeVar("T")

    def __init__(self):
        self.data = {}

    def set_data(self, *dat):
        for d in range(len(dat) // 2):
            self.data[dat[d * 2]] = dat[(d * 2) + 1]

    def mod_data(self, dat: Hashable, f: Callable[[T], T]):
        self.data[dat] = f(self.data[dat])

    def get_data(self, dat: Hashable):
        return self.data[dat]


class Ball(DataStoringObject):
    def __init__(self, start_pos: v.Vector2, start_col: colour,
                 move_function: Callable[[Board, Ball], ball_state]):
        super().__init__()

        self.board = None

        self.start_pos = start_pos
        self.start_col = start_col
        self.move_function = move_function

        self.pos, self.col = self.start_pos, self.start_col

        self.reset()

    def set_board(self, board: Board):
        self.board = board

    def serialize(self) -> ball_state:
        return self.pos, self.col

    def reset(self):
        self.pos = self.start_pos
        self.col = self.start_col
        self.data = {}

    def step(self):
        self.pos, self.col = self.move_function(self.board, self)


class Board(DataStoringObject):
    def __init__(self, dimensions: v.Vector2, balls: List[Ball]):
        super().__init__()

        self.dimensions = dimensions
        self.balls = balls
        self.link_balls()

    def link_balls(self):
        for ball in self.balls:
            ball.board = self

    def serialize(self) -> List[ball_state]:
        return [
            ball.serialize() for ball in self.balls
        ]

    def reset(self):
        for ball in self.balls:
            ball.reset()

    def step(self):
        for ball in self.balls:
            ball.step()

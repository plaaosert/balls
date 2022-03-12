# avoidance, with a moving bar of balls to show reaction better

import math
import random

from balls import render, data, vector


def move_down(board: data.Board, ball: data.Ball) -> data.ball_state:
    return ball.pos + vector.Vector2(0, 2), ball.col


def move_away(board: data.Board, ball: data.Ball) -> data.ball_state:
    # closeness = sum(
    #     (b.pos - ball.pos).magnitude() for b in board.balls
    # ) / len(board.balls)

    farness_sum = 0
    balls_positions = [0, 0, 0, 0]  # [up, right, down, left]
    for ball_other in balls:
        diff = ball_other.pos - ball.pos

        farness_sum += (diff.magnitude() / 1.5)
        if abs(diff.x) > abs(diff.y):
            if diff.x > 0:
                balls_positions[1] += int((board.dimensions.x / 8) / diff.magnitude())
            elif diff.x < 0:
                balls_positions[3] += int((board.dimensions.x / 8) / diff.magnitude())
        else:
            if diff.y > 0:
                balls_positions[2] += int((board.dimensions.y / 8) / diff.magnitude())
            elif diff.y < 0:
                balls_positions[0] += int((board.dimensions.y / 8) / diff.magnitude())

    closeness = (farness_sum / len(board.balls))

    # reduce chance of moving off the board
    if ball.pos.x > (board.dimensions.x / 2):  # right
        # reduce the chance of moving right (the left count) based on the proximity to the right edge
        balls_positions[3] = int(round(
            balls_positions[3] * ((board.dimensions.x - ball.pos.x) / (board.dimensions.x / 2))
        ))
    elif ball.pos.x < (board.dimensions.x / 2):  # left
        # reduce the chance of moving left (the right count) based on the proximity to the left edge
        balls_positions[1] = int(round(
            balls_positions[1] * (ball.pos.x / (board.dimensions.x / 2))
        ))

    if ball.pos.y > (board.dimensions.y / 2):  # down
        balls_positions[0] = int(round(
            balls_positions[0] * ((board.dimensions.y - ball.pos.y) / (board.dimensions.y / 2))
        ))
    elif ball.pos.y < (board.dimensions.y / 2):  # up
        balls_positions[2] = int(round(
            balls_positions[2] * (ball.pos.y / (board.dimensions.y / 2))
        ))

    if sum(balls_positions) <= 1:
        movement_choice = random.randint(0, 3)
    else:
        movement_choice = random.choice((
            *(0 for _ in range(balls_positions[0])),
            *(1 for _ in range(balls_positions[1])),
            *(2 for _ in range(balls_positions[2])),
            *(3 for _ in range(balls_positions[3]))
        ))

    movement = (
        vector.Vector2(0, 1), vector.Vector2(-1, 0), vector.Vector2(0, -1), vector.Vector2(1, 0)
    )[movement_choice] * 4

    position = ball.pos + movement

    return position, (255 - min(255, max(0, int(closeness))), min(255, max(0, int(closeness))), 64)


balls = [
    data.Ball(vector.Vector2(0, 0), (255, 0, 0), move_away) for i in range(120)
]

for index, ball in enumerate(balls):
    ball.pos = vector.Vector2(400 + random.randint(-1, 1), 400 + random.randint(-1, 1))


balls.extend([
    data.Ball(vector.Vector2(x, 16), (255, 255, 255), move_down) for x in range(2, 800, 2)
])


board = data.Board(vector.Vector2(800, 800), balls)

render.draw_frames(board, 4, "out.gif", 500)
render.redraw_frames("out.mp4", 500, 60)

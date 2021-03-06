# ball pendulum. set of 60 balls moving at different speeds, the further ones moving faster. creates chaotic motion

import math

from balls import render, data, vector


def successor_angle(board: data.Board, ball: data.Ball) -> data.ball_state:
    angle_current = ball.get_data("angle")
    direction = ball.get_data("direction")
    radius = ball.get_data("radius")
    origin = ball.get_data("origin")

    angle_next = angle_current + (ball.get_data("speed") * direction)
    if angle_next >= 135:
        angle_next = 135 - (angle_next - 135)
        direction *= -1
    elif angle_next <= 45:
        angle_next = 45 + (45 - angle_next)
        direction *= -1

    ball.set_data("angle", angle_next, "direction", direction)

    position = vector.Vector2(
        int(radius * math.cos(math.radians(angle_next)) + origin.x),
        int(radius * math.sin(math.radians(angle_next)) + origin.y)
    )

    return position, (255 - int(5 * abs(90 - angle_next)), int(5 * abs(90 - angle_next)), 4 * ball.get_data("index"))


balls = [
    data.Ball(vector.Vector2(0, 0), (255, 0, 0), successor_angle) for i in range(60)
]

for index, ball in enumerate(balls):
    ball.pos = vector.Vector2(400, 600 - 32 - (index * 8))

    ball.set_data(
        "angle", 90,
        "origin", vector.Vector2(400, 600),
        "speed", 1 + (0.1 * index),
        "radius", -32 - (index * 8),
        "direction", 1,
        "index", index
    )


board = data.Board(vector.Vector2(800, 800), balls)

render.draw_frames(board, 4, "out.mp4", 1000)

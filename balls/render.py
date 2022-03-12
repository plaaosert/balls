from typing import List
from PIL import Image, ImageDraw
import os
import shutil
import imageio

import data
from vector import Vector2


def draw_balls(dimensions: Vector2, ball_info: List[data.ball_state], ball_size: int, fname: str):
    img_base = Image.new("RGB", (dimensions.x, dimensions.y), (0, 0, 0, 255))

    draw = ImageDraw.Draw(img_base, "RGBA")
    for ball in ball_info:
        draw.ellipse(
            ((ball[0].x - ball_size, ball[0].y - ball_size), (ball[0].x + ball_size, ball[0].y + ball_size)),
            fill=(*ball[1], 255), outline=(0, 0, 0, 255)
        )

    img_base.save(fname)


def stitch_frames(folder: str, delay: float, length: int, out_path: str):
    images = []
    for f_id in range(length):
        images.append(imageio.imread(os.path.join(folder, "frame_{}.png".format(f_id))))

    imageio.mimsave(out_path, images, duration=delay)


def draw_frames(board: data.Board, ball_size: int, fname: str, num_frames: int):
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")

    os.mkdir("tmp")

    for i in range(num_frames):
        draw_balls(board.dimensions, board.serialize(), ball_size, os.path.join("tmp", "frame_{}.png".format(i)))
        board.step()

    if fname.endswith(".gif"):
        stitch_frames("tmp", 1 / 24, num_frames, fname)
    else:
        os.system("ffmpeg -r 24 -i frame_%01d.png -vcodec h264 -y {}".format(fname))

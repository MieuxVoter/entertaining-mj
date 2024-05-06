import numpy as np
from manim import (
    Rectangle,
    RIGHT,
    LEFT,
    Transform,
)
from manim.utils.rate_functions import linear


class StretchRectangleRightObjects:

    def __init__(self, width, x_location, y_location, color):
        self.width = width
        self.color = color
        self.x_location = x_location
        self.y_location = y_location
        self.default_height = 1
        self._original_rect = (
            Rectangle(
                width=0,
                height=self.default_height,
                color=self.color,
                fill_color=self.color,
                fill_opacity=1,
            )
            .to_edge(LEFT)
            .shift(np.array((self.x_location, self.y_location, 0)))
        )

        self._stretched_rect = (
            Rectangle(
                width=self.original_rect.width + self.width,
                height=self.default_height,
                color=self.color,
                fill_color=self.color,
                fill_opacity=1,
            )
            .to_edge(LEFT)
            .shift(np.array((self.x_location, self.y_location, 0)))
        )

    @property
    def original_rect(self) -> Rectangle:
        return self._original_rect

    @property
    def stretched_rect(self) -> Rectangle:
        return self._stretched_rect

    @property
    def stretch(self) -> Transform:
        return Transform(self.original_rect, self.stretched_rect)


class NextToStretchRectangleRightObjects:

    def __init__(self, width, color, object_to_next_to, direction=RIGHT, buffer=0.25):
        self.width = width
        self.color = color
        self.object_to_next_to = object_to_next_to
        self.direction = direction
        self.default_height = 0.75
        self.buffer = buffer
        self._original_rect = Rectangle(
            width=0,
            height=self.default_height,
            color=self.color,
            fill_color=self.color,
            fill_opacity=1,
        ).next_to(self.object_to_next_to, self.direction, buff=self.buffer)

        self._stretched_rect = Rectangle(
            width=self.original_rect.width + self.width,
            height=self.default_height,
            color=self.color,
            fill_color=self.color,
            fill_opacity=1,
        ).next_to(self.object_to_next_to, self.direction, buff=self.buffer)

    @property
    def original_rect(self) -> Rectangle:
        return self._original_rect

    @property
    def stretched_rect(self) -> Rectangle:
        return self._stretched_rect

    def stretch(self, ratefunc=linear) -> Transform:
        return Transform(self.original_rect, self.stretched_rect, rate_func=ratefunc)

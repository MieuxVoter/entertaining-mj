from manim import (
    Scene,
    Square,
    BLUE,
    ORANGE,
    Rectangle,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    Transform,
    ImageMobject,
    VGroup,
    FadeIn,
    ORIGIN,
    Text,
    Group,
    Circle,
)
from color_utils import get_colors
import numpy as np
from jm_constant import DEFAULT_VOTE, EASY_VOTE, SAME_REJECT_VOTE_AGAIN
from candidate import CandidateManim, CandidateCharacteristics, CandidateManimList
from manim.utils.rate_functions import there_and_back, linear


class StretchRectangleRightObjects:

    def __init__(self, width, x_location, y_location, color):
        self.width = width
        self.color = color
        self.x_location = x_location
        self.y_location = y_location
        self.default_height = 1

    @property
    def original_rect(self) -> Rectangle:
        return (
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

    @property
    def stretched_rect(self) -> Rectangle:
        new_width = self.original_rect.width + self.width
        stretched_rect = (
            Rectangle(
                width=new_width,
                height=self.default_height,
                color=self.color,
                fill_color=self.color,
                fill_opacity=1,
            )
            .to_edge(LEFT)
            .shift(np.array((self.x_location, self.y_location, 0)))
        )
        return stretched_rect

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

    @property
    def original_rect(self) -> Rectangle:
        return Rectangle(
            width=0,
            height=self.default_height,
            color=self.color,
            fill_color=self.color,
            fill_opacity=1,
        ).next_to(self.object_to_next_to, self.direction, buff=self.buffer)

    @property
    def stretched_rect(self) -> Rectangle:
        new_width = self.original_rect.width + self.width
        stretched_rect = Rectangle(
            width=new_width,
            height=self.default_height,
            color=self.color,
            fill_color=self.color,
            fill_opacity=1,
        ).next_to(self.object_to_next_to, self.direction, buff=self.buffer)
        return stretched_rect

    def stretch(self, ratefunc=linear) -> Transform:
        return Transform(self.original_rect, self.stretched_rect, rate_func=ratefunc)

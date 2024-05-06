from manim import (
    Scene,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    ImageMobject,
    FadeIn,
    Text,
    FadeOut,
    BLUE,
    RED,
    Rectangle,
    Group,
    Create,
    Transform,
)

from color_utils import get_colors
from jm_constant import DEFAULT_VOTE
from streched_rectangles import StretchRectangleRightObjects


class StackBarDisplay(Scene):

    def construct(self):
        colors = get_colors(DEFAULT_VOTE.nb_grades)

        for i in range(DEFAULT_VOTE.nb_grades):
            rect = StretchRectangleRightObjects(
                width=DEFAULT_VOTE["marcel"][i] / 10,
                x_location=DEFAULT_VOTE.cumulative_results()["marcel"][i] / 10,
                y_location=0,
                color=colors[i],
            )
            self.play(rect.stretch)

        self.wait()


class StackBarDisplayAndFadeOut(Scene):

    def construct(self):
        colors = get_colors(DEFAULT_VOTE.nb_grades)

        rectangles = []
        for i in range(DEFAULT_VOTE.nb_grades):
            rect = StretchRectangleRightObjects(
                width=DEFAULT_VOTE["marcel"][i] / 10,
                x_location=DEFAULT_VOTE.cumulative_results()["marcel"][i] / 10,
                y_location=0,
                color=colors[i],
            )
            rectangles.append(rect)
            self.play(rect.stretch)

        for rect in rectangles:
            self.play(FadeOut(rect.original_rect))

        self.wait()


class StackBarDisplayAndFadOut(Scene):

    def construct(self):
        colors = get_colors(DEFAULT_VOTE.nb_grades)

        rect = Rectangle(width=2, height=1, color=BLUE)

        # Add the rectangle to the scene
        self.play(Create(rect))

        # Create a stretched rectangle
        stretched_rect = Rectangle(width=4, height=1, color=RED)

        # Transform the original rectangle into the stretched rectangle
        self.play(Transform(rect, stretched_rect))

        # Fade out the rectangle
        self.play(FadeOut(rect))

        self.wait()


class StackTogether(Scene):

    def construct(self):
        colors = get_colors(DEFAULT_VOTE.nb_grades)

        vertical_step = 2
        vertical_offset = vertical_step * DEFAULT_VOTE.nb_candidates / 2

        for i in range(DEFAULT_VOTE.nb_grades):
            rectangles = []
            for num, candidate in enumerate(DEFAULT_VOTE.candidates):
                rectangles.append(
                    StretchRectangleRightObjects(
                        width=DEFAULT_VOTE[candidate][i] / 10,
                        x_location=DEFAULT_VOTE.cumulative_results()[candidate][i] / 10,
                        y_location=num * vertical_step - vertical_offset,
                        color=colors[i],
                    )
                )
            self.play(*[rect.stretch for rect in rectangles])

        self.wait()


class PresentCandidates(Scene):
    """
    Present the candidates.
    """

    def construct(self):

        image_spacing = 0.5
        text_offset = 0.25
        fontsize = 12
        scale = 1

        images = [
            ImageMobject("image126.png"),
            ImageMobject("image126.png"),
            ImageMobject("image126.png"),
        ]

        names = [
            Text("Michel \n Dupont", font_size=fontsize),
            Text("Marcel \n Champlain", font_size=fontsize),
            Text("Rosalie \n Dupuis", font_size=fontsize),
        ]

        is_number_of_images_uneven = len(images) % 2 != 0

        for image in images:
            image.scale(scale)

        if is_number_of_images_uneven:
            images_left = images[: len(images) // 2]
            flipped_images_left = images_left[::-1]
            images_right = images[len(images) // 2 + 1 :]
            center_image = images[len(images) // 2]

            for i, image in enumerate(flipped_images_left):
                if i == 0:
                    image.next_to(center_image, LEFT, buff=image_spacing)
                else:
                    image.next_to(flipped_images_left[i - 1], LEFT, buff=image_spacing)

            for i, image in enumerate(images_right):
                if i == 0:
                    image.next_to(center_image, RIGHT, buff=image_spacing)
                else:
                    image.next_to(images_right[i - 1], RIGHT, buff=image_spacing)

        if not is_number_of_images_uneven:
            raise NotImplementedError("Even number of images not implemented yet.")

        for i, name in enumerate(names):
            name.next_to(images[i], DOWN, buff=text_offset)

        v_groups = []
        for i, _ in enumerate(images):
            v_groups.append(Group(images[i], names[i]))

        # Display the images
        # self.play(*[FadeIn(image) for image in images])
        self.play(*[FadeIn(v_group) for v_group in v_groups])
        self.wait(2)

        self.play(
            v_groups[0].animate.move_to(LEFT * 5 + UP * 2),
            v_groups[1].animate.move_to(LEFT * 5),
            v_groups[2].animate.move_to(LEFT * 5 + DOWN * 2),
        )

        self.wait(2)

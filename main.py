import numpy as np
from manim import (
    Scene,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    FadeIn,
    FadeOut,
    Text,
    Group,
    Circle,
    RoundedRectangle,
    Line,
    WHITE,
)
from manim.utils.rate_functions import linear, ease_out_sine, rush_into

from candidate import CandidateManimListFromVote
from color_utils import get_colors
from jm_constant import EASY_VOTE_SECOND_GRADE
from streched_rectangles import NextToStretchRectangleRightObjects


class EntertainingJM(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vote = EASY_VOTE_SECOND_GRADE
        self.candidates = CandidateManimListFromVote(self.vote).build()
        self.colors = get_colors(self.vote.nb_grades)

    def construct(self):
        v_groups = self.present_candidate()
        self.add_majority_label(v_groups)
        self.present_grades(v_groups[0])
        self.vertical_bar(v_groups)
        # self.stack(v_groups)
        self.stack_with_controled_time(v_groups, up_to_majority=True)
        self.replace_groups(v_groups)
        self.wait(2)

    def stack(self, groups):
        """
        For Now it is stacked at the same pace.
        Todo: stack with a the same speed for each percent of bars.
        """

        all_rectangles = []
        for i in range(self.vote.nb_grades):
            rectangles = []
            for num, candidate in enumerate(self.vote.candidates):
                rectangles.append(
                    NextToStretchRectangleRightObjects(
                        width=self.vote[candidate][i] / 10,
                        object_to_next_to=(
                            # align on pictures
                            groups[num].submobjects[0]
                            if i == 0
                            else all_rectangles[i - 1][num].stretched_rect
                        ),
                        direction=RIGHT,
                        color=self.colors[i],
                    )
                )
            all_rectangles.append(rectangles)
            self.play(*[rect.stretch for rect in rectangles])

        self.wait()

    def stack_with_controled_time(self, groups, up_to_majority=False):
        self.stack_bars = []
        time_by_grade = 1

        rate_funcs = [rush_into]
        rate_funcs += [linear] * (self.vote.nb_grades - 2)
        rate_funcs += [ease_out_sine]

        grades = self.vote.up_to_majority_grade if up_to_majority else self.vote.grades

        for g, grade in enumerate(grades):
            rectangles = []
            votes = self.vote.votes_by_grade(grade)
            max_vote = max(votes)
            time_to_stretch = np.array(self.vote.viz_max_votes_by_grade_to_max(grade)) / max_vote * time_by_grade

            votes_to_max = self.vote.viz_votes_by_grade_to_max(grade)
            for j, time in enumerate(time_to_stretch):
                rectangle_series = []
                for c, candidate in enumerate(self.vote.candidates):

                    if g == 0 and j == 0:  # align on pictures
                        object_to_next_to = groups[c].submobjects[0]
                        buffer = 0.25
                    elif g != 0 and j == 0:  # new grade
                        object_to_next_to = self.stack_bars[g - 1][-1][c].stretched_rect
                        buffer = 0
                    else:
                        object_to_next_to = rectangles[j - 1][c].stretched_rect
                        buffer = 0

                    rectangle_series.append(
                        NextToStretchRectangleRightObjects(
                            # width=self.vote[candidate][i] / 10,
                            width=votes_to_max[c][j] / 10,
                            object_to_next_to=object_to_next_to,
                            direction=RIGHT,
                            buffer=buffer,
                            color=self.colors[g],
                        )
                    )

                self.play(*[rect.stretch(ratefunc=rate_funcs[j]) for rect in rectangle_series], run_time=time * 3)
                rectangles.append(rectangle_series)
            self.stack_bars.append(rectangles)
            self.wait(0.5)

        self.wait()

    def replace_groups(self, groups):
        candidate_idx_to_fadeout = self.vote.candidates_idx_without_majority_grade
        rectangles_to_fadeout = []
        for e in self.stack_bars:
            for t in e:
                for candidate in candidate_idx_to_fadeout:
                    rectangles_to_fadeout.append(t[candidate].original_rect)

        candidate_groups_to_fadeout = [groups[c] for c in candidate_idx_to_fadeout]

        to_fade_out = rectangles_to_fadeout + candidate_groups_to_fadeout
        ready_to_fade_out = [FadeOut(group, rate_func=rush_into) for group in to_fade_out]

        candidate_idx_to_move = self.vote.candidates_idx_with_majority_grade
        rectangles_to_move = []
        for e in self.stack_bars:
            for t in e:
                for candidate in candidate_idx_to_move:
                    rectangles_to_move.append(t[candidate].original_rect)

        candidate_groups_to_move = [groups[c] for c in candidate_idx_to_move]

        to_move = rectangles_to_move + candidate_groups_to_move
        ready_to_move = [group.animate.shift(UP) for group in to_move]

        ready_to_play = ready_to_fade_out + ready_to_move

        self.play(*ready_to_play)

    def present_candidate(self):
        image_spacing = 0.5
        scale = 1

        nb_candidates = self.vote.nb_candidates
        is_number_of_images_uneven = nb_candidates % 2 != 0

        images = self.candidates.images
        for image in images:
            image.scale(scale)

        if is_number_of_images_uneven:
            images_left = images[: nb_candidates // 2]
            flipped_images_left = images_left[::-1]
            images_right = images[nb_candidates // 2 + 1 :]
            center_image = images[nb_candidates // 2]

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

        # Display the images
        # self.play(*[FadeIn(image) for image in images])
        self.play(*[FadeIn(group) for group in self.candidates.to_manim()])
        self.wait(1)

        # Define the vertical offset for each group
        start_from = LEFT * 5 + DOWN * 2
        #
        # # Animate each group to its target position
        move_to = []
        for i, group in enumerate(self.candidates.to_manim()):
            target_position = start_from + UP * i * 2
            move_to.append(group.animate.move_to(target_position))
        self.play(*move_to)

        self.wait(2)

        return self.candidates.to_manim()

    def add_majority_label(self, groups):
        mj_grades = self.vote.majority_grades

        for i, group in enumerate(groups):
            text_group = RoundedRectangle(corner_radius=1.5, height=3.0, width=4.0)
            text_group = RoundedRectangle(corner_radius=1.5, height=3.0, width=4.0)

            majority_label = Text(mj_grades[i], font_size=12)
            majority_label.next_to(group, UP)
            self.play(FadeIn(majority_label))

    def vertical_bar(self, groups):

        offset = (10 + self.vote.nb_grades * 0) / 2 + 0.25
        # Plot a vertical dash line
        start_from = DOWN * 3
        end_at = UP * 3
        dash_line = Line(start=start_from, end=end_at, color=WHITE).next_to(groups[1], RIGHT, buff=offset)
        self.play(FadeIn(dash_line))

    def present_grades(self, last_group):
        # build Circles
        circles = [
            Circle(radius=0.1, color=self.colors[i], fill_color=self.colors[i], fill_opacity=1)
            for i in range(self.vote.nb_grades)
        ]
        grades = [Text(grade, font_size=12) for grade in self.vote.grades]
        grade_groups = []

        # position first circle
        circles[0].next_to(last_group, RIGHT + DOWN)

        # all text to the right of the circles
        for i in range(0, self.vote.nb_grades):
            grades[i].next_to(circles[i], RIGHT)

        # circle and text grouped
        for i in range(0, self.vote.nb_grades):
            grade_groups.append(Group(circles[i], grades[i]))

        # position the other groups
        for i in range(1, self.vote.nb_grades):
            grade_groups[i].next_to(grade_groups[i - 1], RIGHT)

        self.play(*[FadeIn(grade_group) for grade_group in grade_groups])

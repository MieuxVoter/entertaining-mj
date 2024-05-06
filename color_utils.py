from manim import ManimColor
from seaborn import color_palette


class JMColors:
    def __init__(self, colors: tuple[ManimColor, ...] = None):

        self._colors = colors

    @classmethod
    def from_nb_grades(cls, nb_grades: int):
        """
        Returns a dictionary with the colors of each grade.

        Parameters
        ----------
        nb_grades : int
            The number of grades.
        """
        colors = color_palette(palette="coolwarm", n_colors=nb_grades)

        return cls(colors=tuple([ManimColor(color) for color in colors]))

    def grade_color(self, grade: int):
        """
        Returns the color of a grade.

        Parameters
        ----------
        grade : int
            The grade.
        """
        return self.colors[grade]

    @property
    def colors(self):
        return self._colors

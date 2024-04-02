from seaborn import color_palette
from manim import ManimColor


def get_colors(nb_grades: int) -> tuple[ManimColor, ...]:
    """
    Returns a dictionary with the colors of each grade.

    Parameters
    ----------
    nb_grades : int
        The number of grades.

    Returns
    -------
    tuple[ManimColor, ...]
        A dictionary with the colors of each grade.
    """
    colors = color_palette(palette="coolwarm", n_colors=nb_grades)

    return tuple([ManimColor(color) for color in colors])

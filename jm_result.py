from dataclasses import dataclass

import numpy as np
from manim import ManimColor

from color_utils import JMColors


@dataclass(frozen=True)
class JMCandidateResult:
    """
    A class to handle the results of a candidate.

    Parameters
    ----------
    candidate : str
        The name of the candidate.
    votes : tuple[int]
        The votes of the candidate.
    rank : int
        The rank of the candidate.
    grade : str
        The grade of the candidate.
    color : ManimColor
        The color of the grade.
    """

    candidate: str
    votes: tuple[int]
    rank: int
    grade: str
    color: ManimColor


class JMResults:
    def __init__(self, votes: dict[str, tuple[int]], ranks: tuple[int], grades: list[str] = None):
        """
        A class to handle the results of a vote.

        Parameters
        ----------
        votes : dict[str, tuple[int]]
            A dictionary with the votes of each candidate.
        ranks : tuple[int]
            The rank of each candidate.
        grades : list[str]
            The list of grades, From best to worst. e.g. ["Excellent", "Good", "Fair", "Poor"]
        """

        self._ranks = ranks
        self._votes = votes
        self._grades = grades
        self._colors = JMColors.from_nb_grades(self.nb_grades)

    def __getitem__(self, item):
        return self.votes[item]

    def to_candidate_results(self, candidate: str) -> JMCandidateResult:
        return JMCandidateResult(
            candidate=candidate,
            votes=self.votes[candidate],
            rank=self.rank(candidate),
            grade=self.candidate_majority_grade(candidate),
            color=self.color(self.candidate_majority_grade(candidate)),
        )

    @property
    def grades(self):
        return self._grades

    @property
    def nb_candidates(self):
        return len(self.votes)

    @property
    def candidates(self) -> list[str]:
        return list(self.votes.keys())

    @property
    def nb_grades(self):
        return len(self.votes["michel"])

    @property
    def votes(self):
        return self._votes

    def votes_by_grade(self, grade: str) -> list[int]:
        return [votes[self._grades.index(grade)] for candidate, votes in self._votes.items()]

    def cumulative_results(self, mode="backward"):
        result_map = {
            "backward": {
                candidate: np.hstack((0, np.cumsum(grades[:-1]))) for candidate, grades in self._votes.items()
            },
            "forward": {candidate: np.cumsum(grades) for candidate, grades in self._votes.items()},
        }

        return result_map[mode]

    @property
    def ranks(self):
        return self._ranks

    def rank(self, candidate: str) -> int:
        candidate_idx = self.candidates.index(candidate)
        return self._ranks.index(candidate_idx)

    @property
    def majority_grade(self) -> str:
        """The best grade that cumulative votes reach the 50% mark."""
        majority_grades = self.majority_grades
        majority_indexes = []
        for _, grade in enumerate(majority_grades):
            majority_indexes.append(self._grades.index(grade))

        return self._grades[min(majority_indexes)]

    @property
    def up_to_majority_grade(self) -> list[str]:
        """The best grade that cumulative votes reach the 50% mark."""
        majority_grades = self.majority_grades
        majority_indexes = []
        for _, grade in enumerate(majority_grades):
            majority_indexes.append(self._grades.index(grade))

        return self._grades[: min(majority_indexes) + 1]

    @property
    def candidates_without_majority_grade(self) -> list[str]:
        """Get the candidates that do not have the majority grade"""
        majority_grade = self.majority_grade
        return [
            candidate for candidate in self.candidates if self.candidate_majority_grade(candidate) != majority_grade
        ]

    @property
    def candidates_idx_without_majority_grade(self) -> list[int]:
        """Get the candidates index that do not have the majority grade"""
        candidates = self.candidates_without_majority_grade
        return [self.candidates.index(candidate) for candidate in candidates]

    @property
    def candidates_idx_with_majority_grade(self) -> list[int]:
        """Get the candidates index that have the majority grade"""
        candidates = self.candidates_with_majority_grade
        return [self.candidates.index(candidate) for candidate in candidates]

    @property
    def candidates_with_majority_grade(self) -> list[str]:
        """Get the candidates that have the majority grade"""
        majority_grade = self.majority_grade
        return [
            candidate for candidate in self.candidates if self.candidate_majority_grade(candidate) == majority_grade
        ]

    def candidate_majority_grade(self, candidate: str) -> str:
        """Returns the grade that reaches the 50% mark for a given candidate."""
        votes = self._votes[candidate]
        cumulative_votes = np.cumsum(votes)
        majority_vote = np.max(cumulative_votes) / 2
        majority_grade = self._grades[np.argmax(cumulative_votes >= majority_vote)]
        return majority_grade

    @property
    def majority_grades(self) -> list[str]:
        return [self.candidate_majority_grade(candidate) for candidate in self.candidates]

    def viz_votes_by_grade_to_max(self, grade: str) -> list[list[int]]:
        """
        Visualize incremental votes of each candidate by grade to the maximum vote.
        e.g. for grade "Excellent":
            votes = [10, 8, 5, 3]
            viz_votes_for_candidate 0 = [3, 5, 8, 10] -> [3, 2, 3, 2]
            viz_votes_for_candidate 1 = [3, 5, 8, 8] -> [3, 2, 3, 0]
            viz_votes_for_candidate 2 = [3, 5, 5, 5] -> [3, 2, 0, 0]
            viz_votes_for_candidate 3 = [3, 3, 3, 3] -> [3, 0, 0, 0]
        """
        votes = self.votes_by_grade(grade)
        sorted_votes = sorted(votes, reverse=False)
        sorted_cumulative_votes = [[] for _ in range(self.nb_candidates)]
        for i, sorted_vote in enumerate(sorted_votes):
            for j in range(self.nb_candidates):
                if sorted_vote <= votes[j]:
                    sorted_cumulative_votes[j].append(sorted_vote)
                else:
                    sorted_cumulative_votes[j].append(votes[j])

        # return sorted_cumulative_votes
        # diff each element with the previous one except for the first one
        return [
            [
                (
                    sorted_cumulative_votes[j][i] - sorted_cumulative_votes[j][i - 1]
                    if i > 0
                    else sorted_cumulative_votes[j][i]
                )
                for i in range(len(sorted_cumulative_votes[j]))
            ]
            for j in range(self.nb_candidates)
        ]

    def viz_max_votes_by_grade_to_max(self, grade: str) -> list[int]:
        """Get the maximum of them"""
        vote_to_cumulate = self.viz_votes_by_grade_to_max(grade)
        # keep the list that keeps adding
        sum_of_votes = [sum(vote) for vote in vote_to_cumulate]
        index_max_cumsum = np.argmax(sum_of_votes)
        return vote_to_cumulate[index_max_cumsum]

    @property
    def colors(self):
        return self._colors.colors

    def color(self, grade: str):
        idx = self._grades.index(grade)
        return self._colors.grade_color(idx)

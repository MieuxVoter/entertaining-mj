from manim import ImageMobject, Text, Group, DOWN, ORIGIN, UP, RoundedRectangle

from jm_result import JMResults, JMCandidateResult


class CandidateCharacteristics:
    def __init__(self, name: str, surname: str, picture: str):
        self.name = name
        self.surname = surname
        self._picture = picture

    def __str__(self):
        return f"{self.name}\n{self.surname}"

    @property
    def picture(self):
        return self._picture


class GradeLabelOnRoundedRectangle:
    def __init__(self, grade: str, color: str = "WHITE"):
        self.grade = grade
        self.manim_grade_string = Text(grade, font_size=12)
        self.manim_rounded_rectangle = RoundedRectangle(
            corner_radius=0.15, height=0.30, width=0.40, fill_color=color, fill_opacity=1
        )
        self.group = self.to_manim()

    def to_manim(self):
        return Group(
            self.manim_rounded_rectangle,
            self.manim_grade_string.next_to(self.manim_rounded_rectangle, ORIGIN),
        )


class CandidateManim:
    def __init__(self, characteristics: CandidateCharacteristics, result: JMCandidateResult):
        self.characteristics = characteristics
        self.result = result
        self.manim_image = ImageMobject(self.characteristics.picture)
        self.manim_text = Text(self.characteristics.__str__(), font_size=12)
        self.manim_grade_label = GradeLabelOnRoundedRectangle(self.result.grade).to_manim()
        self.group = self.to_manim()
        # self.extra_elements = []

    def __str__(self):
        """Make first letter UpperCase and the rest LowerCase"""
        first_name = self.characteristics.name[0].upper() + self.characteristics.name[1:].lower()
        first_surname = self.characteristics.surname[0].upper() + self.characteristics.surname[1:].lower()
        return f"{first_name} {first_surname}"

    def to_manim(self):
        text_offset = 0.25
        return Group(
            self.manim_image,
            self.manim_text.next_to(self.manim_image, DOWN, buff=text_offset),
            self.manim_grade_label.next_to(self.manim_text, UP * 0.25, buff=0),
            # *self.extra_elements,
        )

    def add_object(self, obj):
        self.extra_elements.append(obj)


class CandidateManimListFromVote:
    def __init__(self, vote: JMResults):
        self.vote = vote
        self.candidates = CandidateManimList()

    def build(self):
        for i in range(self.vote.nb_candidates):
            self.candidates.append(
                CandidateManim(
                    characteristics=CandidateCharacteristics(
                        name=self.vote.candidates[i],
                        surname="Dupont",  # TODO: add surname to vote
                        picture="image126.png",  # TODO: add picture to vote
                    ),
                    result=self.vote.to_candidate_results(self.vote.candidates[i]),
                )
            )
        return self.candidates


class CandidateManimList:
    def __init__(self, candidates: list[CandidateManim] = None):
        self.candidates = candidates if candidates is not None else []

    # append a candidate to the list
    def append(self, candidate: CandidateManim):
        self.candidates.append(candidate)

    @property
    def images(self) -> list[ImageMobject]:
        return [candidate.manim_image for candidate in self.candidates]

    # count candidates
    def __len__(self):
        return len(self.candidates)

    def to_manim(self) -> list[Group]:
        return [candidate.to_manim() for candidate in self.candidates]

from manim import ImageMobject, Text, Group, DOWN


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


class CandidateManim:
    def __init__(self, characteristics: CandidateCharacteristics):
        self.characteristics = characteristics
        self.manim_image = ImageMobject(self.characteristics.picture)
        self.manim_text = Text(self.characteristics.__str__(), font_size=12)

    def __str__(self):
        """Make first letter UpperCase and the rest LowerCase"""
        first_name = self.characteristics.name[0].upper() + self.characteristics.name[1:].lower()
        first_surname = self.characteristics.surname[0].upper() + self.characteristics.surname[1:].lower()
        return f"{first_name} {first_surname}"

    @property
    def picture(self):
        return self._picture

    def to_manim(self):
        text_offset = 0.25
        return Group(
            self.manim_image,
            self.manim_text.next_to(self.manim_image, DOWN, buff=text_offset),
        )


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

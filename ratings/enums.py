from enum import IntEnum


class Rating(IntEnum):
    ZERO_STAR = 0
    ZERO_STAR_AND_HALF = 1
    ONE_STAR = 2
    ONE_STAR_AND_HALF = 3
    TWO_STARS = 4
    TWO_STARS_AND_HALF = 5
    THREE_STARS = 6
    THREE_STARS_AND_HALF = 7
    FOUR_STARS = 8
    FOUR_STARS_AND_HALF = 9
    FIVE_STARS = 10

    @staticmethod
    def choices():
        return [
            ("0", Rating.ZERO_STAR.value),
            ("0.5", Rating.ZERO_STAR_AND_HALF.value),
            ("1", Rating.ONE_STAR.value),
            ("1.5", Rating.ONE_STAR_AND_HALF.value),
            ("2", Rating.TWO_STARS.value),
            ("2.5", Rating.TWO_STARS_AND_HALF.value),
            ("3", Rating.THREE_STARS.value),
            ("3.5", Rating.THREE_STARS_AND_HALF.value),
            ("4", Rating.FOUR_STARS.value),
            ("4.5", Rating.FOUR_STARS_AND_HALF.value),
            ("5", Rating.FIVE_STARS.value),
        ]

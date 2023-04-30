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


class ViewingState(IntEnum):
    WATCHING = 0
    VIEWED = 1

    @staticmethod
    def choices():
        return [
            ("Watching", ViewingState.WATCHING.value),
            ("Viewed", ViewingState.VIEWED.value),
        ]


class Category(IntEnum):
    FILM_AND_ANIMATION = 1
    AUTOS_AND_VEHICLES = 2
    MUSIC = 10
    PETS_AND_ANIMALS = 15
    SPORTS = 17
    TRAVEL_AND_EVENTS = 19
    GAMING = 20
    PEOPLE_AND_BLOGS = 22
    COMEDY = 23
    ENTERTAINMENT = 24
    NEWS_AND_POLITICS = 25
    HOWTO_AND_STYLE = 26
    EDUCATION = 27
    SCIENCE_AND_TECHNOLOGY = 28
    NONPROFITS_AND_ACTIVISM = 29

    @staticmethod
    def choices():
        return [
            ("Film & Animation", Category.FILM_AND_ANIMATION.value),
            ("Autos & Vehicles", Category.AUTOS_AND_VEHICLES.value),
            ("Music", Category.MUSIC.value),
            ("Pets & Animals", Category.PETS_AND_ANIMALS.value),
            ("Sports", Category.SPORTS.value),
            ("Travel & Events", Category.TRAVEL_AND_EVENTS.value),
            ("Gaming", Category.GAMING.value),
            ("People & Blogs", Category.PEOPLE_AND_BLOGS.value),
            ("Comedy", Category.COMEDY.value),
            ("Entertainment", Category.ENTERTAINMENT.value),
            ("News & Politics", Category.NEWS_AND_POLITICS.value),
            ("How-to & Styles", Category.HOWTO_AND_STYLE.value),
            ("Education", Category.EDUCATION.value),
            ("Science & Technology", Category.SCIENCE_AND_TECHNOLOGY.value),
            ("Non-profits & Activism", Category.NONPROFITS_AND_ACTIVISM.value),
        ]

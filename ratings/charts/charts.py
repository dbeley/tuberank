from django.contrib.auth.models import User

from ratings.enums import Rating


def get_video_ratings_chart_for_user(user: User) -> dict[str, list]:
    ratings = user.video_ratings.values_list("rating", flat=True)

    ratings_counts: dict = {}
    for rating_choice in Rating.choices():
        ratings_counts[rating_choice[0]] = 0

    for rating in ratings:
        ratings_counts[rating] += 1

    sorted_ratings_counts = sorted(ratings_counts.items(), key=lambda x: x[0])

    ratings_labels = [
        Rating.choices()[rating[0]][1] for rating in sorted_ratings_counts
    ]
    ratings_data = [rating[1] for rating in sorted_ratings_counts]
    return {
        "ratings_labels": ratings_labels,
        "ratings_data": ratings_data,
    }


def get_channel_ratings_chart_for_user(user: User) -> dict[str, list]:
    ratings = user.channel_ratings.values_list("rating", flat=True)

    ratings_counts: dict = {}
    for rating_choice in Rating.choices():
        ratings_counts[rating_choice[0]] = 0

    for rating in ratings:
        ratings_counts[rating] += 1

    sorted_ratings_counts = sorted(ratings_counts.items(), key=lambda x: x[0])

    ratings_labels = [
        Rating.choices()[rating[0]][1] for rating in sorted_ratings_counts
    ]
    ratings_data = [rating[1] for rating in sorted_ratings_counts]
    return {
        "ratings_labels": ratings_labels,
        "ratings_data": ratings_data,
    }

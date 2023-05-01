# ytvd (YouTube Video Database)

A community website to rate and discover youtube videos.

## Development

```
python -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```

```
python manage.py migrate --run-syncdb
```

## TODO

### Homepage
- Add links to Github in footer
- Add about page

### Video detail page
- Display categories
- Display number of ratings + rating in a better way (top of the page, stars, separate box)
- Display duration
- Display related videos with the same tags
- Display "list this video is in" with best lists where the video is

### Video list page
- Add sorting mechanism
- Add htmx-aware form to add/modify a rating

### Channel rating page
- Create channel rating page

### Categories
- Add categories page
- Add categories to videos/channels/snapshots

### Profile / Settings
- Add profile / settings page
- Add statistics
- Add user-generated lists with ratings
- Re-arrange review body

### Channel list
- Add channel rating feature
- Display all channel reviews
- Add sorting mechanism (alphabetical, chronological, popular, indexed, best rated, etc.)
- Display duration

### URL mapping
- Add slug for videos, channels

### Tag / Lists
- Feature to delete a tag from a video
- Feature to delete a tag when no video attached to it
- Feature to reorder a list

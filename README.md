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

### Search page
- Add sorting mechanism

### Channel detail page
- Display channel ratings + reviews
- Include link to see the channel on youtube
- Add sorting mechanism
- Display duration

### Video detail page
- Display categories
- Display number of ratings + rating in a better way (top of the page, stars, separate box)
- Display duration
- Display related videos with the same tags
- Display "list this video is in" with best lists where the video is

### Channel list page
- Add sorting mechanism (alphabetical, chronological, popular, indexed, best rated, etc.)

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

### Localization
- Add FR language
- Add EN language

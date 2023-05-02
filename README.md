# TubeRank

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

### Get all video urls of a YouTube channel

```
yt-dlp -j --flat-playlist $CHANNEL_URL | jq -r '.id' | sed 's_^_https://www.youtube.com/watch?v=_'
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
- Display duration

### URL mapping
- Add slug for videos, channels

### Tag / Lists
- Better display of tags and lists (critical feature)
- Feature to delete a tag from a video
- Feature to delete a tag when no video attached to it
- Feature to reorder a list

### Deployment
- Fix nodejs deployment for static tailwind files
- Remove copyright mention in footer

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
- DONE Display curated selection of Channels / Videos based on ratings
- Add links to Github in footer
- Add Import video feature

### Search page
- DONE Add htmx to search page to only updates channel or video parts
- Add sorting mechanism

### Channel detail page
- DONE Display list of all imported videos + ratings
- Display channel ratings + reviews
- Include link to see the channel on youtube
- Add sorting mechanism

### Video detail page
- Display categories
- DONE Include link to watch the video (player integration?)
- Display user-generated tags, lists
- DONE Display video ratings + reviews

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
- Add "watched" model

### Import video
- Add import video feature

### Charts page
- Add possibility to create charts
- Paginated
- User tags
- Sort by best rating, most ratings, etc.
- Htmx ?

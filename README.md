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
- Add about page

### Search page
- DONE Add htmx to search page to only updates channel or video parts
- Add sorting mechanism

### Channel detail page
- DONE Display list of all imported videos + ratings
- Display channel ratings + reviews
- Include link to see the channel on youtube
- Add sorting mechanism
- Display duration

### Video detail page
- Display categories
- DONE Include link to watch the video (player integration?)
- DONE Display user-generated tags, lists
- DONE Display video ratings + reviews
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

### User-generated tags
- DONE Add tag model
- DONE Add tag page
- DONE Add possibility to add tags to videos

### User-generated lists
- DONE Add list model
- DONE Create view to add a video to a list
- DONE Create view to view a list

### Profile / Settings
- Add profile / settings page
- Add statistics
- DONE Add "watched" model
- Add user-generated lists with ratings

### Import video
- Add import video feature

### Charts page
- DONE Add possibility to create charts
- DONE Paginated
- DONE User tags
- DONE Sort by best rating, most ratings, etc.

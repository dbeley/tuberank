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
- Display curated selection of Channels / Videos based on ratings

### Channel detail page
- Display list of all imported videos + ratings
- Display channel ratings + reviews
- Include link to see the channel on youtube

### Video detail page
- Display categories
- Include link to watch the video (player integration?)
- Display user-generated tags, lists
- Display video ratings + reviews

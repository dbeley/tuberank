# TubeRank

A community website to rate and discover youtube videos.

## Dependencies

- python
- nodejs
- npm
- gettext

## Development

```
python -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```

```
npm install -D tailwindcss
npm install flowbite
npm run tailwind-watch
python manage.py migrate --run-syncdb
```

## Local Deployment

- Create `.env` with the required secrets (see `.env.example` for an example)

## Deployment

fly.io cheatsheet

```
fly deploy
fly secrets list
fly secrets set DEBUG="0"
fly logs
fly ssh console
fly ssh console --pty -C 'python /code/manage.py migrate'
fly ssh console --pty -C 'python /code/manage.py createsuperuser'
```

### Get all video urls of a YouTube channel

```
yt-dlp -j --flat-playlist $CHANNEL_URL | jq -r '.id' | sed 's_^_https://www.youtube.com/watch?v=_'
```

## TODO

### Homepage
- Add about page

### Video detail page
- Display categories
- Display related videos with the same tags
- Add htmx-aware form to add/modify a rating

### Categories
- Add categories page
- Add categories to videos/channels/snapshots

### Login / Registration
- Update registration template
- Display login errors

### Profile / Settings
- Add profile / settings page
- Add more statistics
- Add user-generated lists with ratings
- Re-arrange review body
- Remove/improve display of profile picture

### Channel list
- Add channel rating feature
- Display all channel reviews
- Display duration

### URL mapping
- Add slug for videos, channels

### Tag / Lists
- Better display of tags
- Feature to delete a tag from a video
- Feature to delete a tag when no video attached to it
- Feature to reorder a list

### Import function
- add channel batch import feature

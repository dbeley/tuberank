# TubeRank

A community website to rate and discover youtube videos.

Built with Django (django-rest-framework, whitenoise), Tailwind (Flowbite) and htmx. Deployed on fly.io.

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

Deployment from scratch with fly.io

```
fly launch
fly secrets set LOCAL_DEPLOY="0"
fly secrets set ... # see .env.example for list of environment variables to set
fly deploy
fly certs add domain.tld
fly certs check domain.tld
```

fly.io cheatsheet

```
fly secrets list
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
- Add ratings to each tag. When 0 -> tag is not displayed or is deleted

### Import function
- Add channel batch import feature
- Add search by url + importing it automatically
- Add api to import videos + rate + view

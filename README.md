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

## Deployment

- Create `secret.ini` with the required secrets (see `secret.ini.example` for an example)
- Add domain to `tuberank.settings.ALLOWED_HOSTS`
- Add domain to `tuberank.settings.CSRF_TRUSTED_ORIGINS`
- Check that `tuberank.settings.DEBUG` is `False`
- Check that `tuberank.settings.DATABASES` default backend is `postgresql`

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

### Channel rating page
- Create channel rating page

### Categories
- Add categories page
- Add categories to videos/channels/snapshots

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
- Better display of tags and lists (critical feature)
- Feature to delete a tag from a video
- Feature to delete a tag when no video attached to it
- Feature to reorder a list

### Import function
- add channel batch import feature

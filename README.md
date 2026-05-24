# 🎵 Ukulele Songbook

Personal Streamlit app for practicing ukulele songs. One tab per song, lyrics on the left, picking/chord notation on the right.

## Project structure

```
ukulele_app/
├── app.py              # the Streamlit app
├── requirements.txt    # Python dependencies
├── README.md
└── songs/
    ├── imagine/
    │   ├── lyrics.txt          # lyrics (editable)
    │   └── tab.pdf             # picking/chords file (pdf, jpg, or png)
    ├── bad_guy_v1/
    │   ├── lyrics.txt
    │   └── tab.jpg
    ├── sweet_home_alabama/
    │   └── lyrics.txt          # tab file not yet added — drop one in to populate
    └── ...
```

Each song lives in its own folder under `songs/`. The folder must contain:
- `lyrics.txt` — plain text. Lines wrapped in `[brackets]` (e.g. `[Verse 1]`, `[Chorus]`) are styled as section headers automatically.
- `tab.pdf`, `tab.jpg`, `tab.jpeg`, or `tab.png` — the picking/chord notation. Multi-page PDFs get prev/next arrows in the viewer.

## Editing lyrics from GitHub

1. Open the repo on GitHub
2. Browse to `songs/<song_name>/lyrics.txt`
3. Click the ✏️ pencil icon → paste lyrics → "Commit changes"
4. Streamlit Cloud auto-redeploys within seconds

## Adding a tab file later (Sweet Home Alabama, Hells Bells)

1. Save your PDF/JPG as `tab.pdf` (or `tab.jpg`)
2. Drag-and-drop it into `songs/sweet_home_alabama/` (or `songs/hells_bells/`) on GitHub
3. Commit. Done.

## Adding a new song

1. Create a new folder under `songs/`, e.g. `songs/my_new_song/`
2. Add `lyrics.txt` and a `tab.pdf`/`tab.jpg`
3. Add the entry to the `SONGS` list near the top of `app.py`:

```python
SONGS = [
    ...,
    ("my_new_song", "My New Song"),
]
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at <http://localhost:8501>.

## Deploying to Streamlit Cloud (free)

1. Push this folder to a GitHub repo.
2. Go to <https://share.streamlit.io>, click "New app", point it at your repo, set the main file to `app.py`.
3. Done — Streamlit Cloud installs `requirements.txt` automatically.

## Tabs

- **🎼 Chords** — reference grid of common ukulele chords (major, minor, 7, maj7, m7) across all 12 roots, drawn as SVG diagrams.
- **Songs** — one tab per song, in the order defined by `SONGS` in `app.py`.

## Notes

- The Last of Us, Pride and Joy, and Better Call Saul are instrumentals — their `lyrics.txt` files are intentionally empty.
- Bad Guy is split into two tabs (v1 and v2) for the two different arrangements.
- Lyrics files are in your own repo and never quoted by the app to anyone outside; the app is a personal practice tool.

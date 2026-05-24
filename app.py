"""Ukulele Songbook — a personal Streamlit app.

Layout:
- Tab 1: Ukulele chord reference (common chords with diagrams)
- Tabs 2+: One per song, lyrics on the left, tab file on the right
"""
from pathlib import Path
import streamlit as st
import pypdfium2 as pdfium
from PIL import Image

# ─────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Ukulele App",
    page_icon="",
    layout="wide",
)

APP_DIR = Path(__file__).parent
SONGS_DIR = APP_DIR / "songs"

# Order of song tabs. Each entry: (folder_slug, display_title)
SONGS = [
    ("the_last_of_us",       "The Last of Us"),
    ("imagine",              "Imagine"),
    ("just_the_two_of_us",   "Just the Two of Us"),
    ("sweet_home_alabama",   "Sweet Home Alabama"),
    ("sugar",                "Sugar"),
    ("believer",             "Believer"),
    ("shallow",              "Shallow"),
    ("banana_pancakes",      "Banana Pancakes"),
    ("i_lost_my_baby",       "I Lost My Baby"),
    ("bella_ciao",           "Bella Ciao"),
    ("wicked_game",          "Wicked Game"),
    ("do_i_wanna_know",      "Do I Wanna Know"),
    ("hells_bells",          "Hells Bells"),
    ("dream_on",             "Dream On"),
    ("country_roads",        "Country Roads"),
    ("bad_guy_v1",           "Bad Guy (v1)"),
    ("bad_guy_v2",           "Bad Guy (v2)"),
    ("pride_and_joy",        "Pride and Joy"),
    ("free_bird",            "Free Bird"),
    ("nothing_else_matters", "Nothing Else Matters"),
    ("looking_out_for_you",  "Looking Out for You"),
    ("better_call_saul",     "Better Call Saul"),
    ("never_be_alone",       "Never Be Alone"),
    ("dust_bowl_iii",        "Dust Bowl III"),
    ("feel_good_inc",        "Feel Good Inc."),
]

# ─────────────────────────────────────────────────────────────────────
# Ukulele chord reference data
# Standard tuning: G (high) – C – E – A
# Each entry: [G, C, E, A] fret numbers (0 = open)
# ─────────────────────────────────────────────────────────────────────

UKE_CHORDS = {
    # C family
    "C":     [0, 0, 0, 3],
    "Cm":    [0, 3, 3, 3],
    "C7":    [0, 0, 0, 1],
    "Cmaj7": [0, 0, 0, 2],
    "Cm7":   [3, 3, 3, 3],

    "C#":     [1, 1, 1, 4],
    "C#m":    [1, 4, 4, 4],
    "C#7":    [1, 1, 1, 2],
    "C#maj7": [1, 1, 1, 3],
    "C#m7":   [4, 4, 4, 4],

    # D family
    "D":     [2, 2, 2, 0],
    "Dm":    [2, 2, 1, 0],
    "D7":    [2, 2, 2, 3],
    "Dmaj7": [2, 2, 2, 4],
    "Dm7":   [2, 2, 1, 3],

    "Eb":     [3, 3, 3, 1],
    "Ebm":    [3, 3, 2, 1],
    "Eb7":    [3, 3, 3, 4],
    "Ebmaj7": [3, 3, 3, 5],
    "Ebm7":   [3, 3, 2, 4],

    # E family
    "E":     [4, 4, 4, 2],
    "Em":    [0, 4, 3, 2],
    "E7":    [1, 2, 0, 2],
    "Emaj7": [1, 3, 0, 2],
    "Em7":   [0, 2, 0, 2],

    # F family
    "F":     [2, 0, 1, 0],
    "Fm":    [1, 0, 1, 3],
    "F7":    [2, 3, 1, 0],
    "Fmaj7": [2, 4, 1, 3],
    "Fm7":   [1, 3, 1, 3],

    "F#":     [3, 1, 2, 1],
    "F#m":    [2, 1, 2, 0],
    "F#7":    [3, 4, 2, 4],
    "F#maj7": [3, 5, 2, 4],
    "F#m7":   [2, 4, 2, 4],

    # G family
    "G":     [0, 2, 3, 2],
    "Gm":    [0, 2, 3, 1],
    "G7":    [0, 2, 1, 2],
    "Gmaj7": [0, 2, 2, 2],
    "Gm7":   [0, 2, 1, 1],

    "G#":     [1, 3, 4, 3],
    "G#m":    [1, 3, 4, 2],
    "G#7":    [1, 3, 2, 3],
    "G#maj7": [1, 3, 3, 3],
    "G#m7":   [1, 3, 2, 2],

    # A family
    "A":     [2, 1, 0, 0],
    "Am":    [2, 0, 0, 0],
    "A7":    [0, 1, 0, 0],
    "Amaj7": [1, 1, 0, 0],
    "Am7":   [0, 0, 0, 0],

    "Bb":     [3, 2, 1, 1],
    "Bbm":    [3, 1, 1, 1],
    "Bb7":    [1, 2, 1, 1],
    "Bbmaj7": [3, 2, 1, 0],  # alt: 2210
    "Bbm7":   [1, 1, 1, 1],

    # B family
    "B":     [4, 3, 2, 2],
    "Bm":    [4, 2, 2, 2],
    "B7":    [2, 3, 2, 2],
    "Bmaj7": [3, 3, 2, 2],
    "Bm7":   [2, 2, 2, 2],
}

CHORD_ROOTS = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
CHORD_TYPES = ["", "m", "7", "maj7", "m7"]
TYPE_LABELS = {"": "Major", "m": "Minor", "7": "7th", "maj7": "Maj 7", "m7": "Min 7"}


# ─────────────────────────────────────────────────────────────────────
# SVG chord diagram generator
# ─────────────────────────────────────────────────────────────────────

def chord_svg(name: str, frets: list, width: int = 110, height: int = 145) -> str:
    """Render a ukulele chord diagram as inline SVG.
    frets order: [G, C, E, A] — leftmost string = G, rightmost = A.
    """
    grid_left = 20
    grid_top = 34
    grid_w = 72
    grid_h = 88
    num_strings = 4
    num_frets = 4
    string_gap = grid_w / (num_strings - 1)
    fret_gap = grid_h / num_frets

    pressed = [f for f in frets if f > 0]
    max_fret = max(pressed) if pressed else 0

    # If the chord fits in frets 1-4 of the nut, show the nut. Otherwise shift up.
    if max_fret <= num_frets:
        start_fret = 0
    else:
        start_fret = min(pressed) - 1

    parts = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">',
        # Title
        f'<text x="{width/2}" y="20" text-anchor="middle" '
        f'font-family="-apple-system, system-ui, sans-serif" font-size="15" '
        f'font-weight="600" fill="#222">{name}</text>',
    ]

    # Strings (vertical lines)
    for i in range(num_strings):
        x = grid_left + i * string_gap
        parts.append(
            f'<line x1="{x}" y1="{grid_top}" x2="{x}" y2="{grid_top + grid_h}" '
            f'stroke="#444" stroke-width="0.8"/>'
        )

    # Frets (horizontal lines)
    for j in range(num_frets + 1):
        y = grid_top + j * fret_gap
        sw = 2.5 if (j == 0 and start_fret == 0) else 0.8
        parts.append(
            f'<line x1="{grid_left}" y1="{y}" x2="{grid_left + grid_w}" y2="{y}" '
            f'stroke="#444" stroke-width="{sw}"/>'
        )

    # Position label (e.g. "3fr") when not at the nut
    if start_fret > 0:
        parts.append(
            f'<text x="{grid_left + grid_w + 6}" y="{grid_top + fret_gap/2 + 4}" '
            f'font-family="-apple-system, system-ui, sans-serif" font-size="10" '
            f'fill="#666">{start_fret + 1}fr</text>'
        )

    # String labels at the bottom (G C E A)
    string_labels = ["G", "C", "E", "A"]
    for i, label in enumerate(string_labels):
        x = grid_left + i * string_gap
        parts.append(
            f'<text x="{x}" y="{grid_top + grid_h + 14}" text-anchor="middle" '
            f'font-family="-apple-system, system-ui, sans-serif" font-size="10" '
            f'fill="#888">{label}</text>'
        )

    # Dots / open markers
    for i, fret in enumerate(frets):
        x = grid_left + i * string_gap
        if fret == 0:
            parts.append(
                f'<circle cx="{x}" cy="{grid_top - 10}" r="4" fill="none" '
                f'stroke="#444" stroke-width="1.2"/>'
            )
        else:
            rel_fret = fret - start_fret
            y = grid_top + (rel_fret - 0.5) * fret_gap
            parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#222"/>')

    parts.append('</svg>')
    return "".join(parts)


# ─────────────────────────────────────────────────────────────────────
# Lyrics rendering
# ─────────────────────────────────────────────────────────────────────

def lyrics_to_html(text: str) -> str:
    """Render lyrics: section headers in [brackets] become bold accents,
    lyric lines stay close together within a section, blank line between sections.
    """
    if not text.strip():
        return "<p style='color:#888;font-style:italic'>No lyrics yet.</p>"

    html_blocks = []
    for section in text.split("\n\n"):
        lines = section.strip().split("\n")
        if not lines:
            continue
        rendered = []
        for line in lines:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                rendered.append(
                    f'<div style="font-weight:600;color:#a59ce8;margin-top:14px;'
                    f'margin-bottom:4px;font-size:0.95em">{line}</div>'
                )
            else:
                # Escape HTML special chars
                line_html = (line.replace("&", "&amp;")
                                 .replace("<", "&lt;")
                                 .replace(">", "&gt;"))
                rendered.append(f'<div style="line-height:1.55">{line_html}</div>')
        html_blocks.append("".join(rendered))

    return ('<div style="font-family:-apple-system,system-ui,sans-serif;'
            'font-size:0.95em;color:#d0d0d0">' + "".join(html_blocks) + '</div>')


# ─────────────────────────────────────────────────────────────────────
# Tab file helpers
# ─────────────────────────────────────────────────────────────────────

def find_tab_file(folder: Path):
    """Return the path to a tab file in the folder (pdf/jpg/jpeg/png), or None."""
    for ext in ["pdf", "jpg", "jpeg", "png"]:
        candidates = list(folder.glob(f"tab.{ext}"))
        if candidates:
            return candidates[0]
    return None


@st.cache_data(show_spinner=False)
def get_pdf_page_count(pdf_path_str: str) -> int:
    pdf = pdfium.PdfDocument(pdf_path_str)
    return len(pdf)


@st.cache_data(show_spinner=False)
def render_pdf_page(pdf_path_str: str, page_num: int, scale: float = 2.0) -> Image.Image:
    pdf = pdfium.PdfDocument(pdf_path_str)
    page = pdf[page_num]
    bitmap = page.render(scale=scale)
    return bitmap.to_pil()


# ─────────────────────────────────────────────────────────────────────
# Chord-reference tab
# ─────────────────────────────────────────────────────────────────────

def render_chords_tab():
    st.markdown("### 🎵 Ukulele chord reference")
    st.caption("Standard tuning: **G – C – E – A** (high G). Open circles = open string, filled dots = fingered fret.")

    for root in CHORD_ROOTS:
        st.markdown(f"#### {root}")
        cols = st.columns(len(CHORD_TYPES))
        for col, suffix in zip(cols, CHORD_TYPES):
            name = root + suffix
            with col:
                if name in UKE_CHORDS:
                    st.markdown(
                        f'<div style="text-align:center">'
                        f'<div style="font-size:0.78em;color:#888;margin-bottom:2px">'
                        f'{TYPE_LABELS[suffix]}</div>'
                        f'{chord_svg(name, UKE_CHORDS[name])}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div style="text-align:center;color:#bbb;font-size:0.8em;'
                        'padding-top:40px">—</div>',
                        unsafe_allow_html=True
                    )
        st.markdown("---")


# ─────────────────────────────────────────────────────────────────────
# Song tab
# ─────────────────────────────────────────────────────────────────────

VIEWER_HEIGHT = 720

def render_song_tab(slug: str, title: str):
    folder = SONGS_DIR / slug

    st.markdown(f"### {title}")

    col_lyrics, col_tab = st.columns([1, 1], gap="large")

    # LEFT: lyrics
    with col_lyrics:
        st.markdown("**Lyrics**")
        lyrics_path = folder / "lyrics.txt"
        lyrics_text = lyrics_path.read_text(encoding="utf-8") if lyrics_path.exists() else ""
        with st.container(height=VIEWER_HEIGHT, border=True):
            st.markdown(lyrics_to_html(lyrics_text), unsafe_allow_html=True)

    # RIGHT: tab file
    with col_tab:
        st.markdown("**Picking / Chords**")
        tab_file = find_tab_file(folder)

        if tab_file is None:
            with st.container(height=VIEWER_HEIGHT, border=True):
                st.info(
                    "No tab file yet. Add a `tab.pdf`, `tab.jpg`, or `tab.png` "
                    f"into `songs/{slug}/` in your repo to populate this side."
                )
            return

        ext = tab_file.suffix.lower()

        if ext == ".pdf":
            num_pages = get_pdf_page_count(str(tab_file))
            page_key = f"page_{slug}"
            if page_key not in st.session_state:
                st.session_state[page_key] = 0

            # Clamp in case the file was changed
            st.session_state[page_key] = max(
                0, min(st.session_state[page_key], num_pages - 1)
            )
            current = st.session_state[page_key]

            with st.container(height=VIEWER_HEIGHT, border=True):
                image = render_pdf_page(str(tab_file), current)
                st.image(image, use_container_width=True)

            # Bottom navigation — only if more than one page
            if num_pages > 1:
                nav_l, nav_c, nav_r = st.columns([1, 2, 1])
                with nav_l:
                    if st.button("◀ Prev", key=f"prev_{slug}",
                                 disabled=(current == 0),
                                 use_container_width=True):
                        st.session_state[page_key] -= 1
                        st.rerun()
                with nav_c:
                    st.markdown(
                        f"<div style='text-align:center;padding-top:6px;"
                        f"color:#666;font-size:0.9em'>"
                        f"Page {current + 1} of {num_pages}</div>",
                        unsafe_allow_html=True
                    )
                with nav_r:
                    if st.button("Next ▶", key=f"next_{slug}",
                                 disabled=(current == num_pages - 1),
                                 use_container_width=True):
                        st.session_state[page_key] += 1
                        st.rerun()

        else:  # jpg / jpeg / png
            with st.container(height=VIEWER_HEIGHT, border=True):
                st.image(str(tab_file), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='margin-bottom:0'>🎵 Ukulele Songbook</h1>"
    "<p style='color:#777;margin-top:4px'>Personal practice app</p>",
    unsafe_allow_html=True,
)

tab_labels = ["Chords"] + [title for _, title in SONGS]
tabs = st.tabs(tab_labels)

with tabs[0]:
    render_chords_tab()

for i, (slug, title) in enumerate(SONGS):
    with tabs[i + 1]:
        render_song_tab(slug, title)

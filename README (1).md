# 汉字卡 — HSK Flashcards

A static flashcard site for Mandarin Chinese: **all 4,993 words of HSK 1–6**, each with pinyin, an English meaning, and an example sentence with its own pinyin and translation.

- Spaced-repetition review queue (Again / Hard / Good / Easy)
- Recognition (汉 → EN) and recall (EN → 汉) directions
- Audio via your browser's Chinese speech voice
- Searchable word list
- Progress saved in the browser; **works offline** once loaded
- No build step, no dependencies, no tracking

## Deploy to GitHub Pages

1. Create a repository and copy these files into its root.
2. Commit and push to the `main` branch.
3. In the repo: **Settings → Pages → Build and deployment**, set **Source** to *Deploy from a branch*, branch `main`, folder `/ (root)`. Save.
4. Wait a minute; your site is live at `https://USERNAME.github.io/REPO/`.

A workflow is also included at `.github/workflows/deploy.yml` if you prefer **Source: GitHub Actions** instead. Either method works — use one, not both.

### After your first deploy

Open `index.html` and replace the two `USERNAME`/`REPO` placeholders in the `<link rel="canonical">` and `og:url` tags with your real URL. Everything else uses relative paths, so it works at any subpath.

## Running locally

Because of the service worker, open it through a web server rather than double-clicking:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

Opening `index.html` directly from disk also works (the data loads via a `<script>` tag, not `fetch`), but offline caching stays off.

## Files

| File | Purpose |
|---|---|
| `index.html` | The whole app — markup, styles, and logic |
| `vocab.js` | The deck: `window.VOCAB`, 4,993 entries |
| `sw.js` | Service worker for offline use |
| `manifest.webmanifest` | Makes the site installable on phones |
| `icon-*.png` | App icons |
| `.nojekyll` | Stops GitHub Pages running Jekyll over the files |

## Editing the deck

`vocab.js` is one array. Each entry:

```js
{"l":3,"h":"经常","p":"jīng cháng","m":"often",
 "s":"我经常去那家饭馆。","sp":"Wǒ jīngcháng qù nà jiā fànguǎn.",
 "st":"I often go to that restaurant."}
```

`l` = HSK level, `h` = characters, `p` = pinyin, `m` = meaning, `s` = example sentence, `sp` = sentence pinyin, `st` = sentence translation. Add or edit entries freely — the app reads the array as-is.

**After changing `vocab.js`, bump the `CACHE` constant in `sw.js`** (e.g. `hsk-cards-v1` → `hsk-cards-v2`). Otherwise returning visitors keep the cached old copy.

## Customising

All colours are CSS custom properties at the top of `index.html`:

```css
--slate   /* page background */
--paper   /* card surface   */
--jade    /* accent         */
--cinnabar/* the HSK seal   */
```

## Credit and licence

Word list derived from the MIT-licensed [clem109/hsk-vocabulary](https://github.com/clem109/hsk-vocabulary) dataset (HSK 2.0 standard). Example sentences and the app are yours to use and modify.

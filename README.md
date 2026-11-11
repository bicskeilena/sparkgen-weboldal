# SparkGen Studio – sparkgen.hu

Bicskei Léna Magdolna e.v. weboldala. Statikus oldal, GitHub Pages-en fut (`docs/` mappa, `main` ág).

- `index.html` – főoldal forrása (claude.ai artifact-előnézettel is működik)
- `legal/` – adatkezelési tájékoztató és impresszum tartalma
- `img/`, `fonts/`, `static/` – képek, saját tárhelyről kiszolgált betűtípusok, ikonok
- `logo/` – logófájlok (SVG, PNG)
- `build_deploy.py` – legenerálja a kész oldalt a `docs/` mappába

Frissítés: `python3 build_deploy.py`, majd commit + push a `main` ágra.

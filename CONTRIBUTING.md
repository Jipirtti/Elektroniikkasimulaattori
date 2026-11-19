# Kehitysohjeet

Elektroniikkasimulaattoria kehitetään avoimesti Seinäjoen ammattikorkeakoulussa (SEAMK). Muutokset ja palaute ovat tervetulleita.

## Periaatteet

- Simulaattori on yksi tiedosto (`index.html`) ilman ulkoisia kirjastoja ja käännösvaihetta.
- Fysiikkaa koskeva muutos vaatii testin (`tests/test_validointi.py`) ja rivin tiedostoon `VALIDOINTI.md`. Muutetun ilmiön opettajan validoinnin tila palautetaan arvoon *Ei validoitu*.
- Testien odotusarvot lasketaan testissä itsenäisesti komponenttien parametreista oppikirjan kaavalla. Testi ei saa käyttää simulaattorin omia välituloksia odotusarvona.

## Koodin rakenne (index.html)

| Osa | Sisältö |
| --- | --- |
| `TY` | Komponenttityypit: liitännät, parametrit, piirrosmerkki ja MNA-elementit (`elems`) |
| `IDEAL`, `SIMPLE_SHOW` | Yksinkertaisen mallin ihanteelliset arvot ja näytettävät parametrit |
| `rebuild`, `stepSim`, `commit` | Topologia, kerroinmatriisi, aika-askel ja kytkentätilojen iterointi |
| `accumulate` | Mittausikkunat, tehot ja harmoniset |
| `drawScope`, `feedProbe` | Oskilloskooppi |
| `EX` | Esimerkkipiirit |
| `window.ElSim` | Testirajapinta |

### Uusi komponentti

1. Lisää tyyppi `TY`-olioon: `ports`, `prm`, `def`, `init`, `elems`, `draw` ja tarvittaessa `dyn`, `read`, `cur`, `vp`.
2. Elementtityypit: `R` (resistanssi), `C` (kapasitanssi, alkujännite `U0`), `L` (induktanssi, alkuvirta `I0`), `V` (jännitelähde, `v(t)`), `X` (ihanteellinen muuntaja, `nr`), `S` (paloittain lineaarinen kytkin: `kind` = `d`, `scr`, `igbt`, `ch` tai `man`, `Ron`, `Vf`).
3. Lisää yksinkertaisen mallin arvot `IDEAL`-olioon ja näkyvät parametrit `SIMPLE_SHOW`-olioon.
4. Lisää komponentti palettiin (`PAL`) ja testiin `tests/test_kieli.py` (`TYPES`).

### Käännökset

Kaikki tekstit kirjoitetaan muodossa `tr('suomeksi', 'in English')` tai parametreissa `['suomeksi', 'in English']`. Staattisessa HTML:ssä käytetään `data-en`-, `data-en-title`- ja `data-en-aria`-attribuutteja. Testi K01 varmistaa, ettei englanninkielisessä näkymässä ole suomea.

## Testit

```bash
pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest tests -v
```

## Palaute

Käytä issue-malleja (Fysiikka ei vastaa odotusta, Virheilmoitus, Kehitysehdotus) tai Discussions-osiota. Liitä piiri JSON-muodossa (Tallenna / lataa), jotta tilanne voidaan toistaa.

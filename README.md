# Elektroniikkasimulaattori / Electronics Simulator

[![Validointi](../../actions/workflows/validointi.yml/badge.svg)](../../actions/workflows/validointi.yml)

Selaimessa toimiva opetussimulaattori DC- ja AC-piireille ja tehoelektroniikalle. Piiri rakennetaan vetämällä komponentteja piirtoalustalle ja kytkemällä niiden liitännät johtimilla. Jännitteitä ja virtoja mitataan nelikanavaisella oskilloskoopilla, jossa on liipaisu ja mittaustaulukko. Jokaisen komponentin parametrit voi asettaa, ja komponentin mitatut arvot (keskiarvo, tehollisarvo, teho, tehokerroin, THD) näkyvät ominaisuuspaneelissa.

**Kokeile:** <https://jipirtti.github.io/Elektroniikkasimulaattori/> tai avaa `index.html` suoraan selaimessa. Asennusta tai palvelinta ei tarvita.

**Kieli / Language:** käyttöliittymä on suomeksi ja englanniksi. Kieltä vaihdetaan yläpalkin FI | EN -valitsimella lennosta. Suora linkki englanninkieliseen versioon: `?lang=en`. The user interface is available in Finnish and English; switch with the FI | EN toggle or use `?lang=en`.

**Malli / Model:** yläpalkin Yksinkertainen | Kehittynyt -valitsimella vaihdetaan simulointimallia lennosta. Yksinkertaisessa mallissa komponentit ovat ihanteellisia, joten tulos vastaa suoraan oppikirjan kaavoja. Kehittynyt malli sisältää kynnysjännitteet, johtotilan resistanssit, lähteen impedanssin (kommutointi), ESR:n, käämiresistanssit, muuntajan hajainduktanssin ja kuolleen ajan. Linkki: `?malli=yksinkertainen` tai `?mode=simple`. Choose Simple (ideal components) or Advanced (real components) in the header.

Tekijä: Juho Pirttilahti, Seinäjoen ammattikorkeakoulu (SEAMK), 2026. Suunnittelu, sisältö ja validointi: Juho Pirttilahti. Ohjelmakoodi toteutettu tekoälyavusteisesti (Claude, Anthropic). Lisenssi: [CC BY 4.0](LICENSE).

## Ominaisuudet

- 16 komponenttia: DC-, AC- ja kolmivaihelähde, maa, vastus, kondensaattori, kela, muuntaja, kytkin, diodi, tyristori, MOSFET, IGBT, DC-moottori sekä jännite- ja virtamittari.
- Hilaohjaus MOSFETille ja IGBT:lle: PWM (taajuus, pulssisuhde, vaihe) ja sini-PWM (kantoaalto, lähtötaajuus, modulaatioindeksi, vaihe), käänteinen ohjaus ja kuollut aika. Tyristorin ohjauskulma luonnollisesta kommutointihetkestä.
- Nelikanavainen oskilloskooppi: aikataso 1 µs–5 s/div, liipaisu (kanava, taso, reuna; Auto, Normaali, Kerta, Vapaa), kanavakohtainen asteikko ja siirto, mittaustaulukko (keskiarvo, tehollisarvo, ääriarvot, huipusta huippuun, taajuus).
- Komponenttien mitatut arvot jaksoittain: keskiarvot, tehollisarvot ja teho; AC-lähteistä pätöteho, näennäisteho, loisteho, tehokerroin, siirtymätehokerroin ja virran THD.
- 13 esimerkkipiiriä: jännitteenjako ja RC-lataus, RLC-sarjapiiri, 1- ja 3-vaiheiset diodi- ja tyristorisillat, buck-, boost- ja buck-boost-hakkuri, H-silta- ja kolmivaihe-invertteri sini-PWM:llä, muuntajateholähde ja DC-moottori katkojalla.
- Piirin muokkaus kuten hydrauliikkasimulaattorissa: johtimien reitin veto, laatikkovalinta, ryhmäsiirto, kopioi ja liitä, kumoa, tallennus selaimeen ja tekstinä.

## Dokumentaatio

| Tiedosto | Sisältö |
| --- | --- |
| [docs/kayttoohje.md](docs/kayttoohje.md) | Käyttöohje, esimerkit odotettuine arvoineen ja harjoitustehtävät. Verkkosivuna: <https://jipirtti.github.io/Elektroniikkasimulaattori/docs/kayttoohje.html> |
| [VALIDOINTI.md](VALIDOINTI.md) | Validoitavat ilmiöt, käsinlaskukaavat ja opettajan validoinnin tila |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Kehitysohjeet, testien ajaminen ja palautteen antaminen |
| [CHANGELOG.md](CHANGELOG.md) | Versiohistoria |

## Validointi

Simulaattorin ilmiöt validoidaan kahdella tasolla, ks. [VALIDOINTI.md](VALIDOINTI.md):

- **Automaattisesti:** validointitestit (`tests/test_validointi.py`, E01–E22) vertaavat simulaattorin tuloksia oppikirjan kaavoihin, esimerkiksi Ud = 3√2/π·U, Uo = D·Ui ja Û1 = ma·Udc. Mallitestit (M01–M05), kielitestit (K01–K04) ja käyttöliittymätestit (U01–U05) täydentävät niitä. GitHub Actions ajaa testit jokaisesta muutoksesta ja maanantaisin ajastetusti. Jos ajastettu ajo epäonnistuu, siitä avautuu automaattisesti issue.
- **Opettajan validointi:** jokainen ilmiö tarkistetaan käsinlaskulla, kirjallisuudesta tai laboratoriomittauksella ja kirjataan validoiduksi. Validointikierros avautuu issueksi automaattisesti 15.1. ja 15.8.

Testien ajaminen omalla koneella:

```bash
pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest tests -v
```

## Palaute

- **Fysiikka ei vastaa odotusta:** avaa issue mallilla *Fysiikka ei vastaa odotusta* ja liitä piiri JSON-muodossa (simulaattorin Tallenna / lataa).
- **Virhe käyttöliittymässä:** mallilla *Virheilmoitus*.
- **Ideat ja kysymykset:** Discussions-osio tai malli *Kehitysehdotus*.

## Rakenne

```
index.html                  Simulaattori (yksi tiedosto, ei riippuvuuksia eikä käännösvaihetta)
docs/                       Käyttöohje (markdown) ja kuvat
tools/rakenna_ohje.py       Rakentaa käyttöohjeen HTML-sivun julkaisun yhteydessä
tests/                      Validointitestit (pytest + Playwright)
VALIDOINTI.md               Validointisuunnitelma ja -tila
.github/workflows/          Validointi, validointikierros ja GitHub Pages -julkaisu
.github/ISSUE_TEMPLATE/     Palautelomakkeet
```

## Lisenssi

Simulaattori ja käyttöohje on lisensoitu [Creative Commons Nimeä 4.0 Kansainvälinen -lisenssillä (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.fi). Saat kopioida, jakaa ja muokata aineistoa mihin tahansa tarkoitukseen, kunhan mainitset tekijän ja oppilaitoksen, merkitset lisenssin ja kerrot tekemistäsi muutoksista.

Suositeltu viittaus: Pirttilahti, J. (2026). *Elektroniikkasimulaattori ja käyttöohje.* Seinäjoen ammattikorkeakoulu. CC BY 4.0.

# Muutosloki

## Julkaisematon

- Kopioi kuva: kuvan otsikko ja PNG-tiedoston nimi valitulla kielellä (aiemmin piirikaavion ja oskilloskoopin otsikko jäi suomeksi englannin- ja saksankielisessä kuvassa). Uusi testi KV10 tarkistaa, että jokaisen kaavion kuvassa on vain valitun kielen tekstejä.
- Saksankielinen käyttöliittymä (FI | EN | DE -valitsin, `?lang=de`, selaimen kieli de). Termit tarkistettu saksalaisista standardeista ja alan termistöstä. Kielitestit tarkistavat, ettei saksankielisessä näkymässä ole kääntämättömiä rivejä.
- Käyttöohje englanniksi (`docs/user-manual.md`) ja saksaksi (`docs/bedienungsanleitung.md`) omilla kuvakaappauksilla (`docs/kuvat/en/`, `docs/kuvat/de/`). `tools/rakenna_ohje.py` rakentaa kaikki kolme HTML-sivua, ja simulaattorin Käyttöohje-linkki avaa valitun kielen ohjeen.
- Kopioi kuva -painike jokaiseen kaavioon: kaavio leikepöydälle PNG-kuvana vaalealla taustalla ja kaksinkertaisella tarkkuudella, otsikon, selitteen ja lähdemerkinnän kanssa. Jos selain estää kopioinnin, kuva avautuu ikkunaan tallennettavaksi. Yhteinen SimKuva-moduuli kaikissa simulaattoreissa. Testit KV01–KV04.
- Palautekanava: yläpalkin *Palaute*-painike avaa lomakkeen (fysiikka / virhe / kehitysehdotus), joka avaa valmiiksi täytetyn GitHub-issuen repon lomakepohjalla. Mukaan liitetään automaattisesti piiri (Tallenna / lataa -muoto), versio, malli, kieli, selain ja varoitukset. Jos piiri ei mahdu linkkiin, se kopioidaan leikepöydälle. Varareitit ilman GitHub-tiliä: Kopioi raportti ja Lähetä sähköpostilla. Lomakkeen ollessa auki simulaattorin pikanäppäimet eivät toimi. Uudet testit P01–P07 (`tests/test_palaute.py`).

## 1.0.0 – 2026-11-18

- Ensimmäinen julkaisu: DC- ja AC-piirit ja tehoelektroniikka selaimessa.
- Ratkaisija: muunneltu solmupistemenetelmä (MNA), implisiittinen Euler, paloittain lineaariset puolijohteet ja kytkentätilojen iterointi, LU-hajotelmien välimuisti.
- 16 komponenttia, MOSFETin ja IGBT:n PWM- ja sini-PWM-hilaohjaus, tyristorin ohjauskulma, DC-moottori.
- Nelikanavainen oskilloskooppi liipaisulla ja mittaustaulukolla; komponenttien keskiarvot, tehollisarvot, teho, tehokerroin ja THD.
- Yksinkertainen ja kehittynyt malli, suomi ja englanti.
- 13 esimerkkipiiriä, käyttöohje ja harjoitustehtävät.
- Validointitestit E01–E22, mallitestit M01–M05, kielitestit K01–K04 ja käyttöliittymätestit U01–U05.

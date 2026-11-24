# Muutosloki

## Julkaisematon

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

# Validointisuunnitelma

Simulaattorin ilmiöt validoidaan kahdella tasolla:

1. **Automaattinen regressiovalidointi:** testit `tests/` vertaavat simulaattorin tulosta kaavaan, jonka testi laskee itsenäisesti komponenttien parametreista. GitHub Actions ajaa testit jokaisesta muutoksesta ja maanantaisin.
2. **Opettajan validointi:** vastuuopettaja tarkistaa jokaisen ilmiön käsinlaskulla, kirjallisuudesta tai laboratoriomittauksella ja kirjaa tuloksen tähän tiedostoon (päivämäärä, validoija, menetelmä). Validointikierros avautuu issueksi automaattisesti 15.1. ja 15.8.

Kun simulaattorin fysiikkaa muutetaan, muutoksen koskemat rivit palautetaan tilaan *Ei validoitu*.

Testit E01–E19 ja E22 ajetaan yksinkertaisella mallilla (ihanteelliset komponentit), E20 ja E21 kehittyneellä mallilla. Odotetut arvot ovat esimerkkipiirien oletusarvoilla.

## A. Automaattisesti testatut ilmiöt (tests/test_validointi.py)

| ID | Ilmiö | Piiri ja toimenpide | Käsinlaskukaava | Odotettu (oletus) | Tol. | Opettajan validointi |
| --- | --- | --- | --- | --- | --- | --- |
| E01 | Jännitteenjako | Esim. 1, 0,6 s | U2 = U·R2 / (R1 + R2) | 6,00 V | 0,2 % | Ei validoitu |
| E02 | RC-lataus | Esim. 1, t = τ | u(τ) = U∞(1 − e⁻¹), τ = (R1∥R2)·C | 3,79 V (τ = 50 ms) | 0,5 % | Ei validoitu |
| E03 | RL-piirin virta | 10 V, 10 Ω, 100 mH, t = τ | i(τ) = (U/R)(1 − e⁻¹), τ = L/R | 0,632 A | 0,5 % | Ei validoitu |
| E04 | RLC-sarjapiiri | Esim. 2 | I = U/|Z|, P = I²R, cos φ = R/|Z| | 12,1 A; 1,47 kW; 0,527 | 1–1,5 % | Ei validoitu |
| E05 | Sarjaresonanssi | Esim. 2, C = 1/(ω²L) | I = U/R | 23,0 A | 1,5 % | Ei validoitu |
| E06 | 1-vaiheinen diodisilta, R-kuorma | 230 V, 100 Ω | Ud = 2√2/π·U | 207 V | 0,5 % | Ei validoitu |
| E07 | Suodatinkondensaattorin rippeli | Esim. 3 | ΔU = Id·(T/2 − t_v)/C | 2,7 V | 5 % | Ei validoitu |
| E08 | 1-vaiheinen tyristorisilta, R-kuorma | 230 V, 100 Ω, α = 60° | Ud = 0,9·U·(1 + cos α)/2 | 155 V | 1 % | Ei validoitu |
| E09 | 1-vaiheinen tyristorisilta, jatkuva virta | Esim. 4, α = 60° | Ud = 0,9·U·cos α | 103,5 V | 1,5 % | Ei validoitu |
| E10 | 3-vaiheinen diodisilta B6 | Esim. 5 | Ud = 3√2/π·U | 540 V | 0,3 % | Ei validoitu |
| E11 | 3-vaiheinen tyristorisilta B6C | Esim. 6, α = 30° | Ud = 3√2/π·U·cos α | 468 V | 1,5 % | Ei validoitu |
| E12 | Buck-hakkuri | Esim. 7 | Uo = D·Ui, ΔIL = Ui·D(1 − D)/(L·fs) | 24,0 V; 2,73 A | 1 % / 3 % | Ei validoitu |
| E13 | Boost-hakkuri | Esim. 8 | Uo = Ui/(1 − D) | 24,0 V | 1,5 % | Ei validoitu |
| E14 | Buck-boost-hakkuri | Esim. 9 | Uo = −D/(1 − D)·Ui | −18,0 V | 1,5 % | Ei validoitu |
| E15 | H-siltainvertteri, sini-PWM | Esim. 10 | Û1 = ma·Udc | 240 V | 1,5 % | Ei validoitu |
| E16 | Kolmivaiheinvertteri, sini-PWM | Esim. 11 | U12,1 = √3/(2√2)·ma·Udc | 274 V | 1,5 % | Ei validoitu |
| E17 | Muuntaja | Esim. 12 | U2/U1 = N2/N1, I1/I2 = N2/N1 | 0,104 | 0,2 % / 0,5 % | Ei validoitu |
| E18 | DC-moottori katkojalla | Esim. 13 | I = TL/kΦ, ω = (D·U − Ra·I)/kΦ | 2,00 A; 220 rad/s | 1 % | Ei validoitu |
| E19 | Häviöttömän hakkurin tehotase | Esim. 7 | P_in = P_out | 57,6 W | 1,5 % | Ei validoitu |
| E20 | Diodin kynnysjännite (kehittynyt) | 10 V, diodi, 100 Ω | I = (U − UF0)/(R + rD) | 93,0 mA | 0,1 % | Ei validoitu |
| E21 | Kommutointi (kehittynyt) | B6, Lk = 2 mH, RL-kuorma | Ud = 3√2/π·U − 3ωLk·Id/π | 532 V | 1 % | Ei validoitu |
| E22 | Oskilloskoopin mittaukset | Esim. 2, CH1 | U (rms), 2√2·U (huipusta huippuun), f | 230 V; 651 V; 50 Hz | 1 % | Ei validoitu |

## A2. Mallitestit (tests/test_malli.py)

| ID | Ilmiö | Piiri ja toimenpide | Odotus | Opettajan validointi |
| --- | --- | --- | --- | --- |
| M01 | Ihanteellinen diodi (yksinkertainen) | 10 V, diodi, 100 Ω | I = U/R = 100 mA | Ei validoitu |
| M02 | Lähteen sisäinen resistanssi (kehittynyt) | 12 V, Rs 0,5 Ω, 5,5 Ω | I = U/(R + Rs) = 2,00 A | Ei validoitu |
| M03 | Mallin vaihto säilyttää parametrit | Esim. 3, D1 UF0 = 0,95 V | Yksinkertaisessa 0 V, takaisin vaihdettaessa 0,95 V | Ei validoitu |
| M04 | Kynnysjännitteiden vaikutus diodisillassa | 230 V, UF0 = 1 V, R-kuorma | ΔUd ≈ 2·UF0 | Ei validoitu |
| M05 | Kuollut aika | Esim. 7, td = 5 µs | Johtoaika lyhenee: D − td·fs | Ei validoitu |

## B. Laadulliset ilmiöt (opettajan validointi)

| ID | Ilmiö | Piiri ja toimenpide | Odotettu havainto | Opettajan validointi |
| --- | --- | --- | --- | --- |
| L01 | Kelan virran katkaisu | Esim. 7, poista diodi D1 ja kytke Q1.S suoraan kelaan | Q1:n jännite nousee kilovolttiluokkaan; varoitus jännitepiikistä ja ylijännitteestä | Ei validoitu |
| L02 | Epäjatkuva virta buck-hakkurissa | Esim. 7, R1 = 100 Ω | Kelan virta käy nollassa, Uo > D·Ui | Ei validoitu |
| L03 | Tyristorisilta, α > 90° | Esim. 4, α = 120° | Passiivisella RL-kuormalla virta muuttuu epäjatkuvaksi ja Ud putoaa lähelle nollaa; jatkuvalla virralla (aktiivinen kuorma) Ud olisi negatiivinen | Ei validoitu |
| L04 | Kommutointilovet | Esim. 6, kehittynyt malli, Ls = 2 mH | Lovet vaihejännitteessä ja tasajännitteessä kommutoinnin aikana | Ei validoitu |
| L05 | Diodisillan virran harmoniset | Esim. 3 | Virta pulsseina; THD selvästi yli 100 % | Ei validoitu |
| L06 | Kapasitiivinen loisteho | Esim. 2 | Virta edellä jännitettä, Q1 < 0 | Ei validoitu |
| L07 | Moottorin käynnistysvirta | Esim. 13, nollaa tila | Virta suurimmillaan käynnistyksessä, laskee nopeuden kasvaessa | Ei validoitu |
| L08 | Muuntajan magnetointivirta (kehittynyt) | Esim. 12, irrota kuorma | Ensiövirta pieni, jäljessä jännitteestä noin 90° | Ei validoitu |

## C. Rajaukset

Seuraavia ilmiöitä malli ei kuvaa, joten niitä ei validoida: kytkentähäviöt ja kytkentätransientit (puolijohteiden kapasitanssit, takavirta), muuntajan kyllästyminen ja hystereesi, lämpeneminen, komponenttien toleranssit ja ikääntyminen, johtimien resistanssi ja induktanssi, sähkömagneettiset häiriöt.

"""Fysiikan validointitestit E01–E22.

Jokainen testi ajaa piirin simulaattorissa ja vertaa tulosta oppikirjan kaavaan, joka lasketaan
tässä tiedostossa itsenäisesti komponenttien parametreista. Ellei toisin mainita, testit ajetaan
yksinkertaisella mallilla (ihanteelliset komponentit), jolloin kaavat ovat tarkkoja.
Tunnisteet vastaavat tiedoston VALIDOINTI.md taulukkoa.
"""
import math
import pytest
from conftest import circuit

SQ2, SQ3 = math.sqrt(2), math.sqrt(3)


def par(sim, label):
    return sim.call("param", label)


# ---------------------------------------------------------------- DC-piirit
def test_E01_jannitteenjako(sim, check):
    sim.call("loadExample", "ex1"); sim.call("run", 0.6)
    U, R1, R2 = par(sim, "U1")["U"], par(sim, "R1")["R"], par(sim, "R2")["R"]
    check("E01", "Jännitteenjako U2 = U·R2 / (R1 + R2)", sim.call("v", "C1"), U * R2 / (R1 + R2), 0.002, "V")


def test_E02_rc_aikavakio(sim, check):
    sim.call("loadExample", "ex1")
    U, R1, R2, C = par(sim, "U1")["U"], par(sim, "R1")["R"], par(sim, "R2")["R"], par(sim, "C1")["C"] * 1e-6
    tau = (R1 * R2 / (R1 + R2)) * C
    sim.call("run", tau)
    check("E02", "RC-lataus u(τ) = U∞·(1 − e⁻¹), τ = (R1∥R2)·C", sim.call("v", "C1"), U * R2 / (R1 + R2) * (1 - math.exp(-1)), 0.005, "V")


def test_E03_rl_aikavakio(sim, check):
    sim.call("loadCircuit", circuit([("c1", "vdc", {"U": 10}, "U1"), ("c2", "r", {"R": 10}, "R1"), ("c3", "l", {"L": 100}, "L1"), ("c4", "gnd", {}, "G")],
                                    [("c1:p", "c2:1"), ("c2:2", "c3:1"), ("c3:2", "c1:n"), ("c1:n", "c4:0")]))
    tau = 0.1 / 10
    sim.call("run", tau)
    check("E03", "RL-piirin virta i(τ) = (U/R)·(1 − e⁻¹), τ = L/R", sim.call("i", "L1"), 1.0 * (1 - math.exp(-1)), 0.005, "A")


def test_E20_diodin_kynnysjannite(sim, check):
    """Kehittynyt malli: I = (U − UF0) / (R + rD)."""
    sim.call("setMode", "advanced")
    sim.call("loadCircuit", circuit([("c1", "vdc", {"U": 10, "Rs": 0}, "U1"), ("c2", "d", {"Vf": 0.7, "Ron": 10}, "D1"), ("c3", "r", {"R": 100}, "R1"), ("c4", "gnd", {}, "G")],
                                    [("c1:p", "c2:A"), ("c2:K", "c3:1"), ("c3:2", "c1:n"), ("c1:n", "c4:0")]))
    sim.call("run", 0.01)
    check("E20", "Diodin kynnysjännite: I = (U − UF0) / (R + rD)", sim.call("i", "R1"), (10 - 0.7) / (100 + 0.01), 0.001, "A")


# ---------------------------------------------------------------- AC-piirit
def _rlc(sim):
    U, f = par(sim, "U1")["U"], par(sim, "U1")["f"]
    R, L, C = par(sim, "R1")["R"], par(sim, "L1")["L"] / 1000, par(sim, "C1")["C"] * 1e-6
    w = 2 * math.pi * f
    Z = math.hypot(R, w * L - 1 / (w * C))
    return U, R, Z


def test_E04_rlc_virta_ja_teho(sim, check):
    sim.call("loadExample", "ex2"); sim.call("run", 0.3)
    U, R, Z = _rlc(sim)
    m = sim.call("measure", "R1", "I", None, 0.02)
    check("E04a", "RLC-sarjapiiri: I = U / |Z|", m["rms"], U / Z, 0.01, "A")
    sim.call("run", 0.02)
    s = sim.call("source", "U1")
    check("E04b", "Pätöteho P = I²·R", s["P"], (U / Z) ** 2 * R, 0.015, "W")
    check("E04c", "Tehokerroin cos φ = R / |Z|", s["PF"], R / Z, 0.015, "")


def test_E05_resonanssi(sim, check):
    sim.call("loadExample", "ex2")
    f, L = par(sim, "U1")["f"], par(sim, "L1")["L"] / 1000
    C = 1 / ((2 * math.pi * f) ** 2 * L)
    sim.call("setParam", "C1", "C", C * 1e6); sim.call("reset"); sim.call("run", 0.6)
    m = sim.call("measure", "R1", "I", None, 0.02)
    check("E05", "Sarjaresonanssi f0 = 1/(2π√(LC)): I = U / R", m["rms"], par(sim, "U1")["U"] / par(sim, "R1")["R"], 0.015, "A")


# ---------------------------------------------------------------- tasasuuntaajat
def _bridge1(kind, p, load):
    comps = [("c1", "vac", {"U": 230, "f": 50}, "U1")] + [(f"c{i+2}", kind, p, f"V{i+1}") for i in range(4)] + load + [("c9", "gnd", {}, "G")]
    wires = [("c1:L", "c2:A"), ("c2:A", "c3:K"), ("c1:N", "c4:A"), ("c4:A", "c5:K"), ("c2:K", "c4:K"), ("c3:A", "c5:A"), ("c3:A", "c9:0")]
    return comps, wires


def test_E06_diodisilta_1v(sim, check):
    comps, wires = _bridge1("d", {}, [("c6", "r", {"R": 100}, "R1")])
    sim.call("loadCircuit", circuit(comps, wires + [("c2:K", "c6:1"), ("c6:2", "c3:A")]))
    sim.call("run", 0.04)
    m = sim.call("measure", "R1", "U", None, 0.1)
    check("E06", "1-vaiheinen diodisilta: Ud = 2√2/π·U", m["avg"], 2 * SQ2 / math.pi * 230, 0.005, "V")


def test_E07_suodatinkondensaattorin_rippeli(sim, check):
    """Kondensaattori purkautuu kuormaan tasavirralla Id ajan t_p = T/2 − t_v, jossa t_v on latausaika
    (jännite nousee sinin mukana minimistä huippuun): ΔU = Id·t_p / C."""
    sim.call("loadExample", "ex3"); sim.call("run", 0.5)
    m = sim.call("measure", "R1", "U", None, 0.04)
    U, f, C, R = par(sim, "U1")["U"], par(sim, "U1")["f"], par(sim, "C1")["C"] * 1e-6, par(sim, "R1")["R"]
    t_v = (math.pi / 2 - math.asin(m["min"] / (SQ2 * U))) / (2 * math.pi * f)
    check("E07", "Suodatinkondensaattorin rippeli ΔU = Id·(T/2 − t_v) / C", m["max"] - m["min"], (m["avg"] / R) * (1 / (2 * f) - t_v) / C, 0.05, "V")


def test_E08_tyristorisilta_r_kuorma(sim, check):
    a = 60
    comps, wires = _bridge1("scr", {"ctl": "kulma", "alpha": a, "f": 50}, [("c6", "r", {"R": 100}, "R1")])
    sim.call("loadCircuit", circuit(comps, wires + [("c2:K", "c6:1"), ("c6:2", "c3:A")]))
    sim.call("run", 0.06)
    m = sim.call("measure", "R1", "U", None, 0.1)
    check("E08", "1-vaiheinen tyristorisilta, R-kuorma: Ud = 0,9·U·(1 + cos α)/2", m["avg"], 2 * SQ2 / math.pi * 230 * (1 + math.cos(math.radians(a))) / 2, 0.01, "V")


def test_E09_tyristorisilta_rl_kuorma(sim, check):
    sim.call("loadExample", "ex4"); sim.call("run", 1.0)
    a, R = par(sim, "Th1")["alpha"], par(sim, "R1")["R"]
    m = sim.call("measure", "R1", "I", None, 0.1)
    check("E09", "1-vaiheinen tyristorisilta, jatkuva virta: Ud = 0,9·U·cos α", m["avg"] * R, 2 * SQ2 / math.pi * par(sim, "U1")["U"] * math.cos(math.radians(a)), 0.015, "V")


def test_E10_diodisilta_3v(sim, check):
    sim.call("loadExample", "ex5"); sim.call("run", 0.06)
    m = sim.call("measure", "R1", "U", None, 0.1)
    check("E10", "3-vaiheinen diodisilta B6: Ud = 3√2/π·U", m["avg"], 3 * SQ2 / math.pi * par(sim, "U1")["U"], 0.003, "V")


def test_E11_tyristorisilta_3v(sim, check):
    sim.call("loadExample", "ex6"); sim.call("run", 1.0)
    a, R = par(sim, "Th1")["alpha"], par(sim, "R1")["R"]
    m = sim.call("measure", "R1", "I", None, 0.1)
    check("E11", "3-vaiheinen tyristorisilta B6C: Ud = 3√2/π·U·cos α", m["avg"] * R, 3 * SQ2 / math.pi * par(sim, "U1")["U"] * math.cos(math.radians(a)), 0.015, "V")


def test_E21_kommutointi(sim, check):
    """Kehittynyt malli: lähteen induktanssi Lk aiheuttaa kommutointihäviön ΔUd = 3ωLk·Id/π (B6, tasainen Id)."""
    sim.call("setMode", "advanced")
    Lk, U, f = 2.0, 400.0, 50.0
    comps = [("c1", "v3", {"U": U, "f": f, "Rs": 0, "Ls": Lk}, "U1")] + [(f"c{i+2}", "d", {"Vf": 0, "Ron": 0.01}, f"D{i+1}") for i in range(6)] + \
            [("c8", "r", {"R": 40}, "R1"), ("c9", "l", {"L": 2000, "rl": 0}, "L1"), ("c10", "gnd", {}, "G")]
    wires = [("c1:L1", "c2:A"), ("c1:L2", "c3:A"), ("c1:L3", "c4:A"), ("c2:A", "c5:K"), ("c3:A", "c6:K"), ("c4:A", "c7:K"),
             ("c2:K", "c3:K"), ("c3:K", "c4:K"), ("c5:A", "c6:A"), ("c6:A", "c7:A"), ("c2:K", "c8:1"), ("c8:2", "c9:1"), ("c9:2", "c5:A"), ("c5:A", "c10:0")]
    sim.call("loadCircuit", circuit(comps, wires)); sim.call("run", 1.5)
    Id = sim.call("measure", "R1", "I", None, 0.1)["avg"]
    Ud = Id * 40
    check("E21", "Kommutointi: Ud = 3√2/π·U − 3ωLk·Id/π", Ud, 3 * SQ2 / math.pi * U - 3 * 2 * math.pi * f * Lk / 1000 * Id / math.pi, 0.01, "V")


# ---------------------------------------------------------------- hakkurit
def test_E12_buck(sim, check):
    sim.call("loadExample", "ex7"); sim.call("run", 0.01)
    Ui, D, fs, L = par(sim, "U1")["U"], par(sim, "Q1")["D"] / 100, par(sim, "Q1")["f"] * 1000, par(sim, "L1")["L"] / 1000
    m = sim.call("measure", "R1", "U", None, 0.001)
    check("E12a", "Buck: Uo = D·Ui", m["avg"], D * Ui, 0.01, "V")
    il = sim.call("measure", "L1", "I", None, 0.001)
    check("E12b", "Buck: kelan virran rippeli ΔIL = Ui·D·(1 − D) / (L·fs)", il["max"] - il["min"], Ui * D * (1 - D) / (L * fs), 0.03, "A")


def test_E13_boost(sim, check):
    sim.call("loadExample", "ex8"); sim.call("run", 0.03)
    Ui, D = par(sim, "U1")["U"], par(sim, "Q1")["D"] / 100
    m = sim.call("measure", "R1", "U", None, 0.002)
    check("E13", "Boost: Uo = Ui / (1 − D)", m["avg"], Ui / (1 - D), 0.015, "V")


def test_E14_buck_boost(sim, check):
    sim.call("loadExample", "ex9"); sim.call("run", 0.03)
    Ui, D = par(sim, "U1")["U"], par(sim, "Q1")["D"] / 100
    m = sim.call("measure", "R1", "U", None, 0.002)
    check("E14", "Buck-boost: Uo = −D/(1 − D)·Ui", m["avg"], -D / (1 - D) * Ui, 0.015, "V")


def test_E19_tehotase(sim, check):
    sim.call("loadExample", "ex7"); sim.call("run", 0.01)
    pin = sim.call("measure", "U1", "I", None, 0.002)["avg"] * par(sim, "U1")["U"]
    m = sim.call("measure", "R1", "U", None, 0.002)
    check("E19", "Häviötön hakkuri: P_in = P_out", pin, m["rms"] ** 2 / par(sim, "R1")["R"], 0.015, "W")


# ---------------------------------------------------------------- vaihtosuuntaajat
def test_E15_h_silta(sim, check):
    sim.call("loadExample", "ex10"); sim.call("run", 0.1)
    ma, Udc, fm = par(sim, "Q1")["ma"], par(sim, "U1")["U"], par(sim, "Q1")["fm"]
    f = sim.call("fourier", "PV1", "U", None, fm, 2, 5)
    check("E15", "H-silta, bipolaarinen sini-PWM: perusaallon huippuarvo Û1 = ma·Udc", f["amp"][0], ma * Udc, 0.015, "V")


def test_E16_kolmivaihe_invertteri(sim, check):
    sim.call("loadExample", "ex11"); sim.call("run", 0.1)
    ma, Udc, fm = par(sim, "Q1")["ma"], par(sim, "U1")["U"], par(sim, "Q1")["fm"]
    f = sim.call("fourier", "PV1", "U", None, fm, 2, 5)
    check("E16", "3-vaiheinvertteri, sini-PWM: pääjännitteen perusaalto U12,1 = √3/(2√2)·ma·Udc", f["amp"][0] / SQ2, SQ3 / (2 * SQ2) * ma * Udc, 0.015, "V")


# ---------------------------------------------------------------- muuntaja ja moottori
def test_E17_muuntaja(sim, check):
    sim.call("loadExample", "ex12"); sim.call("run", 0.3)
    U1n, U2n = par(sim, "T1")["U1"], par(sim, "T1")["U2"]
    u1 = sim.call("measure", "T1", "U", "P", 0.02)["rms"]
    u2 = sim.call("measure", "T1", "U", "S", 0.02)["rms"]
    check("E17a", "Muuntaja: U2 / U1 = N2 / N1", u2 / u1, U2n / U1n, 0.002, "")
    i1 = sim.call("measure", "T1", "I", "P", 0.02)["rms"]
    i2 = sim.call("measure", "T1", "I", "S", 0.02)["rms"]
    check("E17b", "Muuntaja: I1 / I2 = N2 / N1", i1 / i2, U2n / U1n, 0.005, "")


def test_E18_dc_moottori(sim, check):
    sim.call("loadExample", "ex13"); sim.call("run", 1.2)
    p = par(sim, "M1"); U, D = par(sim, "U1")["U"], par(sim, "Q1")["D"] / 100
    I = p["TL"] / p["k"]
    check("E18a", "DC-moottori: ankkurivirta I = TL / kΦ", sim.call("measure", "M1", "I", None, 0.002)["avg"], I, 0.01, "A")
    check("E18b", "DC-moottori: ω = (D·U − Ra·I) / kΦ", sim.call("rpm", "M1") * 2 * math.pi / 60, (D * U - p["Ra"] * I) / p["k"], 0.01, "rad/s")


def test_E22_oskilloskoopin_mittaukset(sim, check):
    """Oskilloskoopin mittaustaulukko (keskiarvo, tehollisarvo, taajuus) vastaa signaalin arvoja."""
    sim.call("loadExample", "ex2"); sim.call("run", 0.2)
    ms = sim.call("drawScope")
    U = par(sim, "U1")["U"]
    check("E22a", "Oskilloskooppi: sinijännitteen tehollisarvo U", ms[0]["rms"], U, 0.01, "V")
    check("E22b", "Oskilloskooppi: huipusta huippuun 2√2·U", ms[0]["pp"], 2 * SQ2 * U, 0.01, "V")
    check("E22c", "Oskilloskooppi: taajuus f", ms[0]["f"], par(sim, "U1")["f"], 0.01, "Hz")

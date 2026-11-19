"""Yksinkertaisen ja kehittyneen mallin testit M01–M05."""
import math
from conftest import circuit


def test_M01_yksinkertainen_diodi_on_ihanteellinen(sim, check):
    sim.call("loadCircuit", circuit([("c1", "vdc", {"U": 10}, "U1"), ("c2", "d", {}, "D1"), ("c3", "r", {"R": 100}, "R1"), ("c4", "gnd", {}, "G")],
                                    [("c1:p", "c2:A"), ("c2:K", "c3:1"), ("c3:2", "c1:n"), ("c1:n", "c4:0")]))
    sim.call("run", 0.01)
    check("M01", "Yksinkertainen malli: ihanteellinen diodi, I = U / R", sim.call("i", "R1"), 0.1, 0.001, "A")


def test_M02_kehittynyt_lahteen_resistanssi(sim, check):
    sim.call("setMode", "advanced")
    sim.call("loadCircuit", circuit([("c1", "vdc", {"U": 12, "Rs": 0.5}, "U1"), ("c2", "r", {"R": 5.5}, "R1"), ("c3", "gnd", {}, "G")],
                                    [("c1:p", "c2:1"), ("c2:2", "c1:n"), ("c1:n", "c3:0")]))
    sim.call("run", 0.01)
    check("M02", "Kehittynyt malli: lähteen sisäinen resistanssi, I = U / (R + Rs)", sim.call("i", "R1"), 12 / 6, 0.001, "A")


def test_M03_mallin_vaihto_sailyttaa_parametrit(sim):
    sim.call("setMode", "advanced"); sim.call("loadExample", "ex3")
    sim.call("setParam", "D1", "Vf", 0.95)
    sim.call("setMode", "simple")
    assert sim.call("param", "D1")["Vf"] == 0, "M03: kynnysjännite ei poistunut yksinkertaisessa mallissa"
    assert sim.call("userParam", "D1")["Vf"] == 0.95, "M03: käyttäjän arvo hävisi mallia vaihdettaessa"
    assert '"Vf":0.95' in sim.call("serialize"), "M03: tallennukseen ei mennyt käyttäjän arvo"
    sim.call("setMode", "advanced")
    assert sim.call("param", "D1")["Vf"] == 0.95, "M03: kehittyneen mallin parametri ei palautunut"


def test_M04_kehittynyt_kynnysjannitteet_laskevat_tasajannitetta(sim, check):
    """Kehittynyt malli: diodisillassa kaksi diodia johtaa kerrallaan; R-kuormalla Ud laskee noin 2·UF0."""
    def ud(mode):
        sim.call("setMode", mode)
        comps = [("c1", "vac", {"U": 230, "f": 50, "Rs": 0, "Ls": 0}, "U1")] + [(f"c{i+2}", "d", {"Vf": 1.0, "Ron": 0.001}, f"D{i+1}") for i in range(4)] + \
                [("c6", "r", {"R": 100}, "R1"), ("c9", "gnd", {}, "G")]
        wires = [("c1:L", "c2:A"), ("c2:A", "c3:K"), ("c1:N", "c4:A"), ("c4:A", "c5:K"), ("c2:K", "c4:K"), ("c3:A", "c5:A"), ("c3:A", "c9:0"), ("c2:K", "c6:1"), ("c6:2", "c3:A")]
        sim.call("loadCircuit", circuit(comps, wires)); sim.call("run", 0.04)
        return sim.call("measure", "R1", "U", None, 0.1)["avg"]
    d = ud("simple") - ud("advanced")
    check("M04", "Kynnysjännitteen vaikutus diodisillassa ΔUd ≈ 2·UF0 (likiarvo)", d, 2.0, 0.1, "V")


def test_M05_kuollut_aika_viivastaa_paallekytkentaa(sim):
    sim.call("setMode", "advanced"); sim.call("loadExample", "ex7")
    sim.call("setParam", "Q1", "td", 5)
    sim.call("run", 0.0005)
    period = 1 / (sim.call("param", "Q1")["f"] * 1000)
    on = 0
    n = 400
    for k in range(n):
        sim.call("run", period / n)
        on += 1 if sim.call("isOn", "Q1", 0) else 0
    duty = on / n
    expected = sim.call("param", "Q1")["D"] / 100 - 5e-6 / period
    assert abs(duty - expected) < 0.02, f"M05: pulssisuhde {duty:.3f}, odotettu {expected:.3f} (kuollut aika lyhentää johtoaikaa)"

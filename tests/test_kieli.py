"""Kieliversioiden testit K01–K04."""
import re
from conftest import INDEX, circuit

TYPES = ["vdc", "vac", "v3", "gnd", "r", "c", "l", "tr", "sw", "d", "scr", "mos", "igbt", "dcm", "vm", "am"]


def test_K01_englanninkieliset_tekstit_kattavat(sim):
    sim.call("setLang", "en")
    for mode in ("simple", "advanced"):
        sim.call("setMode", mode)
        sim.call("loadCircuit", {"comps": [{"id": f"c{i+1}", "type": t, "x": 100 + i * 120, "y": 200, "rot": 0, "label": f"X{i}", "p": {}} for i, t in enumerate(TYPES)],
                                 "wires": [], "probes": [{"kind": "U", "target": "c5"}, {"kind": "I", "target": "c5"}]})
        sim.call("run", 0.02)
        for i in range(1, len(TYPES) + 1):
            sim.js(f"""(() => {{const g=document.querySelector('.comp[data-id="c{i}"] .hit');const r=g.getBoundingClientRect();
                const o={{bubbles:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,pointerId:1,button:0}};
                g.dispatchEvent(new PointerEvent('pointerdown',o));document.querySelector('#cv').dispatchEvent(new PointerEvent('pointerup',o));}})()""")
            text = sim.js("document.querySelector('#insp').innerText")
            left = [l for l in text.split("\n") if re.search("[äöÄÖ]", l)]
            assert not left, f"K01: suomea ominaisuuspaneelissa ({TYPES[i-1]}, {mode}): {left[:4]}"
    sim.js("document.querySelector('#helpBtn').click()")
    body = sim.js("document.body.innerText")
    left = [l for l in body.split("\n") if re.search("[äöÄÖ]", l) and "Seinäjoki" not in l]
    assert not left, f"K01: suomenkielistä tekstiä englanninkielisessä näkymässä: {left[:5]}"
    assert not sim.call("i18nMissing")


def test_K02_kielen_vaihto_ei_vaikuta_laskentaan(sim):
    def ajo(l):
        sim.call("setLang", l); sim.call("loadExample", "ex7"); sim.call("run", 0.004)
        return sim.call("v", "R1")
    assert ajo("fi") == ajo("en"), "K02: kieli vaikutti laskentaan"


def test_K03_url_parametrit(browser):
    page = browser.new_page()
    page.goto(INDEX.as_uri() + "?lang=en&malli=kehittynyt")
    page.wait_for_function("window.ElSim !== undefined")
    assert page.evaluate("ElSim.lang()") == "en" and page.evaluate("ElSim.mode()") == "advanced"
    assert page.inner_text("[data-mode=simple]") == "Simple"
    page.goto(INDEX.as_uri() + "?lang=fi&mode=simple")
    page.wait_for_function("window.ElSim !== undefined")
    assert page.evaluate("ElSim.lang()") == "fi" and page.evaluate("ElSim.mode()") == "simple"
    assert page.inner_text("[data-mode=advanced]") == "Kehittynyt"
    page.evaluate("localStorage.clear()")
    page.close()


def test_K04_oskilloskoopin_ohjaimet_englanniksi(sim):
    sim.call("setLang", "en"); sim.call("loadExample", "ex11"); sim.call("run", 0.02)
    text = sim.js("document.querySelector('#sctl').innerText + '\\n' + document.querySelector('#meas').innerText")
    left = [l for l in text.split("\n") if re.search("[äöÄÖ]", l)]
    assert not left, f"K04: suomea oskilloskoopin ohjaimissa: {left[:4]}"
    assert "Timebase" in text and "RMS" in text

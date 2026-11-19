"""Käyttöliittymän testit U01–U05."""
import json
from conftest import circuit


def _center(sim, cid):
    return sim.js(f"(()=>{{const r=document.querySelector('.comp[data-id=\"{cid}\"] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2];}})()")


def _ptr(sim, kind, x, y, shift=False, target="cv"):
    el = f"document.elementFromPoint({x},{y})" if target == "pt" else "document.querySelector('#cv')"
    sim.js(f"(() => {{{el}.dispatchEvent(new PointerEvent('{kind}',{{bubbles:true,pointerId:1,button:0,pointerType:'mouse',shiftKey:{str(shift).lower()},clientX:{x},clientY:{y}}}));}})()")


def test_U01_jannite_anturi_lisaa_kanavan(sim):
    sim.call("loadExample", "ex2"); sim.call("pause")
    sim.js("document.querySelector('[data-tool=I]').click()")
    x, y = _center(sim, "c3")
    _ptr(sim, "pointerdown", x, y, target="pt"); _ptr(sim, "pointerup", x, y)
    chans = sim.call("scope")["channels"]
    assert len(chans) == 4 and any(c["label"] == "I(L1)" for c in chans), f"U01: kanavaa ei lisätty: {chans}"
    sim.js("document.querySelector('[data-tool=U]').click()")
    _ptr(sim, "pointerdown", x, y, target="pt"); _ptr(sim, "pointerup", x, y)
    assert len(sim.call("scope")["channels"]) == 4, "U01: viides kanava lisättiin, vaikka kanavia on neljä"
    assert "Oskilloskoopissa on neljä kanavaa" in sim.js("document.querySelector('#warns').innerText")


def test_U02_kytkimen_klikkaus(sim, check):
    sim.call("loadExample", "ex1"); sim.call("pause"); sim.call("run", 0.3)
    u0 = sim.call("v", "C1")
    x, y = _center(sim, "c2")
    _ptr(sim, "pointerdown", x, y, target="pt"); _ptr(sim, "pointerup", x, y)
    assert sim.call("state", "S1")["on"] is False, "U02: kytkin ei auennut klikkauksesta"
    tau = sim.call("param", "R2")["R"] * sim.call("param", "C1")["C"] * 1e-6
    sim.call("run", tau)
    check("U02", "Avattu kytkin: purkautuminen u(τ) = u0·e⁻¹, τ = R2·C", sim.call("v", "C1"), u0 * 0.36788, 0.01, "V")


def test_U03_tallennus_ja_lataus(sim):
    sim.call("loadExample", "ex10")
    s = sim.call("serialize")
    sim.call("loadCircuit", json.loads(s))
    assert sim.call("serialize") == s, "U03: tallennus ja lataus eivät tuota samaa piiriä"
    d = json.loads(s)
    assert d["scope"]["tb"] == 5e-3 and len(d["probes"]) == 2


def test_U04_laatikkovalinta_kopioi_liita(sim):
    sim.call("loadExample", "ex2"); sim.call("pause")
    n_c = len(json.loads(sim.call("serialize"))["comps"])
    box = sim.js("""(()=>{const rs=['c2','c3'].map(id=>document.querySelector(`.comp[data-id="${id}"] .hit`).getBoundingClientRect());
      return [Math.min(...rs.map(r=>r.left))-12,Math.min(...rs.map(r=>r.top))-12,Math.max(...rs.map(r=>r.right))+12,Math.max(...rs.map(r=>r.bottom))+12];})()""")
    _ptr(sim, "pointerdown", box[0], box[1], shift=True, target="pt")
    _ptr(sim, "pointermove", box[2], box[3], shift=True); _ptr(sim, "pointerup", box[2], box[3], shift=True)
    assert set(sim.call("selection")) == {"R1", "L1"}, f"U04: laatikkovalinta {sim.call('selection')}"
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'c',ctrlKey:true,bubbles:true}))")
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'v',ctrlKey:true,bubbles:true}))")
    d = json.loads(sim.call("serialize"))
    assert len(d["comps"]) == n_c + 2, "U04: liittäminen ei lisännyt kahta komponenttia"
    sim.js("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Delete',bubbles:true}))")
    assert len(json.loads(sim.call("serialize"))["comps"]) == n_c


def test_U05_johtimen_reitin_veto(sim):
    sim.call("loadExample", "ex2"); sim.call("pause")
    pt = sim.js("""(()=>{const g=[...document.querySelectorAll('#lWires .wire')].find(g=>{const w=ElSim._wire(g.dataset.w);return w.a==='c1:L'&&w.b==='c2:1';});
      const p=g.querySelector('.wb');const pts=p.getAttribute('d').slice(1).split('L').map(s=>s.split(',').map(Number));
      let bi=0,bl=-1;for(let i=0;i<pts.length-1;i++){const l=Math.abs(pts[i+1][0]-pts[i][0])+Math.abs(pts[i+1][1]-pts[i][1]);if(l>bl){bl=l;bi=i;}}
      const m=p.getScreenCTM();const q=new DOMPoint((pts[bi][0]+pts[bi+1][0])/2,(pts[bi][1]+pts[bi+1][1])/2).matrixTransform(m);
      return [q.x,q.y,Math.abs(pts[bi][1]-pts[bi+1][1])<0.5];})()""")
    x, y, horiz = pt
    _ptr(sim, "pointerdown", x, y, target="pt")
    for s in range(1, 6):
        _ptr(sim, "pointermove", x + (0 if horiz else -8 * s), y + (-8 * s if horiz else 0))
    _ptr(sim, "pointerup", x, y)
    w = [w for w in json.loads(sim.call("serialize"))["wires"] if w["a"] == "c1:L"][0]
    assert w.get("pts"), "U05: reitin muutos ei tallentunut"
    assert len(json.loads(sim.call("serialize"))["wires"]) == 5

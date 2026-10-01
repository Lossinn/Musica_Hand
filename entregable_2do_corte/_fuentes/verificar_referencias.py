"""Verificación en línea de TODAS las referencias del documento y del póster.

- DOI: metadatos en la API de Crossref (o DataCite para arXiv) y resolución en doi.org.
- URL de fuentes sin DOI (DANE, Ley 1581): respuesta HTTP.
Escribe referencias_verificadas.json. No modifica doi_verificados.json.
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
F = Path(__file__).resolve().parent
sys.path.insert(0, str(F))
from datos import DOIS, REF_IDS, REF_EXTRA  # noqa: E402

UA = {"User-Agent": "HandSingKids-verif/1.1 (mailto:elquemascamella69@gmail.com)"}


def get(url, method="GET"):
    req = urllib.request.Request(url, headers=UA, method=method)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, r.geturl(), r.read() if method == "GET" else b""
    except urllib.error.HTTPError as e:
        return e.code, url, b""
    except Exception as e:  # noqa: BLE001
        return None, url, str(e).encode()


out = []
for rid in REF_IDS:
    doi = DOIS[rid]["doi"]
    st, _, body = get("https://api.crossref.org/works/" + doi)
    meta = json.loads(body)["message"] if st == 200 else {}
    st2, final, _ = get("https://doi.org/" + doi, "HEAD")
    tit = (meta.get("title") or [""])[0]
    ok_tit = tit.lower()[:40] == DOIS[rid]["titulo"].lower()[:40]
    out.append(dict(id=rid, doi=doi, crossref=st, doi_org=st2, destino=final, titulo_coincide=ok_tit,
                    anio=(meta.get("issued", {}).get("date-parts") or [[None]])[0][0],
                    volumen=meta.get("volume"), numero=meta.get("issue"), paginas=meta.get("page"),
                    articulo=meta.get("article-number"), autores=len(meta.get("author", []))))
    print(rid, doi, "crossref", st, "doi.org", st2, "título", "OK" if ok_tit else "DIFIERE")

# arXiv (DataCite)
st, _, body = get("https://api.datacite.org/dois/10.48550/arXiv.2006.10214")
att = json.loads(body)["data"]["attributes"] if st == 200 else {}
st2, final, _ = get("https://doi.org/10.48550/arXiv.2006.10214", "HEAD")
out.append(dict(id="zhang", doi="10.48550/arXiv.2006.10214", datacite=st, doi_org=st2,
                titulo=(att.get("titles") or [{}])[0].get("title"), anio=att.get("publicationYear"),
                autores=[c.get("name") for c in att.get("creators", [])]))
print("zhang", "datacite", st, "doi.org", st2, (att.get("titles") or [{}])[0].get("title"))

for clave, url, _ in REF_EXTRA:
    if 'href="' in url:
        u = url.split('href="')[1].split('"')[0]
        st, final, _ = get(u, "GET")
        out.append(dict(id=clave, url=u, http=st, destino=final))
        print(clave, u, st)

(F / "referencias_verificadas.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

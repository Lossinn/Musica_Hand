s = open("nucleo_hsk.py", encoding="utf-8").read()
a = s.index("    for i, (n, mail, _) in enumerate(autores, 1):\n        par(f\"^{{{i}}} Autor {i}")
b = s.index("    par(f\"^{{*}} Autor de correspondencia")
nuevo = '''    v = list(EQUIPO).index(primero)
    plantillas = [
        "Autor {i}: {n} - Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. ORCID: pendiente. Correo electrónico: {m}",
        "{n}. Universidad Pontificia Bolivariana, Seccional Montería (Córdoba, Colombia). Correo: {m}. ORCID: pendiente.",
        "Autor {i} — {n} — {m} — UPB Seccional Montería, Córdoba, Colombia — ORCID: pendiente",
        "{n} (autor {i}), Universidad Pontificia Bolivariana, Seccional Montería, Colombia; correo electrónico {m}; ORCID pendiente.",
        "Afiliación del autor {i}: Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. {n}, {m}. ORCID: pendiente.",
        "{i}. {n}, Universidad Pontificia Bolivariana (Seccional Montería, Colombia). Contacto: {m}. ORCID: pendiente.",
        "Autor {i}: {n}. Filiación: Universidad Pontificia Bolivariana, Seccional Montería, Córdoba, Colombia. {m}. ORCID: pendiente.",
    ]
    docentes = [
        "Co-Autor / Co-Investigador: {d}. Filiación: Docente Titular, Facultad de Ingeniería Industrial. Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE), Hub Industrial Solution (HIS), Universidad Pontificia Bolivariana, Seccional Montería, Colombia. ORCID: pendiente. Correo electrónico: {c}",
        "Co-Autor / Co-Investigador: {d}, Docente Titular de la Facultad de Ingeniería Industrial; SILOGE (Grupo de Investigación en Simulación, Logística y Gestión de Operaciones) y HIS (Hub Industrial Solution), UPB Seccional Montería, Colombia. {c}. ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d} ({c}; ORCID pendiente). Filiación: Hub Industrial Solution (HIS) y grupo SILOGE, Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería, Colombia; Docente Titular.",
        "Co-Autor / Co-Investigador: {d}. Docente Titular, Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería, Colombia, y miembro del Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE) y del Hub Industrial Solution (HIS). Correo: {c}. ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d} — Filiación: Facultad de Ingeniería Industrial (Docente Titular), Grupo SILOGE de Simulación, Logística y Gestión de Operaciones, Hub Industrial Solution (HIS); UPB Seccional Montería, Colombia — {c} — ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d}, UPB Seccional Montería, Colombia. Docente Titular de la Facultad de Ingeniería Industrial; Grupo de Investigación en Simulación, Logística y Gestión de Operaciones (SILOGE); Hub Industrial Solution (HIS). Correo electrónico: {c}. ORCID: pendiente.",
        "Co-Autor / Co-Investigador: {d}. Filiación: Hub Industrial Solution (HIS); Grupo de Investigación SILOGE (Simulación, Logística y Gestión de Operaciones); Docente Titular, Facultad de Ingeniería Industrial, Universidad Pontificia Bolivariana, Seccional Montería, Colombia. Contacto: {c}. ORCID: pendiente.",
    ]
    for i, (n, mail, _) in enumerate(autores, 1):
        par("^{" + str(i) + "} " + plantillas[v].format(i=i, n=n, m=mail), "Normal", size=8)
    par("^{" + str(len(autores) + 1) + "} " + docentes[v].format(d=DOCENTE[0], c=DOCENTE[1]), "Normal", size=8)
'''
s = s[:a] + nuevo + s[b:]
open("nucleo_hsk.py", "w", encoding="utf-8").write(s)
# art_*: usar DECL
import re
for p in ("vitola", "petro", "negrete", "carrascal", "quintana", "pemberty", "guerra"):
    f = f"art_{p}.py"
    t = open(f, encoding="utf-8").read()
    i = t.index("declaraciones(dict(")
    j = t.index("cierre(autores")
    t = t[:i] + f"from decl_personas import DECL\ndeclaraciones(DECL[\"{p}\"])\n" + t[j:]
    open(f, "w", encoding="utf-8").write(t)
print("ok")

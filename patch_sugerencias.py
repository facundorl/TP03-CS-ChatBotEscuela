# -*- coding: utf-8 -*-
"""Agrega 'titulo' y 'sugerencias' a cada intent de intents.json.
No toca 'patterns' ni 'tag', por lo que NO hace falta reentrenar el modelo.
"""
import json

TITULOS = {
    "saludo": "Saludo",
    "despedida": "Despedida",
    "agradecimiento": "Agradecimiento",
    "constancia_alumno_regular": "Constancia de alumno regular",
    "certificado_analitico": "Certificado analitico",
    "practicas_profesionalizantes": "Practicas profesionalizantes",
    "seguridad_talleres": "Seguridad en talleres",
    "seguridad_laboratorio_computacion": "Normas del laboratorio",
    "mesas_examen": "Mesas de examen",
    "equivalencias": "Equivalencias y pases",
    "especialidades": "Especialidades",
    "contacto_ubicacion": "Contacto y ubicacion",
    "inscripciones": "Inscripciones",
    "turnos": "Turnos",
    "horarios": "Horarios",
    "horarios-taller": "Horarios de talleres",
    "cooperadora": "Cooperadora",
    "faltas": "Faltas y asistencia",
}

SUGERENCIAS = {
    "saludo": ["especialidades", "inscripciones", "horarios"],
    "despedida": [],
    "agradecimiento": [],
    "constancia_alumno_regular": ["certificado_analitico", "faltas", "contacto_ubicacion"],
    "certificado_analitico": ["constancia_alumno_regular", "equivalencias", "contacto_ubicacion"],
    "practicas_profesionalizantes": ["seguridad_talleres", "especialidades", "horarios-taller"],
    "seguridad_talleres": ["horarios-taller", "practicas_profesionalizantes", "seguridad_laboratorio_computacion"],
    "seguridad_laboratorio_computacion": ["seguridad_talleres", "especialidades", "horarios-taller"],
    "mesas_examen": ["faltas", "equivalencias", "horarios"],
    "equivalencias": ["mesas_examen", "certificado_analitico", "inscripciones"],
    "especialidades": ["turnos", "horarios-taller", "practicas_profesionalizantes"],
    "contacto_ubicacion": ["horarios", "inscripciones", "cooperadora"],
    "inscripciones": ["especialidades", "turnos", "contacto_ubicacion"],
    "turnos": ["horarios", "horarios-taller", "especialidades"],
    "horarios": ["turnos", "horarios-taller", "faltas"],
    "horarios-taller": ["seguridad_talleres", "turnos", "especialidades"],
    "cooperadora": ["contacto_ubicacion", "inscripciones"],
    "faltas": ["mesas_examen", "horarios", "constancia_alumno_regular"],
}

RUTA = "intents.json"

with open(RUTA, "r", encoding="utf-8") as f:
    data = json.load(f)

for intent in data["intents"]:
    tag = intent["tag"]
    intent["titulo"] = TITULOS.get(tag, tag.replace("_", " ").capitalize())
    intent["sugerencias"] = SUGERENCIAS.get(tag, [])

with open(RUTA, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("OK - intents.json actualizado con 'titulo' y 'sugerencias'")
for i in data["intents"]:
    print(" -", i["tag"], "->", i["sugerencias"])

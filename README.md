# PSR-TP03-C2: Chatbot Escolar con Inteligencia Artificial - Escuela Técnica N° 36 D.E. 15

Sistema asistente virtual orientado a la resolución de consultas sobre trámites administrativos, normativas académicas, prácticas profesionalizantes y seguridad en entornos de taller y laboratorio de la Escuela Técnica N° 36 "Almirante Guillermo Brown" (Saavedra, Ciudad Autónoma de Buenos Aires).

El proyecto implementa técnicas de Procesamiento de Lenguaje Natural (PLN) y un modelo secuencial de red neuronal densa (Deep Learning con TensorFlow/Keras), expuesto mediante una API REST en Flask y consumido por una interfaz de usuario desacoplada desarrollada en React y Vite.

---

## 1. Arquitectura del Sistema

```text
[Frontend: React + Vite (landingGUI)]
       |
       | (Peticiones HTTP POST con payload JSON a http://localhost:5000/chat)
       v
[Backend de Red: API REST con Flask y Flask-CORS (app.py)]
       |
       +--> [Normalización Unicode NFD y Vectorización Bag of Words]
       v
[Clasificador: Red Neuronal Keras (chatbot_model.h5)]
       |
       +--> Umbral de certeza >= 60%: Retorno de respuesta clasificada
       +--> Umbral de certeza < 60% o vocabulario nulo: Fallback institucional
```

---

## 2. Requerimientos del Entorno

- **Python:** Versión 3.11.x recomendada para compatibilidad con TensorFlow.
- **Node.js:** Versión 18.x o superior con gestor de paquetes `npm`.
- **Sistema Operativo:** Compatible con Windows, Linux o macOS.

---

## 3. Instalación y Despliegue

### 3.1. Clonación del Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd TP03-C2
```

### 3.2. Configuración del Entorno Virtual de Python
Se recomienda el uso de un entorno virtual aislado para evitar conflictos de dependencias:

```bash
# Creación del entorno virtual
python -m venv .venv

# Activación en Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Activación en Linux / macOS:
source .venv/bin/activate

# Instalación de dependencias del backend
pip install -r requirements.txt
```

### 3.3. Entrenamiento de la Red Neuronal
Para compilar la base de conocimiento y generar los artefactos del modelo (`chatbot_model.h5`, `words.pkl` y `classes.pkl`):

```bash
python train.py
```

### 3.4. Ejecución del Servidor Backend (API REST)
```bash
python app.py
```
El servicio quedará disponible en `http://localhost:5000`:
- **Comprobación de estado:** `GET http://localhost:5000/`
- **Endpoint del asistente:** `POST http://localhost:5000/chat`

### 3.5. Ejecución del Cliente Frontend
En una consola secundaria:

```bash
cd landingGUI
npm install
npm run dev
```
La aplicación web se ejecutará localmente en `http://localhost:5173`.

---

## 4. Pruebas de Integración y Verificación de Red

Se puede evaluar la respuesta del backend mediante solicitudes HTTP con herramientas como `curl`, Postman o Insomnia:

```bash
curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"Como solicito la constancia de alumno regular?\"}"
```

### Estructura de Respuesta (JSON):
```json
{
  "confidence": 1.0,
  "intent": "constancia_alumno_regular",
  "response": "Podés solicitar tu constancia de alumno regular en la Secretaría de la ET 36 (Galván 3700)..."
}
```

---

## 5. Especificaciones Funcionales Cubiertas

1. **Emisión de Documentación:** Solicitud de constancias de alumno regular, certificados analíticos, título técnico y trámites vinculados ante el GCBA.
2. **Prácticas Profesionalizantes:** Información reglamentaria conforme a la Ley 26.058 (mínimo de 200 horas reloj, asignación a contraturno, cobertura de ART y convenios).
3. **Seguridad e Higiene Técnica:** Protocolo de Elementos de Protección Personal (EPP) en talleres (mameluco de grafa, calzado con puntera de acero, antiparras), normativas operativas y reglamento de laboratorios de informática.
4. **Instancias de Evaluación:** Cronogramas de mesas de examen para asignaturas previas y libres, matriculación en Secretaría/Preceptoría y régimen FINESTEC.
5. **Identidad Institucional:** Especialidades técnicas oficiales (Computación y Maestro Mayor de Obras), ubicación física en el Polo Educativo Saavedra y canales de comunicación.
6. **Manejo de Errores y Respuesta por Defecto (Fallback):** Control de umbral de confianza mínimo (60%) y filtrado de términos no discriminativos para canalizar dudas complejas hacia las vías de atención formal.

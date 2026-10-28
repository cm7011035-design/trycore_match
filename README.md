
# API de Matching de Candidatos

API REST desarrollada con Python y Django para calcular la compatibilidad entre un candidato y una vacante laboral.

## Tecnologías

- Python
- Django
- API HTTP con JSON
- Pruebas automatizadas con Django TestCase

## Instalación

Clona el repositorio y entra en la carpeta del proyecto.

Activa el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Inicia el servidor:

```bash
python manage.py runserver
```

La API estará disponible en:

`http://127.0.0.1:8000/match`

## Endpoint

### POST /match

Recibe un objeto JSON con los datos del candidato y de la vacante.

Ejemplo:

```json
{
  "candidato": {
    "skills": ["Python", "Django", "SQL"],
    "experiencia_anios": 3
  },
  "vacante": {
    "skills_requeridas": ["Python", "Django", "SQL", "Docker"],
    "experiencia_min": 5,
    "tipo_contrato": "indefinido"
  }
}
```

## Fórmula de puntuación

- Cobertura de habilidades: porcentaje de habilidades requeridas que cumple el candidato, multiplicado por 70.
- Experiencia: `max(0, 1 - brecha_experiencia / 5) * 20`.
- Bonificación por contrato:
  - Indefinido: 10 puntos.
  - Obra o labor: 5 puntos.
  - Prestación de servicios: 0 puntos.

La puntuación final se redondea al entero más cercano.

Si la lista de habilidades requeridas está vacía, la cobertura se considera 1.0 para evitar una división por cero.

## Categorías

| Puntuación | Categoría |
|---|---|
| Menor que 40 | NO_FIT |
| 40 a 64 | MAYBE |
| 65 a 84 | GOOD_FIT |
| 85 o más | EXCELLENT_FIT |

## Ejecutar pruebas

```bash
python manage.py test matching
```

El conjunto actual contiene siete pruebas automatizadas para validar categorías, experiencia, habilidades y campos requeridos.


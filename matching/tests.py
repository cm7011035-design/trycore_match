
import json
from django.test import TestCase, Client


class MatchingAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "/match"
        self.datos = {
            "candidato": {
                "skills": ["Python", "Django", "SQL"],
                "experiencia_anios": 5,
            },
            "vacante": {
                "skills_requeridas": ["Python", "Django", "SQL"],
                "experiencia_min": 3,
                "tipo_contrato": "indefinido",
            },
        }

    def enviar(self, datos=None):
        return self.client.post(
            self.url,
            data=json.dumps(datos if datos is not None else self.datos),
            content_type="application/json",
        )

    def test_candidato_excelente(self):
        respuesta = self.enviar()
        self.assertEqual(respuesta.status_code, 200)
        resultado = respuesta.json()
        self.assertEqual(resultado["score"], 100)
        self.assertEqual(resultado["categoria"], "EXCELLENT_FIT")

    def test_candidato_sin_compatibilidad(self):
        datos = {
            "candidato": {
                "skills": [],
                "experiencia_anios": 0,
            },
            "vacante": {
                "skills_requeridas": ["Python", "Django"],
                "experiencia_min": 5,
                "tipo_contrato": "prestacion_servicios",
            },
        }
        respuesta = self.enviar(datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["categoria"], "NO_FIT")

    def test_lista_de_skills_requeridas_vacia(self):
        datos = {
            "candidato": {
                "skills": ["Python"],
                "experiencia_anios": 2,
            },
            "vacante": {
                "skills_requeridas": [],
                "experiencia_min": 2,
                "tipo_contrato": "indefinido",
            },
        }
        respuesta = self.enviar(datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["cobertura_skills"], 1.0)

    def test_experiencia_superior_al_minimo(self):
        datos = {
            "candidato": {
                "skills": ["Python"],
                "experiencia_anios": 8,
            },
            "vacante": {
                "skills_requeridas": ["Python"],
                "experiencia_min": 3,
                "tipo_contrato": "indefinido",
            },
        }
        respuesta = self.enviar(datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["brecha_experiencia"], 0)

    def test_candidato_maybe(self):
        datos = {
            "candidato": {
                "skills": ["Python", "Django"],
                "experiencia_anios": 0,
            },
            "vacante": {
                "skills_requeridas": ["Python", "Django", "SQL"],
                "experiencia_min": 1,
                "tipo_contrato": "prestacion_servicios",
            },
        }
        respuesta = self.enviar(datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["categoria"], "MAYBE")

    def test_candidato_good_fit(self):
        datos = {
            "candidato": {
                "skills": ["Python", "Django"],
                "experiencia_anios": 2,
            },
            "vacante": {
                "skills_requeridas": ["Python", "Django", "SQL"],
                "experiencia_min": 2,
                "tipo_contrato": "obra_labor",
            },
        }
        respuesta = self.enviar(datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["categoria"], "GOOD_FIT")

    def test_campo_requerido_ausente(self):
        datos = {"candidato": self.datos["candidato"]}
        respuesta = self.enviar(datos)
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("error", respuesta.json())

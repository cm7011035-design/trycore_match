
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import calcular_matching


@csrf_exempt
@require_POST
def match(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "JSON inválido"},
            status=400
        )

    if not isinstance(datos, dict):
        return JsonResponse(
            {"error": "Se esperaba un objeto JSON"},
            status=400
        )

    if "candidato" not in datos:
        return JsonResponse(
            {"error": "campo candidato requerido"},
            status=400
        )

    if "vacante" not in datos:
        return JsonResponse(
            {"error": "campo vacante requerido"},
            status=400
        )

    candidato = datos["candidato"]
    vacante = datos["vacante"]

    if not isinstance(candidato, dict):
        return JsonResponse(
            {"error": "candidato debe ser un objeto"},
            status=400
        )

    if not isinstance(vacante, dict):
        return JsonResponse(
            {"error": "vacante debe ser un objeto"},
            status=400
        )

    campos_candidato = {
        "skills": list,
        "experiencia_anios": int,
    }

    campos_vacante = {
        "skills_requeridas": list,
        "experiencia_min": int,
        "tipo_contrato": str,
    }

    for campo, tipo in campos_candidato.items():
        if campo not in candidato:
            return JsonResponse(
                {"error": f"campo {campo} requerido"},
                status=400
            )

        valor = candidato[campo]
        if not isinstance(valor, tipo) or (
            tipo is int and isinstance(valor, bool)
        ):
            return JsonResponse(
                {"error": f"campo {campo} inválido"},
                status=400
            )

    for campo, tipo in campos_vacante.items():
        if campo not in vacante:
            return JsonResponse(
                {"error": f"campo {campo} requerido"},
                status=400
            )

        valor = vacante[campo]
        if not isinstance(valor, tipo):
            return JsonResponse(
                {"error": f"campo {campo} inválido"},
                status=400
            )

    if not all(
        isinstance(skill, str)
        for skill in candidato["skills"]
    ):
        return JsonResponse(
            {"error": "skills debe contener textos"},
            status=400
        )

    if not all(
        isinstance(skill, str)
        for skill in vacante["skills_requeridas"]
    ):
        return JsonResponse(
            {"error": "skills_requeridas debe contener textos"},
            status=400
        )

    if candidato["experiencia_anios"] < 0:
        return JsonResponse(
            {"error": "experiencia_anios no puede ser negativa"},
            status=400
        )

    if vacante["experiencia_min"] < 0:
        return JsonResponse(
            {"error": "experiencia_min no puede ser negativa"},
            status=400
        )

    contratos_validos = {
        "indefinido",
        "obra_labor",
        "prestacion_servicios",
    }

    if vacante["tipo_contrato"] not in contratos_validos:
        return JsonResponse(
            {"error": "tipo_contrato inválido"},
            status=400
        )

    resultado = calcular_matching(candidato, vacante)
    return JsonResponse(resultado, status=200)

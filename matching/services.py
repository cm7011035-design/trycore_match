
def calcular_matching(candidato, vacante):
    """
    Calcula la compatibilidad entre un candidato y una vacante.
    """

    skills_candidato = set(candidato["skills"])
    skills_requeridas = set(vacante["skills_requeridas"])

    # Si no se requieren habilidades, no existe brecha de skills.
    if not skills_requeridas:
        cobertura_skills = 1.0
    else:
        cobertura_skills = (
            len(skills_candidato & skills_requeridas)
            / len(skills_requeridas)
        )

    experiencia = candidato["experiencia_anios"]
    experiencia_minima = vacante["experiencia_min"]

    brecha_experiencia = max(0, experiencia_minima - experiencia)

    puntos_skills = cobertura_skills * 70
    puntos_experiencia = max(
        0, 1 - brecha_experiencia / 5
    ) * 20

    bonos_contrato = {
        "indefinido": 10,
        "obra_labor": 5,
        "prestacion_servicios": 0,
    }

    tipo_contrato = vacante["tipo_contrato"]
    bonus_contrato = bonos_contrato.get(tipo_contrato, 0)

    score = round(
        puntos_skills + puntos_experiencia + bonus_contrato
    )

    if score < 40:
        categoria = "NO_FIT"
    elif score < 65:
        categoria = "MAYBE"
    elif score < 85:
        categoria = "GOOD_FIT"
    else:
        categoria = "EXCELLENT_FIT"

    razones = []

    if cobertura_skills == 1:
        razones.append("Cumple todas las habilidades requeridas")
    else:
        razones.append(
            f"Cobertura de habilidades: "
            f"{cobertura_skills:.0%}"
        )

    if brecha_experiencia == 0:
        razones.append(
            "Cumple la experiencia mínima requerida"
        )
    else:
        razones.append(
            f"Le faltan {brecha_experiencia} años de experiencia"
        )

    razones.append(
        f"Bonificación por contrato: {bonus_contrato} puntos"
    )

    return {
        "score": score,
        "categoria": categoria,
        "cobertura_skills": round(cobertura_skills, 2),
        "brecha_experiencia": brecha_experiencia,
        "razones": razones[:3],
    }

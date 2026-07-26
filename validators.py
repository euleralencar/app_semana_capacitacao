import re


class ValidationError(ValueError):
    pass


def normalize_matricula(value):
    matricula = value.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.-]{3,30}", matricula):
        raise ValidationError("Informe uma matrícula STF válida.")
    return matricula


def normalize_ranking_search(value):
    matricula = value.strip().upper()
    if matricula and not re.fullmatch(r"[A-Z0-9.-]{1,30}", matricula):
        raise ValidationError("Informe uma matrícula STF válida para a busca.")
    return matricula


def normalize_cpf(value):
    cpf = re.sub(r"\D", "", value)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("Informe um CPF válido.")

    total = sum(int(digit) * weight for digit, weight in zip(cpf[:9], range(10, 1, -1)))
    first_digit = (total * 10 % 11) % 10
    total = sum(int(digit) * weight for digit, weight in zip(cpf[:10], range(11, 1, -1)))
    second_digit = (total * 10 % 11) % 10
    if cpf[-2:] != f"{first_digit}{second_digit}":
        raise ValidationError("Informe um CPF válido.")
    return cpf


def validate_registration(data):
    nome = data.get("nome", "").strip()
    secretaria = data.get("secretaria", "").strip()
    if len(nome) < 3 or len(nome) > 150:
        raise ValidationError("Informe o nome completo.")
    if len(secretaria) < 2 or len(secretaria) > 120:
        raise ValidationError("Informe a secretaria.")
    return {
        "nome": nome,
        "matricula": normalize_matricula(data.get("matricula", "")),
        "cpf": normalize_cpf(data.get("cpf", "")),
        "secretaria": secretaria,
    }


def validate_checkin(data):
    codigo_palestra = data.get("codigo_palestra", "").strip().upper()
    if not re.fullmatch(r"[A-Z0-9-]{3,30}", codigo_palestra):
        raise ValidationError("Informe um código de palestra válido.")
    return {
        "matricula": normalize_matricula(data.get("matricula", "")),
        "codigo_palestra": codigo_palestra,
    }

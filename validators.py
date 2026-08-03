import re


class ValidationError(ValueError):
    pass


SECRETARIA_OPTIONS = [
    "CENTRO DE ESTUDOS CONSTITUCIONAIS DO SUPREMO TRIBUNAL FEDERAL",
    "ASSESSORIA DE ANÁLISE DE RECURSOS (ARE)",
    "ASSESSORIA DE APOIO À GOVERNANÇA E CONFORMIDADE (AGC)",
    "ASSESSORIA DE APOIO À JURISDIÇÃO",
    "ASSESSORIA DE ARTICULAÇÃO PARLAMENTAR (ARP)",
    "ASSESSORIA DE ASSUNTOS INTERNACIONAIS (AIN)",
    "ASSESSORIA DE CERIMONIAL (ACE)",
    "ASSESSORIA DO PLENÁRIO (APL)",
    "ASSESSORIA JURÍDICA (AJU)",
    "ASSESSORIA PROCESSUAL (ASP)",
    "AUDITORIA INTERNA (AUDI)",
    "GABINETE DA PRESIDÊNCIA (GPR)",
    "GABINETE DA VICE-PRESIDÊNCIA (GVPR)",
    "GABINETE MINISTRA CÁRMEN LÚCIA (GMCL)",
    "GABINETE MINISTRO ALEXANDRE DE MORAES (GMAM)",
    "GABINETE MINISTRO ANDRÉ MENDONÇA (GMALM)",
    "GABINETE MINISTRO CRISTIANO ZANIN",
    "GABINETE MINISTRO DIAS TOFFOLI (GMDT)",
    "GABINETE MINISTRO EDSON FACHIN (GMEF)",
    "GABINETE MINISTRO FLAVIO DINO (GMFD)",
    "GABINETE MINISTRO GILMAR MENDES (GMGM)",
    "GABINETE MINISTRO LUIZ FUX (GMLF)",
    "GABINETE MINISTRO NUNES MARQUES (GMNM)",
    "GABINETE MINISTRO VAGO",
    "GABINETE DA DIRETORA-GERAL (GDG)",
    "GABINETE DO SECRETÁRIO-GERAL DA PRESIDÊNCIA (GSG)",
    "OUVIDORIA",
    "PRIMEIRA TURMA",
    "SEGUNDA TURMA",
    "SECRETARIA-GERAL DE TECNOLOGIA E INOVAÇÃO (SGTI)",
    "SECRETARIA DE ADMINISTRAÇÃO DE SERVIÇOS E GESTÃO PREDIAL (SAP)",
    "SECRETARIA DE ALTOS ESTUDOS (SAE)",
    "SECRETARIA DE COMUNICAÇÃO SOCIAL (SCO)",
    "SECRETARIA DE DADOS E ESTRATÉGIA (SDE)",
    "SECRETARIA DE EQUIDADE, DIVERSIDADE E INCLUSÃO (SED)",
    "SECRETARIA DE GESTÃO DE PESSOAS (SGP)",
    "SECRETARIA DE GESTÃO DE PRECEDENTES (SPR)",
    "SECRETARIA DE OPERAÇÕES E INFRAESTRUTURA (SOI)",
    "SECRETARIA DE ORÇAMENTO, FINANÇAS E CONTRATAÇÕES (SOC)",
    "SECRETARIA DE POLÍCIA JUDICIAL (SPJ)",
    "SECRETARIA DE RELAÇÕES COM A SOCIEDADE (SRS)",
    "SECRETARIA DE SERVIÇOS INTEGRADOS DE SAÚDE (SIS)",
    "SECRETARIA DE SOLUÇÕES JUDICIAIS (SSJ)",
    "SECRETARIA DE TV E RÁDIO JUSTIÇA (STV)",
]


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
    if secretaria not in SECRETARIA_OPTIONS:
        raise ValidationError("Selecione uma secretaria válida.")
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
        "cpf": normalize_cpf(data.get("cpf", "")),
        "codigo_palestra": codigo_palestra,
    }

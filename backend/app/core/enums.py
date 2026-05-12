from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    gestor = "gestor"
    colaborador = "colaborador"


class SystemCriticality(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    critica = "critica"


class AccessStatus(str, Enum):
    ativo = "ativo"
    pendente = "pendente"
    revogado = "revogado"


class AccessLevel(str, Enum):
    admin = "admin"
    editor = "editor"
    leitura = "leitura"

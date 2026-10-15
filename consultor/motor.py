from dataclasses import dataclass, field

from . import compat  # noqa: F401  (deve vir antes do experta)
from experta import Fact, KnowledgeEngine, P, Rule

from .perguntas import limpar_respostas, perguntas_visiveis
from .regras_meta import REGRAS
from .trilhas import TRILHAS


class Perfil(Fact):
    """Fato com as respostas do usuário (matematica, atuacao, ferramenta, ...)."""


def uma_de(*valores):
    return P(lambda v: v in valores)


@dataclass
class Resultado:
    trilha_id: str | None
    ranking: list = field(default_factory=list)            
    regras_vencedora: list = field(default_factory=list)   
    outras_regras: list = field(default_factory=list)     
    regras_disparadas: list = field(default_factory=list)  
    aderencia: int = 0                                      
    empate: bool = False
    mensagem: str = ""

    @property
    def trilha(self) -> dict | None:
        return TRILHAS.get(self.trilha_id) if self.trilha_id else None

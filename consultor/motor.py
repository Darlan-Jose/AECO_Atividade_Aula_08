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


class ConsultorCarreira(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.pontos = {tid: 0 for tid in TRILHAS}
        self.disparos: list[str] = []
        self.resultado: Resultado | None = None

    def _disparar(self, regra_id: str) -> None:
        self.disparos.append(regra_id)
        for trilha, pts in REGRAS[regra_id]["efeitos"].items():
            self.pontos[trilha] += pts

    #Back-end
    @Rule(Perfil(atuacao="logica", estilo="bastidores"))
    def r01(self):
        self._disparar("R01")

    @Rule(Perfil(atuacao="logica", ferramenta=uma_de("python", "sql")))
    def r02(self):
        self._disparar("R02")

    @Rule(Perfil(ferramenta="javascript", atuacao="logica", estilo="bastidores"))
    def r03(self):
        self._disparar("R03")

    #Front-end
    @Rule(Perfil(atuacao="visual"))
    def r04(self):
        self._disparar("R04")

    @Rule(Perfil(ferramenta="javascript", estilo="usuario"))
    def r05(self):
        self._disparar("R05")

    #Ciência de Dados
    @Rule(Perfil(matematica="alta", atuacao="dados", foco_dados="modelos"))
    def r06(self):
        self._disparar("R06")

    @Rule(Perfil(matematica="alta", ferramenta="python", entrega="insights"))
    def r07(self):
        self._disparar("R07")

    @Rule(Perfil(matematica="baixa", foco_dados="modelos"))
    def r08(self):
        self._disparar("R08")

    #Engenharia de Dados
    @Rule(Perfil(atuacao="dados", foco_dados="pipelines"))
    def r09(self):
        self._disparar("R09")

    @Rule(Perfil(ferramenta=uma_de("sql", "python"), foco_dados="pipelines"))
    def r10(self):
        self._disparar("R10")

    #Cibersegurança
    @Rule(Perfil(atuacao="seguranca"))
    def r11(self):
        self._disparar("R11")

    @Rule(Perfil(entrega="seguranca"))
    def r12(self):
        self._disparar("R12")

    @Rule(Perfil(ferramenta="linux_redes", entrega="seguranca"))
    def r13(self):
        self._disparar("R13")

    #DevOps
    @Rule(Perfil(atuacao="servidores", foco_infra="automacao"))
    def r14(self):
        self._disparar("R14")

    @Rule(Perfil(ferramenta="linux_redes", foco_infra="automacao"))
    def r15(self):
        self._disparar("R15")

    #Cloud
    @Rule(Perfil(atuacao="servidores", foco_infra="arquitetura"))
    def r16(self):
        self._disparar("R16")

    @Rule(Perfil(entrega="infra", foco_infra="arquitetura"))
    def r17(self):
        self._disparar("R17")

    #Mobile
    @Rule(Perfil(atuacao="mobile"))
    def r18(self):
        self._disparar("R18")

    @Rule(Perfil(ferramenta="mobile_lang"))
    def r19(self):
        self._disparar("R19")

    #QA
    @Rule(Perfil(atuacao="testes"))
    def r20(self):
        self._disparar("R20")

    @Rule(Perfil(entrega="qualidade"))
    def r21(self):
        self._disparar("R21")

    #Gestão de Produtos
    @Rule(Perfil(atuacao="gestao"))
    def r22(self):
        self._disparar("R22")

    @Rule(Perfil(entrega="estrategia"))
    def r23(self):
        self._disparar("R23")

    @Rule(Perfil(estilo="negocio"))
    def r24(self):
        self._disparar("R24")

    #Segurança de infra
    @Rule(Perfil(atuacao="servidores", entrega="seguranca"))
    def r25(self):
        self._disparar("R25")

    @Rule(Perfil(), salience=-100)
    def decidir(self):
        self.resultado = self._consolidar()

    def _consolidar(self) -> Resultado:
        n_regras_pos = {tid: 0 for tid in TRILHAS}
        for rid in self.disparos:
            for trilha, pts in REGRAS[rid]["efeitos"].items():
                if pts > 0:
                    n_regras_pos[trilha] += 1

        ordem = list(TRILHAS)
        ranking = sorted(
            self.pontos.items(),
            key=lambda kv: (-kv[1], -n_regras_pos[kv[0]], ordem.index(kv[0])),
        )
        melhor_id, melhor_pts = ranking[0]

        if melhor_pts <= 0:
            return Resultado(
                trilha_id=None,
                ranking=ranking,
                regras_disparadas=list(self.disparos),
                mensagem="As respostas não ativaram regras suficientes para uma recomendação.",
            )

        total_pos = sum(p for _, p in ranking if p > 0)
        empate = len(ranking) > 1 and ranking[1][1] == melhor_pts

        venc, outras = [], []
        for rid in self.disparos:
            regra = REGRAS[rid]
            item = {
                "id": rid,
                "condicao": regra["condicao"],
                "motivo": regra["motivo"],
                "efeitos": regra["efeitos"],
                "pontos": regra["efeitos"].get(melhor_id, 0),
            }
            (venc if melhor_id in regra["efeitos"] else outras).append(item)

        msg = ""
        if empate:
            msg = (
                f"Empate técnico com {TRILHAS[ranking[1][0]]['nome']}. "
                "Desempate pelo número de regras favoráveis."
            )
        return Resultado(
            trilha_id=melhor_id,
            ranking=ranking,
            regras_vencedora=venc,
            outras_regras=outras,
            regras_disparadas=list(self.disparos),
            aderencia=round(100 * melhor_pts / total_pos),
            empate=empate,
            mensagem=msg,
        )

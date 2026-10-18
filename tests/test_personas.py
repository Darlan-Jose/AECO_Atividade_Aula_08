"""Fase 4 - Validação com personas de teste.
python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from consultor.motor import consultar  
from consultor.regras_meta import REGRAS  
from consultor.trilhas import TRILHAS  

# (nome, respostas, trilha esperada)
PERSONAS = [
    (
        "Ana - perfil analítico",
        dict(matematica="alta", atuacao="dados", ferramenta="python", entrega="insights",
             estilo="bastidores", foco_dados="modelos"),
        "DS",
    ),
    (
        "Bruno - perfil infra/segurança",
        dict(matematica="media", atuacao="seguranca", ferramenta="linux_redes",
             entrega="seguranca", estilo="bastidores"),
        "SEC",
    ),
    (
        "Carla - perfil visual/frontend",
        dict(matematica="baixa", atuacao="visual", ferramenta="javascript",
             entrega="produto", estilo="usuario"),
        "FRONT",
    ),
    (
        "Diego - perfil negócios/produto",
        dict(matematica="media", atuacao="gestao", ferramenta="nenhuma",
             entrega="estrategia", estilo="negocio"),
        "PM",
    ),
    (
        "Elisa - engenharia de dados",
        dict(matematica="media", atuacao="dados", ferramenta="sql", entrega="infra",
             estilo="bastidores", foco_dados="pipelines", foco_infra="arquitetura"),
        "DE",
    ),
    (
        "Felipe - back-end",
        dict(matematica="media", atuacao="logica", ferramenta="python", entrega="produto",
             estilo="bastidores"),
        "BACK",
    ),
    (
        "Gabi - DevOps",
        dict(matematica="media", atuacao="servidores", ferramenta="linux_redes", entrega="infra",
             estilo="bastidores", foco_infra="automacao"),
        "DEVOPS",
    ),
    (
        "Heitor - arquitetura em nuvem",
        dict(matematica="media", atuacao="servidores", ferramenta="linux_redes", entrega="infra",
             estilo="bastidores", foco_infra="arquitetura"),
        "CLOUD",
    ),
    (
        "Isabela - mobile",
        dict(matematica="media", atuacao="mobile", ferramenta="mobile_lang", entrega="produto",
             estilo="usuario"),
        "MOBILE",
    ),
    (
        "João - QA",
        dict(matematica="media", atuacao="testes", ferramenta="python", entrega="qualidade",
             estilo="bastidores"),
        "QA",
    ),
]

DESAMBIGUACAO = [
    (
        "Alta matemática, mas quer construir pipelines -> Eng. de Dados, não Cientista",
        dict(matematica="alta", atuacao="dados", ferramenta="python", entrega="insights",
             estilo="bastidores", foco_dados="pipelines"),
        "DE",
    ),
    (
        "JavaScript + bastidores -> Back-end (Node), não Front-end",
        dict(matematica="media", atuacao="logica", ferramenta="javascript", entrega="produto",
             estilo="bastidores"),
        "BACK",
    ),
    (
        "JavaScript + usuário final -> Front-end, não Back-end",
        dict(matematica="media", atuacao="logica", ferramenta="javascript", entrega="produto",
             estilo="usuario"),
        "FRONT",
    ),
    (
        "Servidores + segurança -> Cibersegurança, não DevOps",
        dict(matematica="media", atuacao="servidores", ferramenta="linux_redes",
             entrega="seguranca", estilo="bastidores", foco_infra="automacao"),
        "SEC",
    ),
    (
        "Baixa matemática querendo modelos -> redireciona para Eng. de Dados",
        dict(matematica="baixa", atuacao="dados", ferramenta="python", entrega="insights",
             estilo="bastidores", foco_dados="modelos"),
        "DE",
    ),
]


class TestPersonas(unittest.TestCase):
    def test_personas_por_trilha(self):
        for nome, respostas, esperada in PERSONAS:
            with self.subTest(persona=nome):
                r = consultar(respostas)
                self.assertEqual(r.trilha_id, esperada, f"{nome}: ranking={r.ranking[:3]}")
                self.assertFalse(r.empate, f"{nome}: empate inesperado")

    def test_desambiguacao(self):
        for nome, respostas, esperada in DESAMBIGUACAO:
            with self.subTest(caso=nome):
                self.assertEqual(consultar(respostas).trilha_id, esperada)

    def test_todas_as_trilhas_sao_alcancaveis(self):
        alcancadas = {consultar(r).trilha_id for _, r, _ in PERSONAS}
        self.assertEqual(alcancadas, set(TRILHAS))

    def test_justificativa_nao_vazia(self):
        r = consultar(PERSONAS[0][1])
        self.assertTrue(r.regras_vencedora)
        self.assertTrue(all(i["motivo"] for i in r.regras_vencedora))

    def test_quantidade_de_regras(self):
        self.assertTrue(20 <= len(REGRAS) <= 25, f"{len(REGRAS)} regras")

    def test_pergunta_obrigatoria_faltando(self):
        with self.assertRaises(ValueError):
            consultar(dict(matematica="alta"))


if __name__ == "__main__":
    unittest.main()

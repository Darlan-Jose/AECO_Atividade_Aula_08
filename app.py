"""Interface web (Streamlit) do Consultor Inteligente de Carreiras em TI.
streamlit run app.py
"""
import streamlit as st

from consultor.motor import consultar
from consultor.perguntas import PERGUNTAS, limpar_respostas, perguntas_visiveis
from consultor.regras_meta import REGRAS
from consultor.trilhas import TRILHAS

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

st.title("🧭 Consultor Inteligente de Carreiras em TI")
st.caption("Sistema especialista baseado em regras (Experta) · UNIPAC Barbacena")

aba_consultor, aba_base = st.tabs(["Consultor", "Base de conhecimento"])


def coletar_respostas() -> dict:
    """Renderiza as perguntas de forma dinâmica e devolve as respostas atuais."""
    respostas: dict = {}
    for _ in range(len(PERGUNTAS)):
        visiveis = perguntas_visiveis(respostas)
        novas = {}
        for p in visiveis:
            rotulos = dict(p["opcoes"])
            escolha = st.session_state.get(f"q_{p['id']}")
            novas[p["id"]] = escolha if escolha in rotulos else None
        if {k: v for k, v in novas.items() if v} == respostas:
            break
        respostas = {k: v for k, v in novas.items() if v}
    return respostas

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


with aba_consultor:
    st.write("Responda às perguntas abaixo e o sistema recomendará a trilha mais adequada ao seu perfil.")

    respostas_atuais = coletar_respostas()
    respostas_finais: dict = {}

    for i, p in enumerate(perguntas_visiveis(respostas_atuais), start=1):
        rotulos = dict(p["opcoes"])
        escolha = st.radio(
            f"{i}. {p['texto']}",
            options=list(rotulos),
            format_func=lambda v, r=rotulos: r[v],
            index=None,
            key=f"q_{p['id']}",
        )
        if escolha:
            respostas_finais[p["id"]] = escolha

    respostas_finais = limpar_respostas(respostas_finais)
    completo = all(p["id"] in respostas_finais for p in perguntas_visiveis(respostas_finais))

    if st.button("Descobrir minha trilha", type="primary", disabled=not completo):
        st.session_state["resultado"] = (dict(respostas_finais), consultar(respostas_finais))

    guardado = st.session_state.get("resultado")
    resultado = guardado[1] if guardado and guardado[0] == respostas_finais else None
    if resultado and completo:
        st.divider()
        if resultado.trilha_id is None:
            st.warning(resultado.mensagem)
        else:
            trilha = resultado.trilha
            st.success(f"### Trilha recomendada: {trilha['nome']}")
            st.write(trilha["descricao"])
            st.metric("Aderência ao perfil", f"{resultado.aderencia}%")
            if resultado.empate:
                st.info(resultado.mensagem)

            st.subheader("Por que essa trilha?")
            for item in resultado.regras_vencedora:
                sinal = f"+{item['pontos']}" if item["pontos"] > 0 else str(item["pontos"])
                st.markdown(f"- **{item['id']}** ({sinal} pts): {item['motivo']}")

            st.subheader("Próximos passos")
            for passo in trilha["proximos_passos"]:
                st.markdown(f"- {passo}")

            st.subheader("Outras trilhas compatíveis")
            outras = [(tid, pts) for tid, pts in resultado.ranking[1:4] if pts > 0]
            if outras:
                for tid, pts in outras:
                    st.write(f"{TRILHAS[tid]['nome']}: {pts} pts")
            else:
                st.write("Nenhuma outra trilha pontuou. Seu perfil está bem definido.")

            with st.expander("Ver todas as regras disparadas (transparência do motor)"):
                for rid in resultado.regras_disparadas:
                    r = REGRAS[rid]
                    efeitos = ", ".join(
                        f"{TRILHAS[t]['nome']} {'+' if v > 0 else ''}{v}" for t, v in r["efeitos"].items()
                    )
                    st.markdown(f"**{rid}**: SE {r['condicao']} → {efeitos}")

            with st.expander("Ranking completo"):
                st.bar_chart({TRILHAS[t]["nome"]: pts for t, pts in resultado.ranking})


with aba_base:
    st.write(f"A base de conhecimento tem **{len(REGRAS)} regras** cruzando as respostas da entrevista.")
    for tid, t in TRILHAS.items():
        with st.expander(t["nome"]):
            st.caption(t["descricao"])
            for rid, r in REGRAS.items():
                if tid in r["efeitos"]:
                    pts = r["efeitos"][tid]
                    st.markdown(f"- **{rid}** ({'+' if pts > 0 else ''}{pts}): SE {r['condicao']}")

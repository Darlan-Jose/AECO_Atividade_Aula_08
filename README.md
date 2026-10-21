# Consultor Inteligente de Carreiras em TI
Sistema especialista baseado em regras que entrevista o usuário e recomenda uma entre 10 trilhas de carreira em TI, justificando a decisão com as regras disparadas.

## Tecnologias
- Python 3.10+
- [Experta](https://github.com/nilp0inter/experta): motor de regras SE-ENTÃO com encadeamento para frente
- [Streamlit](https://streamlit.io/): interface web
## Instalação e execução
```bash
# 1. (opcional) ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. dependências
pip install -r requirements.txt

# 3. interface web
streamlit run app.py

# 4. testes com personas
python -m unittest discover -s tests -v
```

> **Python 3.10+ e Experta:** o Experta 1.9.4 usa `collections.Mapping`, removido no Python 3.10.
> O arquivo `consultor/compat.py` corrige isso automaticamente. Se mesmo assim a instalação do `frozendict` falhar, use Python 3.9 ou crie o ambiente com `pip install frozendict==1.2 schema==0.6.7` antes.

## Como funciona
1. **Entrevista dinâmica**: 5 perguntas fixas (matemática, atuação diária, ferramenta, entrega de valor, estilo de interação) e 2 perguntas de aprofundamento que só aparecem quando fazem sentido (`foco_dados` e `foco_infra`).
2. **Motor de inferência**: as respostas viram um fato `Perfil`. As **25 regras** `@Rule` cruzam 2 ou 3 atributos e somam/subtraem pontos às trilhas.
3. **Decisão**: uma regra final de menor prioridade (`salience=-100`) dispara depois de todas as outras e escolhe a trilha com mais pontos (desempate: mais regras favoráveis).
4. **Justificativa transparente**: a tela mostra a trilha, as regras que a sustentaram, as demais regras disparadas e o ranking completo.
### Desambiguações tratadas

| Confusão comum | Como o sistema separa |
|---|---|
| Cientista × Engenheiro de Dados | `foco_dados` (modelos × pipelines) + matemática (R06–R10) |
| Back-end × Front-end | JavaScript + `estilo` (bastidores × usuário) (R03, R05) |
| DevOps × Cloud | `foco_infra` (automação × arquitetura) (R14–R17) |
| DevOps × Cibersegurança | servidores + entrega de segurança (R25) |

## Estrutura do repositório
```
.
├── app.py                    # Interface Streamlit (Fase 3)
├── gerar_matriz.py           # Gera docs/matriz_decisao.md
├── requirements.txt
├── consultor/
│   ├── compat.py             # Shim Experta × Python 3.10+
│   ├── trilhas.py            # As 10 trilhas e próximos passos
│   ├── perguntas.py          # Entrevista dinâmica
│   ├── regras_meta.py        # Metadados das 25 regras (pontos e justificativas)
│   └── motor.py              # Fatos (Fact) e regras (@Rule) do Experta (Fase 2)
├── docs/
│   └── matriz_decisao.md     # Matriz de decisão (Fase 1)
└── tests/
    └── test_personas.py      # Validação com personas (Fase 4)
```

## Validação (Fase 4)
`tests/test_personas.py` traz 10 personas (uma por trilha: analítico, infra/segurança, visual/frontend e negócios/produto) e 5 casos de desambiguação. Todas devem retornar a trilha esperada.

## Como ampliar
Para adicionar uma regra: (1) crie a entrada em `regras_meta.py` com condição, pontos e motivo; (2) crie o método com `@Rule(...)` em `motor.py` chamando `self._disparar("Rxx")`; (3) rode `python gerar_matriz.py` e os testes.

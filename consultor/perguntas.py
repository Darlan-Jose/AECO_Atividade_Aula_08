PERGUNTAS = [
    {
        "id": "matematica",
        "texto": "Qual é a sua afinidade com matemática e estatística?",
        "opcoes": [
            ("baixa", "Baixa"),
            ("media", "Média"),
            ("alta", "Alta"),
        ],
        "condicao": None,
    },
    {
        "id": "atuacao",
        "texto": "O que você gostaria de fazer no seu dia a dia de trabalho?",
        "opcoes": [
            ("logica", "Escrever algoritmos lógicos e regras de negócio"),
            ("visual", "Criar layouts e interfaces visuais"),
            ("servidores", "Lidar com servidores, ambientes e automação"),
            ("dados", "Analisar e trabalhar com dados brutos"),
            ("seguranca", "Garantir segurança e encontrar falhas"),
            ("testes", "Testar sistemas e garantir que funcionem"),
            ("mobile", "Criar aplicativos para celular"),
            ("gestao", "Organizar prioridades e alinhar pessoas e negócio"),
        ],
        "condicao": None,
    },
    {
        "id": "ferramenta",
        "texto": "Qual linguagem/ferramenta você tem mais afinidade hoje?",
        "opcoes": [
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("sql", "SQL / Bancos de dados"),
            ("linux_redes", "Linux / Redes"),
            ("mobile_lang", "Dart, Kotlin, Swift ou React Native"),
            ("nenhuma", "Nenhuma / Iniciante"),
        ],
        "condicao": None,
    },
    {
        "id": "entrega",
        "texto": "Que tipo de entrega de valor você prefere (objetivo profissional)?",
        "opcoes": [
            ("produto", "O produto final usado pelo usuário"),
            ("infra", "A infraestrutura que sustenta o sistema"),
            ("seguranca", "A segurança contra invasões"),
            ("insights", "Conhecimento extraído dos dados"),
            ("qualidade", "A qualidade e a confiabilidade do software"),
            ("estrategia", "A estratégia e o valor para o negócio"),
        ],
        "condicao": None,
    },
    {
        "id": "estilo",
        "texto": "Com quem/o quê você prefere interagir no trabalho?",
        "opcoes": [
            ("usuario", "Com o usuário final e o design"),
            ("bastidores", "Com sistemas e código, nos bastidores técnicos"),
            ("negocio", "Com áreas de negócio e stakeholders"),
        ],
        "condicao": None,
    },

    {
        "id": "foco_dados",
        "texto": "Em dados, o que mais te atrai?",
        "opcoes": [
            ("modelos", "Criar modelos preditivos e de IA"),
            ("pipelines", "Construir pipelines e a infraestrutura que movimenta os dados"),
        ],
        "condicao": lambda r: r.get("atuacao") == "dados" or r.get("entrega") == "insights",
    },
    {
        "id": "foco_infra",
        "texto": "Em infraestrutura, o que mais te atrai?",
        "opcoes": [
            ("automacao", "Automatizar deploys, CI/CD e contêineres"),
            ("arquitetura", "Planejar, migrar e gerir infraestrutura escalável na nuvem"),
        ],
        "condicao": lambda r: r.get("atuacao") == "servidores" or r.get("entrega") == "infra",
    },
]

ROTULOS = {
    p["id"]: {valor: rotulo for valor, rotulo in p["opcoes"]} for p in PERGUNTAS
}


def perguntas_visiveis(respostas: dict) -> list[dict]:
    """Retorna as perguntas que devem aparecer dado o que já foi respondido."""
    return [p for p in PERGUNTAS if p["condicao"] is None or p["condicao"](respostas)]


def limpar_respostas(respostas: dict) -> dict:
    """Mantém apenas respostas de perguntas visíveis e preenchidas."""
    visiveis = {p["id"] for p in perguntas_visiveis(respostas)}
    return {k: v for k, v in respostas.items() if k in visiveis and v}

REGRAS = {
    #Back-end
    "R01": {
        "condicao": "atuacao = lógica E estilo = bastidores",
        "efeitos": {"BACK": 4},
        "motivo": "Você gosta de escrever lógica e prefere atuar nos bastidores técnicos, perfil típico de quem constrói servidores e regras de negócio.",
    },
    "R02": {
        "condicao": "atuacao = lógica E ferramenta ∈ {Python, SQL}",
        "efeitos": {"BACK": 3},
        "motivo": "Python e SQL são ferramentas centrais para APIs, regras de negócio e bancos de dados.",
    },
    "R03": {
        "condicao": "ferramenta = JavaScript E atuacao = lógica E estilo = bastidores",
        "efeitos": {"BACK": 3},
        "motivo": "JavaScript com foco em lógica e bastidores aponta para back-end com Node.js, e não para interfaces.",
    },
    #Front-end
    "R04": {
        "condicao": "atuacao = visual",
        "efeitos": {"FRONT": 6},
        "motivo": "Criar layouts e interfaces visuais é a essência do front-end e do UI/UX.",
    },
    "R05": {
        "condicao": "ferramenta = JavaScript E estilo = usuário",
        "efeitos": {"FRONT": 4},
        "motivo": "JavaScript somado ao interesse pelo usuário final indica interfaces web e frameworks reativos.",
    },
    #Ciência de Dados
    "R06": {
        "condicao": "matematica = alta E atuacao = dados E foco_dados = modelos",
        "efeitos": {"DS": 7},
        "motivo": "Forte base matemática, trabalho com dados e interesse em modelos preditivos são o núcleo de Ciência de Dados e Machine Learning.",
    },
    "R07": {
        "condicao": "matematica = alta E ferramenta = Python E entrega = insights",
        "efeitos": {"DS": 3},
        "motivo": "Python com matemática forte e foco em extrair conhecimento dos dados reforça a vocação analítica.",
    },
    "R08": {
        "condicao": "matematica = baixa E foco_dados = modelos",
        "efeitos": {"DS": -4, "DE": 2},
        "motivo": "Modelagem preditiva exige base estatística. Com afinidade baixa, a Engenharia de Dados é um caminho mais viável para trabalhar com dados.",
    },
    #Engenharia de Dados
    "R09": {
        "condicao": "atuacao = dados E foco_dados = pipelines",
        "efeitos": {"DE": 6, "DS": -2},
        "motivo": "Preferir construir a infraestrutura que movimenta os dados (e não modelá-los) diferencia o Engenheiro de Dados do Cientista de Dados.",
    },
    "R10": {
        "condicao": "ferramenta ∈ {SQL, Python} E foco_dados = pipelines",
        "efeitos": {"DE": 3},
        "motivo": "SQL e Python são a base para pipelines ETL/ELT e Data Lakes.",
    },
    #Cibersegurança
    "R11": {
        "condicao": "atuacao = segurança",
        "efeitos": {"SEC": 6},
        "motivo": "Seu interesse diário em segurança e na busca por falhas é o centro da Cibersegurança.",
    },
    "R12": {
        "condicao": "entrega = segurança",
        "efeitos": {"SEC": 5},
        "motivo": "Você valoriza entregar proteção contra invasões, objetivo central de Security/Pentesting.",
    },
    "R13": {
        "condicao": "ferramenta = Linux/Redes E entrega = segurança",
        "efeitos": {"SEC": 3},
        "motivo": "Domínio de Linux e redes é base para defesa cibernética e redes seguras.",
    },
    "R25": {
        "condicao": "atuacao = servidores E entrega = segurança",
        "efeitos": {"SEC": 4},
        "motivo": "Quem trabalha com servidores mas valoriza segurança tende a se destacar em segurança de infraestrutura (DevSecOps), não apenas em automação.",
    },
    #DevOps & SRE
    "R14": {
        "condicao": "atuacao = servidores E foco_infra = automação",
        "efeitos": {"DEVOPS": 7},
        "motivo": "Lidar com servidores e querer automatizar deploys, CI/CD e contêineres define DevOps/SRE.",
    },
    "R15": {
        "condicao": "ferramenta = Linux/Redes E foco_infra = automação",
        "efeitos": {"DEVOPS": 3},
        "motivo": "Linux é o ambiente natural de contêineres, scripts e pipelines de automação.",
    },
    #Cloud
    "R16": {
        "condicao": "atuacao = servidores E foco_infra = arquitetura",
        "efeitos": {"CLOUD": 7},
        "motivo": "Planejar, migrar e gerir infraestrutura escalável é o foco da Arquitetura em Nuvem.",
    },
    "R17": {
        "condicao": "entrega = infraestrutura E foco_infra = arquitetura",
        "efeitos": {"CLOUD": 3},
        "motivo": "Valorizar a infraestrutura que sustenta o sistema, com visão de arquitetura, reforça o perfil de Cloud.",
    },
    #Mobile
    "R18": {
        "condicao": "atuacao = mobile",
        "efeitos": {"MOBILE": 6},
        "motivo": "Você quer criar aplicativos para celular, foco direto do desenvolvimento mobile.",
    },
    "R19": {
        "condicao": "ferramenta = Dart/Kotlin/Swift/React Native",
        "efeitos": {"MOBILE": 5},
        "motivo": "Sua afinidade com linguagens e frameworks mobile acelera a entrada nessa trilha.",
    },
    #QA
    "R20": {
        "condicao": "atuacao = testes",
        "efeitos": {"QA": 6},
        "motivo": "Gostar de testar sistemas e encontrar falhas é a base da Engenharia de Qualidade.",
    },
    "R21": {
        "condicao": "entrega = qualidade",
        "efeitos": {"QA": 5},
        "motivo": "Você valoriza a confiabilidade do software, objetivo central de QA.",
    },
    #Product Management
    "R22": {
        "condicao": "atuacao = gestão",
        "efeitos": {"PM": 6},
        "motivo": "Organizar prioridades e alinhar pessoas e negócio é o dia a dia de Gestão de Produtos.",
    },
    "R23": {
        "condicao": "entrega = estratégia",
        "efeitos": {"PM": 5},
        "motivo": "Você busca gerar valor para o negócio, o que define o papel de Product Manager.",
    },
    "R24": {
        "condicao": "estilo = negócio",
        "efeitos": {"PM": 3},
        "motivo": "Preferir interagir com áreas de negócio e stakeholders é típico de quem faz a ponte entre negócio, design e desenvolvimento.",
    },
}

REGRAS = dict(sorted(REGRAS.items()))

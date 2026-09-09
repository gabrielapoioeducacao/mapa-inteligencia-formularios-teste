import streamlit as st
from supabase import create_client

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Avaliação de Desempenho — Programa Psicólogos nas Escolas",
    page_icon="🏫",
    layout="centered",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .header-block {
        background: linear-gradient(135deg, #1a3a5c 0%, #2563a8 100%);
        color: white;
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .header-block h1 { font-size: 1.4rem; font-weight: 700; margin: 0 0 0.3rem 0; color: white; }
    .header-block p  { font-size: 0.9rem; opacity: 0.85; margin: 0; color: white; }

    .secao-titulo {
        background: #f0f4fb;
        border-left: 4px solid #2563a8;
        padding: 0.7rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        font-size: 1rem;
        color: #1a3a5c;
    }

    .comportamento {
        background: #f8f9fb;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #374151;
    }

    .aviso {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #9a3412;
        margin: 0.5rem 0 1.5rem 0;
    }

    .perfil-card {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        margin-bottom: 1rem;
    }
    .perfil-card:hover { border-color: #2563a8; background: #f0f4fb; }

    .badge-perfil {
        display: inline-block;
        background: #2563a8;
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 1rem;
    }

    .rodape {
        text-align: center;
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ── Conexão Supabase ─────────────────────────────────────────────────────────
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)

supabase = init_supabase()

# ── Constantes ───────────────────────────────────────────────────────────────
URES = [
    "Selecione a URE",
    "URE ADAMANTINA", "URE AMERICANA", "URE ANDRADINA", "URE APIAI",
    "URE ARACATUBA", "URE ARARAQUARA", "URE ASSIS", "URE AVARE",
    "URE BARRETOS", "URE BAURU", "URE BIRIGUI", "URE BOTUCATU",
    "URE BRAGANCA PAULISTA", "URE CAIEIRAS", "URE CAMPINAS LESTE",
    "URE CAMPINAS OESTE", "URE CAPIVARI", "URE CARAGUATATUBA",
    "URE CARAPICUIBA", "URE CATANDUVA", "URE CENTRO", "URE CENTRO OESTE",
    "URE CENTRO SUL", "URE DIADEMA", "URE FERNANDOPOLIS", "URE FRANCA",
    "URE GUARATINGUETA", "URE GUARULHOS NORTE", "URE GUARULHOS SUL",
    "URE ITAPECERICA DA SERRA", "URE ITAPETININGA", "URE ITAPEVA",
    "URE ITAPEVI", "URE ITAQUAQUECETUBA", "URE ITARARE", "URE ITU",
    "URE JABOTICABAL", "URE JACAREI", "URE JALES", "URE JAU",
    "URE JOSE BONIFACIO", "URE JUNDIAI", "URE LESTE 1", "URE LESTE 2",
    "URE LESTE 3", "URE LESTE 4", "URE LESTE 5", "URE LIMEIRA", "URE LINS",
    "URE MARILIA", "URE MAUA", "URE MIRACATU", "URE MIRANTE DO PARANAPANEMA",
    "URE MOGI DAS CRUZES", "URE MOGI MIRIM", "URE NORTE 1", "URE NORTE 2",
    "URE OSASCO", "URE OURINHOS", "URE PENAPOLIS", "URE PINDAMONHANGABA",
    "URE PIRACICABA", "URE PIRAJU", "URE PIRASSUNUNGA",
    "URE PRESIDENTE PRUDENTE", "URE REGISTRO", "URE RIBEIRAO PRETO",
    "URE SANTO ANASTACIO", "URE SANTO ANDRE", "URE SANTOS",
    "URE SAO BERNARDO DO CAMPO", "URE SAO CARLOS", "URE SAO JOAO DA BOA VISTA",
    "URE SAO JOAQUIM DA BARRA", "URE SAO JOSE DO RIO PRETO",
    "URE SAO JOSE DOS CAMPOS", "URE SAO ROQUE", "URE SAO VICENTE",
    "URE SERTAOZINHO", "URE SOROCABA", "URE SUL 1", "URE SUL 2", "URE SUL 3",
    "URE SUMARE", "URE SUZANO", "URE TABOAO DA SERRA", "URE TAQUARITINGA",
    "URE TAUBATE", "URE TUPA", "URE VOTORANTIM", "URE VOTUPORANGA",
]


LIDERES = [
    "Selecione o Líder",
    "ADRIANA DAS GRAÇAS CARDOSO CÂNDIDO",
    "AMANDA ACCIERI TONON",
    "BRUNA DA CONCEICAO BISPO",
    "BRUNO HENRIQUE DA SILVA TINEU",
    "CAMILA CRISTINA DE ARAUJO",
    "CHRISTIANIA SOARES DA SILVA",
    "CRISTIANIA SOARES DA SILVA",
    "DEVAIR AHRENS PIERAZO",
    "DIONI BALBINO DE MOURA",
    "EDUARDO DE OLIVEIRA",
    "EMERSON RODRIGUES ZEFERINO",
    "GISELLE DE JESUS SILVA",
    "HENDIOLI BALBINO DE SOUZA",
    "IVANA MARIA PEREIRA",
    "JACKELINE APARECIDA CARDOSO GONÇALVES",
    "JACKELINE CARDOSO SILVA",
    "JANDIRA SILVA COSTA",
    "JANAINA AMANDA MURBACH DA SILVA",
    "JENIFFER KETLIN TEODORO MIRANDA",
    "JESSICA FEITOSA BORGES DE BRITO",
    "JESSICA PIMENTEL BATISTA MACHADO",
    "KARINA BUENO DE SOUZA",
    "LAIS COLACINO IDA",
    "LARA FERNANDA LEAL VERRONI",
    "MAICON DO SANTOS",
    "MARIANA BORSARI BIRAGHI",
    "MARINEZ RITA SANTANIELLO",
    "MARIA JOSÉ FRANCISCA DE OLIVEIRA",
    "MARIA LUCIA DE MOURA",
    "MATHEUS FELTRIM",
    "MICHELI CRISTINA FEITOSA DA COSTA SANTOS",
    "MICHEL DOS SANTOS BISPO",
    "RAFAEL FARIA MOURA SOUZA",
    "RENATA CRISTINA DA SILVA MORAIS",
    "RENAN ROCHA LOPES",
    "TATIANE DE SANTANA JESUS",
    "THAIANE CAROLINE SIQUEIRA DONADAI",
    "VALDETE REGO FERREIRA",
    "VANESSA COELHO DA SILVA",
    "VICENTE ANGELO DA ROCHA",
    "VINÍCIUS PEREIRA MARQUES",
]

ESCALA = {
    "1 — Raramente observado": 1,
    "2 — Observado ocasionalmente, de forma inconsistente": 2,
    "3 — Observado adequadamente na maioria das situações": 3,
    "4 — Observado de forma consistente e contribui positivamente": 4,
    "5 — Observado como referência, fortalece continuamente a equipe": 5,
}

# Mapeia o código interno de cada item pro número da coluna no banco (1.1, 1.2, 2.1...)
ITEM_NUMERO = {
    "escuta_1": "1.1", "escuta_2": "1.2", "escuta_3": "1.3",
    "praxis_1": "2.1", "praxis_2": "2.2", "praxis_3": "2.3",
    "multiplicacao_1": "3.1", "multiplicacao_2": "3.2", "multiplicacao_3": "3.3",
    "etica_1": "4.1", "etica_2": "4.2", "etica_3": "4.3",
}

COMPETENCIAS = {
    "escuta": {
        "titulo": "Competência 1 — Escuta",
        "definicao": "Capacidade de compreender contextos, acolher diferentes perspectivas, estabelecer diálogo qualificado e considerar informações relevantes antes da definição de encaminhamentos.",
        "itens": [
            ("escuta_1", "1.1 Comunicação e disponibilidade para escuta",
             "O Líder comunica orientações de forma clara e demonstra disponibilidade para ouvir dúvidas, necessidades, sugestões e diferentes perspectivas relacionadas ao trabalho."),
            ("escuta_2", "1.2 Escuta e mediação",
             "O Líder escuta as diferentes partes envolvidas e atua na mediação de desafios, divergências e conflitos com equilíbrio, respeito e imparcialidade."),
            ("escuta_3", "1.3 Acolhimento e construção de relações colaborativas",
             "O Líder acolhe demandas e desafios apresentados pelos diferentes atores e contribui para a construção de relações de trabalho seguras, respeitosas e colaborativas."),
        ],
    },
    "praxis": {
        "titulo": "Competência 2 — Práxis",
        "definicao": "Capacidade de articular conhecimento, informações e experiência prática para planejar a atuação, tomar decisões qualificadas e refletir sobre as necessidades e desafios do território.",
        "itens": [
            ("praxis_1", "2.1 Planejamento e organização",
             "O Líder organiza o trabalho com clareza, estabelece prioridades, estrutura rotinas e acompanha a execução das ações de acordo com as necessidades do território."),
            ("praxis_2", "2.2 Uso de informações para a tomada de decisão",
             "O Líder utiliza registros, dados, relatos e outras informações disponíveis para compreender situações, orientar decisões e qualificar o planejamento das ações."),
            ("praxis_3", "2.3 Qualificação da atuação",
             "O Líder orienta e acompanha a atuação da equipe de forma coerente com as diretrizes do Programa, favorecendo intervenções contextualizadas, preventivas, coletivas e institucionalmente qualificadas."),
        ],
    },
    "multiplicacao": {
        "titulo": "Competência 3 — Multiplicação",
        "definicao": "Capacidade de compartilhar conhecimentos, promover aprendizagem, desenvolver pessoas e equipes e ampliar a autonomia dos atores envolvidos no trabalho.",
        "itens": [
            ("multiplicacao_1", "3.1 Desenvolvimento e feedback",
             "O Líder oferece orientações, acompanhamento e feedbacks que contribuem para o desenvolvimento profissional e o aprimoramento da atuação da equipe."),
            ("multiplicacao_2", "3.2 Aprendizagem e troca de conhecimentos",
             "O Líder promove ou viabiliza espaços de estudo, reflexão, análise de situações e troca de experiências que favorecem a aprendizagem coletiva."),
            ("multiplicacao_3", "3.3 Articulação e fortalecimento da autonomia",
             "O Líder articula-se com diferentes atores e espaços institucionais para fortalecer a atuação integrada e ampliar a autonomia das equipes e dos profissionais no território."),
        ],
    },
    "etica": {
        "titulo": "Competência 4 — Ética",
        "definicao": "Capacidade de atuar com responsabilidade, coerência, transparência, respeito às pessoas e às responsabilidades profissionais, preservando os limites de atuação e os princípios que orientam o Programa.",
        "itens": [
            ("etica_1", "4.1 Coerência e responsabilidade profissional",
             "O Líder atua de forma coerente com os princípios, diretrizes e responsabilidades institucionais do Programa, demonstrando respeito e responsabilidade em suas decisões e relações profissionais."),
            ("etica_2", "4.2 Respeito às responsabilidades e à autonomia profissional",
             "O Líder respeita as responsabilidades, os limites de atuação e a autonomia técnica dos diferentes profissionais, considerando suas atribuições e conhecimentos específicos."),
            ("etica_3", "4.3 Transparência e equidade",
             "O Líder conduz relações, decisões e pactuações com transparência, respeito e equidade, buscando assegurar tratamento justo e clareza nos acordos estabelecidos."),
        ],
    },
}

SEM_INSUMOS_KEY = "Não tenho insumos suficientes para avaliar"

# ── Session state ─────────────────────────────────────────────────────────────
if "pagina" not in st.session_state:
    st.session_state.pagina = "perfil"

# ── Cabeçalho (aparece em todas as páginas) ───────────────────────────────────
st.markdown("""
<div class="header-block">
    <h1>🏫 Avaliação de Desempenho e Competências</h1>
    <p>Programa Psicólogos nas Escolas — Bloco de Competências do Líder Regional</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — Seleção de perfil
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.pagina == "perfil":

    st.markdown("### Qual é o seu perfil?")
    st.markdown("Selecione o perfil que melhor descreve sua função no Programa para iniciar a avaliação.")
    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🧠")
        st.markdown("**Psicólogo**")
        st.markdown("Profissional de psicologia escolar atuando nas unidades.")
        if st.button("Sou Psicólogo", use_container_width=True, key="btn_psi"):
            st.session_state.perfil = "Psicólogo"
            st.session_state.pagina = "formulario"
            st.rerun()

    with col2:
        st.markdown("#### 📋")
        st.markdown("**PEC**")
        st.markdown("Profissional de Educação e Cultura vinculado à URE.")
        if st.button("Sou PEC", use_container_width=True, key="btn_pec"):
            st.session_state.perfil = "PEC"
            st.session_state.pagina = "formulario"
            st.rerun()

    with col3:
        st.markdown("#### 🏛️")
        st.markdown("**Gestor**")
        st.markdown("Gestor do Programa responsável pela supervisão regional.")
        if st.button("Sou Gestor", use_container_width=True, key="btn_ges"):
            st.session_state.perfil = "Gestor do Programa"
            st.session_state.pagina = "formulario"
            st.rerun()

    st.markdown("""
    <div class="rodape">
        Programa Psicólogos nas Escolas · Apoio Educação · Secretaria de Estado da Educação de São Paulo<br>
        As respostas são confidenciais e utilizadas exclusivamente para fins de desenvolvimento profissional.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 — Formulário completo
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pagina == "formulario":

    perfil = st.session_state.perfil

    # Badge do perfil selecionado + botão voltar
    col_badge, col_voltar = st.columns([3, 1])
    with col_badge:
        st.markdown(f'<span class="badge-perfil">👤 {perfil}</span>', unsafe_allow_html=True)
    with col_voltar:
        if st.button("← Voltar", key="btn_voltar"):
            st.session_state.pagina = "perfil"
            st.rerun()

    st.markdown("""
    Esta avaliação tem caráter **formativo e confidencial**. Responda considerando comportamentos 
    efetivamente observados durante o período de referência, com base em situações concretas.
    """)

    # ── Identificação ─────────────────────────────────────────────────────────
    st.markdown('<div class="secao-titulo">Identificação do Participante</div>', unsafe_allow_html=True)

    ure = st.selectbox("URE *", URES, index=0, placeholder="Digite para buscar sua URE...")
    email = st.text_input("E-mail institucional *", placeholder="nome@educacao.sp.gov.br")
    nome_lider = st.selectbox("Nome do Líder avaliado *", LIDERES, index=0, placeholder="Digite para buscar o nome do Líder...")

    # ── Competências ──────────────────────────────────────────────────────────
    respostas = {}

    for comp_key, comp in COMPETENCIAS.items():
        st.markdown(f'<div class="secao-titulo">{comp["titulo"]}</div>', unsafe_allow_html=True)
        st.caption(comp["definicao"])

        for campo, subtitulo, comportamento in comp["itens"]:
            st.markdown(f"**{subtitulo}**")
            st.markdown(f'<div class="comportamento">📋 {comportamento}</div>', unsafe_allow_html=True)

            opcoes = [SEM_INSUMOS_KEY] + list(ESCALA.keys())
            escolha = st.radio(
                "Avaliação:",
                opcoes,
                key=f"radio_{campo}",
                index=0,
                label_visibility="collapsed",
                horizontal=False,
            )

            if escolha == SEM_INSUMOS_KEY:
                respostas[campo] = {"nota": None, "sem_insumos": True, "opcao_texto": escolha}
            else:
                respostas[campo] = {"nota": ESCALA[escolha], "sem_insumos": False, "opcao_texto": escolha}

            st.divider()

    # ── Perguntas abertas ─────────────────────────────────────────────────────
    st.markdown('<div class="secao-titulo">Perguntas Abertas</div>', unsafe_allow_html=True)
    st.markdown('<div class="aviso">💡 Use as perguntas abaixo para registrar exemplos, situações ou aspectos relevantes que complementem sua avaliação.</div>', unsafe_allow_html=True)

    desenvolvimento = st.text_area(
        "Quais são as oportunidades de desenvolvimento do líder?",
        placeholder="Descreva aspectos que poderiam ser aprimorados e como...",
        height=120,
    )

    destaques = st.text_area(
        "Quais são os pontos de destaque do líder?",
        placeholder="Descreva situações concretas que ilustrem os pontos fortes observados...",
        height=120,
    )

    # Bloco exclusivo do Gestor
    entregas_nota = None
    entregas_sem_insumos = False
    entregas_gestor = None

    if perfil == "Gestor do Programa":
        st.markdown('<div class="secao-titulo">Bloco Exclusivo — Gestor do Programa</div>', unsafe_allow_html=True)
        st.markdown("Este bloco deve ser respondido somente pelo **Gestor do Programa**.")

        st.markdown("**Avaliação de Entregas**")
        st.markdown('<div class="comportamento">📋 Avalie o desempenho do líder em relação às entregas pactuadas sob sua responsabilidade no período.</div>', unsafe_allow_html=True)

        ESCALA_ENTREGAS = {
            "Não Avaliado — Sem insumos suficientes": None,
            "1 — Muito abaixo do esperado: Não realiza ou realiza de forma insuficiente as entregas.": 1,
            "2 — Abaixo do esperado: Realiza parte das entregas, com atrasos, inconsistências ou necessidade frequente de cobrança.": 2,
            "3 — Esperado: Realiza as entregas pactuadas dentro dos prazos e parâmetros estabelecidos.": 3,
            "4 — Acima do esperado: Realiza as entregas com qualidade, autonomia e consistência, antecipando necessidades.": 4,
            "5 — Referência: Realiza integralmente as entregas com elevada qualidade, autonomia e consistência, qualificando os processos.": 5,
        }

        escolha_entrega = st.radio(
            "Avaliação de Entregas:",
            list(ESCALA_ENTREGAS.keys()),
            key="radio_entregas",
            index=0,
            label_visibility="collapsed",
        )

        entregas_nota = ESCALA_ENTREGAS[escolha_entrega]
        entregas_sem_insumos = (escolha_entrega == "Não Avaliado — Sem insumos suficientes")
        entregas_opcao_texto = escolha_entrega

        st.divider()

        entregas_gestor = st.text_area(
            "Quais são os pontos de desenvolvimento e potenciais do líder em relação às entregas?",
            placeholder="Considere prazos, qualidade e consistência das entregas pactuadas...",
            height=120,
        )

    # ── Validação e envio ─────────────────────────────────────────────────────
    st.markdown("---")

    def validar():
        erros = []
        if ure == "Selecione a URE":
            erros.append("Selecione a URE.")
        if not email or "@" not in email:
            erros.append("Informe um e-mail institucional válido.")
        if nome_lider == "Selecione o Líder":
            erros.append("Selecione o nome do Líder avaliado.")
        return erros

    if st.button("✅ Enviar avaliação", type="primary", use_container_width=True):
        erros = validar()
        if erros:
            for e in erros:
                st.error(e)
        else:
            # ── Tudo em uma única linha: identificação + notas + qualitativo ──
            payload_avaliacao = {
                "ure": ure,
                "perfil_respondente": perfil,
                "email_respondente": email.strip().lower(),
                "nome_lider": nome_lider.strip(),
                "qualitativo_destaques": destaques.strip() or None,
                "qualitativo_desenvolvimento": desenvolvimento.strip() or None,
                "qualitativo_entregas_gestor": entregas_gestor.strip() if entregas_gestor else None,
                "5.1": entregas_nota,
            }

            for campo, numero in ITEM_NUMERO.items():
                payload_avaliacao[numero] = respostas[campo]["nota"]

            try:
                supabase.table("avaliacoes_lider").insert(payload_avaliacao).execute()
                st.session_state.pagina = "sucesso"
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao enviar a avaliação. Tente novamente. Detalhes: {e}")

    st.markdown("""
    <div class="rodape">
        Programa Psicólogos nas Escolas · Apoio Educação · Secretaria de Estado da Educação de São Paulo<br>
        As respostas são confidenciais e utilizadas exclusivamente para fins de desenvolvimento profissional.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 — Confirmação de envio
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pagina == "sucesso":

    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem;">
        <div style="font-size: 4rem;">✅</div>
        <h2 style="color: #1a3a5c; margin-top: 1rem;">Avaliação enviada com sucesso!</h2>
        <p style="color: #6b7280; font-size: 1rem; margin-top: 0.5rem;">
            Obrigado pela sua participação. Suas respostas foram registradas e serão utilizadas 
            exclusivamente para fins de desenvolvimento profissional.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📋 Responder nova avaliação", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown("""
    <div class="rodape">
        Programa Psicólogos nas Escolas · Apoio Educação · Secretaria de Estado da Educação de São Paulo<br>
        As respostas são confidenciais e utilizadas exclusivamente para fins de desenvolvimento profissional.
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
import requests
import random
import html

st.set_page_config(page_title="Quiz Python")
st.title("Quiz com Python")
st.caption("Powered by Open Trivia Database")

st.sidebar.header("⚙️ Configurações")

quantidade = st.sidebar.slider(
    "Número de perguntas",
    3,
    10,
    5
)

categoria = st.sidebar.selectbox(
    "Categoria",
    [
        ("Geral", 9),
        ("Filmes", 11),
        ("Computação", 18),
        ("Esportes", 21),
        ("História", 23),
    ],
    format_func=lambda x: x[0]
)

dificuldade = st.sidebar.selectbox(
    "Dificuldade",
    ["easy", "medium", "hard"]
)

def buscar_perguntas(quantidade, categoria_id, dificuldade):
    url = "https://opentdb.com/api.php"

    params = {
        "amount": quantidade,
        "category": categoria_id,
        "difficulty": dificuldade,
        "type": "multiple"
    }
    resposta = requests.get(url, params=params)

    dados = resposta.json()

    return dados["results"]


def montar_alternativas(pergunta):

    correta = pergunta["correct_answer"]

    erradas = pergunta["incorrect_answers"]

    alternativas = [correta] + erradas

    random.shuffle(alternativas)

    return alternativas



if st.sidebar.button("Iniciar Quiz"):
    perguntas = buscar_perguntas(
        quantidade,
        categoria[1],
        dificuldade
    )
    st.session_state["perguntas"] = perguntas
    st.session_state["alternativas"] = [
        montar_alternativas(pergunta)
        for pergunta in perguntas
    ]
    st.session_state["respostas"] = {}


if "perguntas" not in st.session_state or not st.session_state["perguntas"]:
    st.info(
        "Configure o quiz na barra lateral e clique em Iniciar Quiz."
    )
    st.stop()


perguntas = st.session_state["perguntas"]
respostas = st.session_state["respostas"]
alternativas_salvas = st.session_state["alternativas"]


for i, pergunta in enumerate(perguntas):
    texto = html.unescape(pergunta["question"])
    alternativas = [
        html.unescape(a)
        for a in alternativas_salvas[i]
    ]
    st.subheader(
        f"Pergunta {i + 1} de {len(perguntas)}"
    )
    st.write(texto)
    escolha = st.radio(
        "Escolha uma alternativa:",
        options=alternativas,
        key=f"q{i}"
    )
    respostas[i] = escolha
    st.divider()


if st.button(" Ver resultado"):
    corretas = 0
    for i, pergunta in enumerate(perguntas):
        gabarito = html.unescape(
            pergunta["correct_answer"]
        )
        escolha = respostas.get(i)
        if escolha == gabarito:
            corretas += 1

    st.metric(
        "Pontuação",
        f"{corretas}/{len(perguntas)}"
    )
    percentual = corretas / len(perguntas)
    mensagens = {
        "excelente": "✨✨Arrasou divo! Você divou!✨✨",
        "bom": "Tá bom, mas dá para melhorar! Você não divou totalmente ainda 🤡",
        "tente_novamente": "Péssimo você é um labubu!"
    }
    if percentual >= 0.8:
        st.success(
            mensagens["excelente"]
        )
    elif percentual >= 0.5:
        st.info(
            mensagens["bom"]
        )
    else:
        st.warning(
            mensagens["tente_novamente"]
        )

    st.subheader("Gabarito")
    for i, pergunta in enumerate(perguntas):
        gabarito = html.unescape(
            pergunta["correct_answer"]
        )
        escolha = respostas.get(i)
        if escolha == gabarito:
            st.success(
                f"Pergunta {i + 1}: correta!"
            )
        else:
            st.error(
                f"Pergunta {i + 1}: errada. "
                f"Resposta correta: {gabarito}"
            )
import streamlit as st
import requests
import random

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

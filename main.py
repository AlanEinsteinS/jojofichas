import streamlit as st
import plotly.graph_objects as go
import json

# Cabeçalho com link para GitHub


def create_progress_bar(value, max_value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={'axis': {'range': [0, max_value]},
               'bar': {'color': color}},
    ))
    fig.update_layout(height=150, margin={'t': 0, 'b': 0, 'l': 0, 'r': 0})
    st.plotly_chart(fig, use_container_width=True)

def save_data(data, filename="rpg_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f)
    st.success(f"Ficha salva com sucesso em {filename}!")

def load_data(filename="rpg_data.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("Nenhum arquivo de dados encontrado.")
        return None

# Aplicar estilos CSS para um tema escuro
st.markdown(
    """
    <style>
    body {
        color: #d4d4d4;
        background-color: #1e1e1e;
    }
    .st-bw {
        color: #d4d4d4;
    }
    .st-cc {
        color: #d4d4d4 !important;
    }
    .st-bv {
        background: #1e1e1e;
    }
    .st-ez {
        background-color: #252525;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do site
st.title('JoJo Fichas')
st.markdown('<p style="text-align: center;"><a href="https://github.com/AlanEinsteinS" target="_blank" style="color: #FFFFFF; text-decoration: none;">Made by dark</a></p>', unsafe_allow_html=True)
# Carregar dados se o arquivo for enviado

uploaded_file = st.file_uploader("Carregar Ficha", type=["json"])
if uploaded_file:
    st.session_state.ficha = json.load(uploaded_file)

# Inicializar dados se não estiverem no estado da sessão
if "ficha" not in st.session_state:
    st.session_state.ficha = {
        "nome_usuario": "",
        "nome_stand": "",
        "atributos": {
            "forca": "E",
            "velocidade": "E",
            "precisao": "E",
            "durabilidade": "E",
            "potencia": "E"
        },
        "status": {
            "vida": 50,
            "stamina": 50,
            "impulso": 50,
            "forca_vontade": 50
        },
        "inventario": "",
        "habilidades": []
    }

# Informações do Usuário
st.header("Informações do Usuário")
st.session_state.ficha["nome_usuario"] = st.text_input("Nome do usuário", st.session_state.ficha["nome_usuario"])
st.session_state.ficha["nome_stand"] = st.text_input("Nome do stand", st.session_state.ficha["nome_stand"])

# Atributos com rank de E a A
st.header("Atributos")
rank_choices = ["E", "D", "C", "B", "A"]
cols = st.columns(5)
for i, atributo in enumerate(["forca", "velocidade", "precisao", "durabilidade", "potencia"]):
    st.session_state.ficha["atributos"][atributo] = cols[i].selectbox(atributo.capitalize(), rank_choices, index=rank_choices.index(st.session_state.ficha["atributos"][atributo]))

# Barras de Vida, Stamina, Impulso e Força de Vontade
st.header("Status")
status_cols = st.columns(4)
for i, status in enumerate(["vida", "stamina", "impulso", "forca_vontade"]):
    st.session_state.ficha["status"][status] = status_cols[i].slider(status.capitalize(), 0, 100, st.session_state.ficha["status"][status])

# Barras de progresso coloridas
st.subheader("Barras de Progresso")
create_progress_bar(st.session_state.ficha["status"]["vida"], 100, 'red')
create_progress_bar(st.session_state.ficha["status"]["stamina"], 100, 'green')
create_progress_bar(st.session_state.ficha["status"]["impulso"], 100, 'blue')
create_progress_bar(st.session_state.ficha["status"]["forca_vontade"], 100, 'purple')

# Inventário
st.header("Inventário")
st.session_state.ficha["inventario"] = st.text_area("Inventário", st.session_state.ficha["inventario"])

# Habilidades
st.header("Habilidades")

if "new_habilidades" not in st.session_state:
    st.session_state.new_habilidades = []

def adicionar_habilidade():
    with st.form(key='habilidade_form', clear_on_submit=True):
        nome_habilidade = st.text_input("Nome da Habilidade")
        descricao_habilidade = st.text_area("Descrição")
        custo_habilidade = st.number_input("Custo", min_value=0)
        submit_button = st.form_submit_button(label='Adicionar Habilidade')

        if submit_button and nome_habilidade and descricao_habilidade:
            st.session_state.ficha["habilidades"].append({
                "nome": nome_habilidade,
                "descricao": descricao_habilidade,
                "custo": custo_habilidade
            })
            st.success("Habilidade adicionada com sucesso!")

# Botão para adicionar habilidade
adicionar_habilidade()

# Mostrar habilidades adicionadas
if st.session_state.ficha["habilidades"]:
    st.subheader("Lista de Habilidades")
    for idx, habilidade in enumerate(st.session_state.ficha["habilidades"]):
        with st.expander(f"Habilidade {idx+1}: {habilidade['nome']}"):
            st.write(f"*Descrição:* {habilidade['descricao']}")
            st.write(f"*Custo:* {habilidade['custo']}")

# Botão para salvar a ficha em um arquivo JSON
if st.button("Salvar Ficha"):
    save_data(st.session_state.ficha)

# Botão para baixar a ficha em um arquivo JSON
ficha_json = json.dumps(st.session_state.ficha)
st.download_button(
    label="Baixar Ficha",
    data=ficha_json,
    file_name="ficha_rpg.json",
    mime="application/json"
)

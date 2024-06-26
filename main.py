import streamlit as st
import json

# Função para salvar dados em um arquivo JSON
def save_data(data, filename="rpg_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    st.success(f"Ficha salva com sucesso em {filename}!")

# Função para carregar dados de um arquivo JSON
def load_data(filename="rpg_data.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("Nenhum arquivo de dados encontrado.")
        return None

# Aplicando a fonte Montserrat para todo o app
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    body {
        font-family: 'Montserrat', sans-serif;
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

    /* Increase font size for sliders */
    .stSlider .streamlit-slider .slider-value span {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do aplicativo
st.title('JoJo Fichas')
st.markdown('<p style="text-align: center;"><a href="https://github.com/AlanEinsteinS" target="_blank" style="color: #FFFFFF; text-decoration: none;">Made by dark</a></p>', unsafe_allow_html=True)

# Carregar dados se um arquivo JSON for enviado
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
            "potencial": "E",
            "alcance": "E"
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

# Informações do usuário
st.header("Informações do Usuário")
st.session_state.ficha["nome_usuario"] = st.text_input("Nome do usuário", st.session_state.ficha["nome_usuario"])
st.session_state.ficha["nome_stand"] = st.text_input("Nome do stand", st.session_state.ficha["nome_stand"])

# Atributos com classificação de E a A
st.header("Atributos")
rank_choices = ["E", "D", "C", "B", "A", "S", "S+", "X"]
cols = st.columns(6)
for i, atributo in enumerate(["forca", "velocidade", "precisao", "durabilidade", "potencial", "alcance"]):
    st.session_state.ficha["atributos"][atributo] = cols[i].selectbox(atributo.capitalize(), rank_choices, index=rank_choices.index(st.session_state.ficha["atributos"][atributo]))

# Barras de Vida, Stamina, Impulso e Força de Vontade
st.header("Status")

# Função para criar sliders coloridos
def create_colored_slider(label, status_key, color, default_max=500):
    st.subheader(label)
    st.markdown(f'<style>.st-eb {{color: {color} !important}}</style>', unsafe_allow_html=True)
    max_value = st.session_state.ficha["status"].get(f"{status_key}_max", default_max)
    max_value = st.number_input(f'Máximo para {label.lower()}', min_value=1, value=max_value)
    st.session_state.ficha["status"][status_key] = st.slider(
        label,
        0, max_value,
        st.session_state.ficha["status"][status_key],
        key=status_key,
        help=f"Nível de {label.lower()} do personagem",
        step=1,
    )
    st.session_state.ficha["status"][f"{status_key}_max"] = max_value  # Salvar o valor máximo no estado da sessão

# Criar sliders coloridos para cada status
create_colored_slider("Vida", "vida", "#FF5733")
create_colored_slider("Stamina", "stamina", "#33FF5E")
create_colored_slider("Impulso", "impulso", "#337CFF")
create_colored_slider("Força de Vontade", "forca_vontade", "#A933FF")

# Inventário
st.header("Inventário")
st.session_state.ficha["inventario"] = st.text_area("Inventário", st.session_state.ficha["inventario"])

# Habilidades
st.header("Habilidades")

# Função para adicionar habilidades
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

# Adicionar habilidade
adicionar_habilidade()

# Função para excluir habilidades
def excluir_habilidade(index):
    st.session_state.ficha["habilidades"].pop(index)
    st.success("Habilidade excluída com sucesso!")

# Mostrar habilidades adicionadas
if st.session_state.ficha["habilidades"]:
    st.subheader("Lista de Habilidades")
    for idx, habilidade in enumerate(st.session_state.ficha["habilidades"]):
        with st.expander(f"Habilidade {idx+1}: {habilidade['nome']}"):
            st.write(f"*Descrição:* {habilidade['descricao']}")
            st.write(f"*Custo:* {habilidade['custo']}")
            # Opções para editar ou excluir habilidade
            edit_habilidade = st.checkbox(f"Editar Habilidade {idx+1}")
            if edit_habilidade:
                nome_habilidade_editar = st.text_input("Novo nome da habilidade", value=habilidade['nome'])
                descricao_habilidade_editar = st.text_area("Nova descrição", value=habilidade['descricao'])
                custo_habilidade_editar = st.number_input("Novo custo", value=habilidade['custo'])
                if st.button("Salvar Edição"):
                    habilidade['nome'] = nome_habilidade_editar
                    habilidade['descricao'] = descricao_habilidade_editar
                    habilidade['custo'] = custo_habilidade_editar
                    st.success("Habilidade editada com sucesso!")
            delete_habilidade = st.checkbox(f"Excluir Habilidade {idx+1}")
            if delete_habilidade:
                if st.button("Confirmar Exclusão"):
                    excluir_habilidade(idx)  # Chama a função para excluir a habilidade pelo índice atual

# Botão para salvar a ficha de personagem em um arquivo JSON
if st.button("Salvar Ficha"):
    save_data(st.session_state.ficha)

# Botão para baixar a ficha de personagem como um arquivo JSON
ficha_json = json.dumps(st.session_state.ficha, indent=4)
st.download_button(
    label="Baixar Ficha",
    data=ficha_json,
    file_name="ficha_rpg.json",
    mime="application/json"
)

import streamlit as st
import pickle
import os

# Função para salvar os dados inseridos localmente
def salvar_dados_localmente(nome_usuario, dados):
    try:
        # Obter o caminho da área de trabalho do usuário
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

        # Criar diretório se não existir
        save_dir = os.path.join(desktop_path, 'saves')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Salvar dados em um arquivo com nome do usuário
        file_path = os.path.join(save_dir, f'{nome_usuario}_dados_salvos.pkl')
        with open(file_path, 'wb') as f:
            pickle.dump(dados, f)
        st.success('Dados salvos localmente com sucesso!')
    except Exception as e:
        st.error(f'Erro ao salvar dados: {e}')

# Função para carregar todos os saves de um usuário
def carregar_saves_usuario(nome_usuario):
    try:
        saves = []
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        save_dir = os.path.join(desktop_path, 'saves')
        
        save_files = [f for f in os.listdir(save_dir) if f.startswith(f'{nome_usuario}_')]
        
        for file in save_files:
            file_path = os.path.join(save_dir, file)
            with open(file_path, 'rb') as f:
                dados = pickle.load(f)
                saves.append(dados)
        
        return saves
    except Exception as e:
        st.error(f'Erro ao carregar saves do usuário: {e}')
        return []

# Estilo customizado
st.markdown(
    """
    <style>
    body {
        color: #FFFFFF; /* Cor do texto */
        background-color: #000000; /* Cor de fundo */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Fonte */
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF; /* Cor do título principal */
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF; /* Cor do título de seção */
        margin-top: 20px;
        border-bottom: 2px solid #FFFFFF; /* Linha de separação */
        padding-bottom: 10px;
    }
    .data-entry {
        font-size: 16px;
        margin-bottom: 10px;
    }
    .data-entry strong {
        color: #FFFFFF; /* Cor do texto em negrito */
    }
    </style>
    """, unsafe_allow_html=True
)

# Cabeçalho com link para GitHub
st.markdown('<p class="main-title">JoJo Fichas</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;"><a href="https://github.com/AlanEinsteinS" target="_blank" style="color: #FFFFFF; text-decoration: none;">Made by dark</a></p>', unsafe_allow_html=True)

# Dados do usuário
st.markdown('<p class="section-header">Dados do Usuário</p>', unsafe_allow_html=True)
nome_usuario = st.text_input('Nome do Usuário', key='nome_usuario')

# Dados do Stand
st.markdown('<p class="section-header">Dados do Stand</p>', unsafe_allow_html=True)
nome_stand = st.text_input('Nome do Stand', key='nome_stand')
impulso = st.text_input('Impulso', key='impulso')
forca_contato = st.text_input('Força de Contato', key='forca_contato')
stamina = st.text_input('Stamina', key='stamina')
habilidades = st.text_area('Habilidades', height=200, key='habilidades')
fraquezas = st.text_area('Fraquezas', height=200, key='fraquezas')
aparencia_stand = st.text_area('Aparência do Stand / Forma', height=200, key='aparencia_stand')
condicao_ferimento = st.text_input('Condição do Ferimento', key='condicao_ferimento')
condicoes = st.text_area('Condições', height=200, key='condicoes')
tecnicas = st.text_area('Técnicas', height=200, key='tecnicas')
anotacoes_stand = st.text_area('Anotações do Stand / Ações', height=200, key='anotacoes_stand')

# Traits do Stand
st.markdown('<p class="section-header">Traits do Stand</p>', unsafe_allow_html=True)
poder = st.selectbox('Poder', ['A', 'B', 'C', 'D', 'E'], key='poder')
velocidade = st.selectbox('Velocidade', ['A', 'B', 'C', 'D', 'E'], key='velocidade')
alcance = st.selectbox('Alcance', ['A', 'B', 'C', 'D', 'E'], key='alcance')
durabilidade = st.selectbox('Durabilidade', ['A', 'B', 'C', 'D', 'E'], key='durabilidade')
precisao = st.selectbox('Precisão', ['A', 'B', 'C', 'D', 'E'], key='precisao')
potencial = st.selectbox('Potencial', ['A', 'B', 'C', 'D', 'E'], key='potencial')

# Botão para salvar os dados
if st.button('Salvar Dados'):
    dados = {
        "nome_usuario": nome_usuario,
        "nome_stand": nome_stand,
        "impulso": impulso,
        "forca_contato": forca_contato,
        "stamina": stamina,
        "habilidades": habilidades,
        "fraquezas": fraquezas,
        "aparencia_stand": aparencia_stand,
        "condicao_ferimento": condicao_ferimento,
        "condicoes": condicoes,
        "tecnicas": tecnicas,
        "anotacoes_stand": anotacoes_stand,
        "poder": poder,
        "velocidade": velocidade,
        "alcance": alcance,
        "durabilidade": durabilidade,
        "precisao": precisao,
        "potencial": potencial
    }
    salvar_dados_localmente(nome_usuario, dados)

# Botão para carregar todos os saves do usuário
if st.button('Ver Todos os Saves'):
    saves_usuario = carregar_saves_usuario(nome_usuario)
    if saves_usuario:
        st.markdown('<p class="section-header">Todos os Saves</p>', unsafe_allow_html=True)
        for idx, save in enumerate(saves_usuario):
            st.markdown(f'<p class="data-entry"><strong>Save {idx + 1}</strong></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Nome do Stand:</strong> {save["nome_stand"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Impulso:</strong> {save["impulso"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Força de Contato:</strong> {save["forca_contato"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Stamina:</strong> {save["stamina"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Habilidades:</strong></p><p>{save["habilidades"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Fraquezas:</strong></p><p>{save["fraquezas"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Aparência do Stand / Forma:</strong></p><p>{save["aparencia_stand"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Condição do Ferimento:</strong> {save["condicao_ferimento"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Condições:</strong></p><p>{save["condicoes"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Técnicas:</strong></p><p>{save["tecnicas"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Anotações do Stand / Ações:</strong></p><p>{save["anotacoes_stand"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Poder:</strong> {save["poder"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Velocidade:</strong> {save["velocidade"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Alcance:</strong> {save["alcance"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Durabilidade:</strong> {save["durabilidade"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Precisão:</strong> {save["precisao"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="data-entry"><strong>Velocidade:</strong> {save["velocidade"]}</p>', unsafe_allow_html=True)
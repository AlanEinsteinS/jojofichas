import streamlit as st
import json
import base64
from datetime import datetime

class RPGCharacterSheet:
    def __init__(self):
        # Initialize the character sheet with more comprehensive default values
        self.default_ficha = {
            "info": {
                "nome_usuario": "",
                "nome_stand": "",
                "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ultima_edicao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "atributos": {
                "forca": "E",
                "velocidade": "E", 
                "precisao": "E",
                "durabilidade": "E",
                "potencial": "E",
                "alcance": "E"
            },
            "status": {
                "vida": {"atual": 50, "max": 500},
                "stamina": {"atual": 50, "max": 500},
                "impulso": {"atual": 50, "max": 500},
                "forca_vontade": {"atual": 50, "max": 500}
            },
            "inventario": [],
            "habilidades": [],
            "historia": "",
            "notas_extras": ""
        }

    def aplicar_estilo_personalizado(self):
        """Aplicar estilo personalizado para o aplicativo"""
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Montserrat:wght@400;700&display=swap');
        
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #121212;
            color: #e0e0e0;
        }
        
        .main .block-container {
            background-color: #1e1e1e;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: #252525;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #a0a0a0;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff;
            background-color: #353535;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #00ffff;
            background-color: #353535;
        }
        
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: #00ffff;
        }
        
        .stButton>button {
            background-color: #00ffff;
            color: #121212;
            font-weight: bold;
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #00cccc;
            transform: scale(1.05);
        }
        
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea, 
        .stSelectbox>div>div>select {
            background-color: #252525 !important;
            color: #e0e0e0 !important;
            border: 1px solid #353535 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def save_data(self, data, filename="rpg_data.json"):
        """Salvar dados em um arquivo JSON"""
        data["info"]["ultima_edicao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        st.success(f"Ficha salva com sucesso em {filename}!")

    def load_data(self, filename="rpg_data.json"):
        """Carregar dados de um arquivo JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.warning("Nenhum arquivo de dados encontrado.")
            return None

    def criar_interface_ficha(self):
        """Criar interface completa para a ficha de personagem"""
        # Inicializar ficha se não existir
        if "ficha" not in st.session_state:
            st.session_state.ficha = self.default_ficha.copy()

        # Tabs para organizar a ficha
        tab1, tab2, tab3, tab4 = st.tabs(["Informações", "Atributos", "Status", "Habilidades"])

        with tab1:
            self._criar_aba_informacoes()

        with tab2:
            self._criar_aba_atributos()

        with tab3:
            self._criar_aba_status()

        with tab4:
            self._criar_aba_habilidades()

        # Botões de ação na parte inferior
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Salvar Ficha", key="salvar_ficha"):
                self.save_data(st.session_state.ficha)

        with col2:
            ficha_json = json.dumps(st.session_state.ficha, indent=4, ensure_ascii=False)
            st.download_button(
                label="Baixar Ficha",
                data=ficha_json,
                file_name=f"ficha_rpg_{st.session_state.ficha['info']['nome_stand']}.json",
                mime="application/json"
            )

        with col3:
            uploaded_file = st.file_uploader("Carregar Ficha", type=["json"])
            if uploaded_file:
                try:
                    st.session_state.ficha = json.load(uploaded_file)
                    st.success("Ficha carregada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao carregar ficha: {e}")

    def _criar_aba_informacoes(self):
        """Criar aba de informações pessoais"""
        st.header("Informações do Stand")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.ficha["info"]["nome_usuario"] = st.text_input(
                "Nome do Usuário", 
                st.session_state.ficha["info"]["nome_usuario"]
            )
        with col2:
            st.session_state.ficha["info"]["nome_stand"] = st.text_input(
                "Nome do Stand", 
                st.session_state.ficha["info"]["nome_stand"]
            )

        st.text_area(
            "História do Stand", 
            st.session_state.ficha["historia"], 
            key="historia_stand",
            on_change=lambda: st.session_state.ficha.update({"historia": st.session_state.historia_stand})
        )

        st.text_area(
            "Notas Extras", 
            st.session_state.ficha["notas_extras"], 
            key="notas_extras_stand",
            on_change=lambda: st.session_state.ficha.update({"notas_extras": st.session_state.notas_extras_stand})
        )

        # Mostrar data de criação e última edição
        st.markdown(f"""
        **Criado em:** {st.session_state.ficha['info'].get('data_criacao', 'N/A')}
        **Última Edição:** {st.session_state.ficha['info'].get('ultima_edicao', 'N/A')}
        """)

    def _criar_aba_atributos(self):
        """Criar aba de atributos do Stand"""
        st.header("Atributos do Stand")
        
        rank_choices = ["E", "D", "C", "B", "A", "S", "S+", "X"]
        
        cols = st.columns(3)
        atributos = ["forca", "velocidade", "precisao"]
        
        for i, atributo in enumerate(atributos):
            with cols[i]:
                st.session_state.ficha["atributos"][atributo] = st.selectbox(
                    atributo.capitalize(), 
                    rank_choices, 
                    index=rank_choices.index(st.session_state.ficha["atributos"][atributo])
                )
        
        cols = st.columns(3)
        atributos = ["durabilidade", "potencial", "alcance"]
        
        for i, atributo in enumerate(atributos):
            with cols[i]:
                st.session_state.ficha["atributos"][atributo] = st.selectbox(
                    atributo.capitalize(), 
                    rank_choices, 
                    index=rank_choices.index(st.session_state.ficha["atributos"][atributo])
                )

    def _criar_aba_status(self):
        """Criar aba de status do personagem"""
        st.header("Status do Personagem")
        
        status_colors = {
            "vida": "#FF5733",
            "stamina": "#33FF5E", 
            "impulso": "#337CFF", 
            "forca_vontade": "#A933FF"
        }
        
        for status_key, color in status_colors.items():
            st.subheader(status_key.replace("_", " ").title())
            
            # Configurar estilo do slider
            st.markdown(f'<style>.st-eb {{color: {color} !important}}</style>', unsafe_allow_html=True)
            
            # Slider para status atual
            st.session_state.ficha["status"][status_key]["atual"] = st.slider(
                f"Valor Atual de {status_key.replace('_', ' ').title()}",
                0, 
                st.session_state.ficha["status"][status_key]["max"], 
                st.session_state.ficha["status"][status_key]["atual"],
                key=f"{status_key}_atual"
            )
            
            # Input para valor máximo
            st.session_state.ficha["status"][status_key]["max"] = st.number_input(
                f"Valor Máximo para {status_key.replace('_', ' ').title()}",
                min_value=1, 
                value=st.session_state.ficha["status"][status_key]["max"],
                key=f"{status_key}_max"
            )

    def _criar_aba_habilidades(self):
        """Criar aba de gerenciamento de habilidades"""
        st.header("Habilidades do Stand")
        
        # Adicionar nova habilidade
        with st.expander("Adicionar Nova Habilidade"):
            with st.form(key='nova_habilidade', clear_on_submit=True):
                nome = st.text_input("Nome da Habilidade")
                descricao = st.text_area("Descrição")
                custo = st.number_input("Custo", min_value=0)
                submit = st.form_submit_button("Adicionar")
                
                if submit and nome and descricao:
                    nova_habilidade = {
                        "nome": nome,
                        "descricao": descricao,
                        "custo": custo
                    }
                    st.session_state.ficha["habilidades"].append(nova_habilidade)
                    st.success("Habilidade adicionada com sucesso!")
        
        # Listar e gerenciar habilidades existentes
        if st.session_state.ficha["habilidades"]:
            st.subheader("Habilidades Existentes")
            for idx, habilidade in enumerate(st.session_state.ficha["habilidades"]):
                with st.expander(f"{habilidade['nome']} (Custo: {habilidade['custo']})"):
                    # Campos editáveis
                    nome_edit = st.text_input("Nome", value=habilidade['nome'], key=f"nome_{idx}")
                    descricao_edit = st.text_area("Descrição", value=habilidade['descricao'], key=f"desc_{idx}")
                    custo_edit = st.number_input("Custo", value=habilidade['custo'], min_value=0, key=f"custo_{idx}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Salvar Alterações", key=f"salvar_{idx}"):
                            habilidade['nome'] = nome_edit
                            habilidade['descricao'] = descricao_edit
                            habilidade['custo'] = custo_edit
                            st.success("Habilidade atualizada!")
                    
                    with col2:
                        if st.button("Excluir Habilidade", key=f"excluir_{idx}"):
                            st.session_state.ficha["habilidades"].pop(idx)
                            st.success("Habilidade removida!")
                            st.experimental_rerun()

def main():
    # Configurações iniciais do Streamlit
    st.set_page_config(
        page_title="JoJo RPG Character Sheet", 
        page_icon=":star:", 
        layout="wide"
    )

    # Criar instância da classe
    app = RPGCharacterSheet()

    # Aplicar estilo personalizado
    app.aplicar_estilo_personalizado()

    # Título do aplicativo
    st.title('🌟 JoJo RPG - Character Sheet')
    st.markdown('<p style="text-align: center;">Criado com 💖 por dark</p>', unsafe_allow_html=True)

    # Criar interface da ficha
    app.criar_interface_ficha()

if __name__ == "__main__":
    main()
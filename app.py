import streamlit as st
from billboard import get_top_songs
from spotify import get_spotify_data

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Músicas mais ouvidas nos EUA",
    page_icon="🎧",
    layout="wide"
)

# =========================================================
# CSS GLOBAL (remove bugs visuais do Streamlit)
# =========================================================
st.markdown(
    """
    <style>
    /* Fundo uniforme (remove faixa superior diferente) */
    .stApp {
        background: linear-gradient(180deg, #061a1f 0%, #061a1f 100%);
        color: #eaeaea;
    }

    /* Remove header padrão e sombra */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    header[data-testid="stHeader"]::after {
        box-shadow: none;
    }

    /* Remove ícones automáticos (keyboard_arrow_*, anchors) */
    .stAnchorLink {
        display: none !important;
    }
    span.material-icons {
        display: none !important;
    }

    /* Links */
    a {
        color: #1db954 !important;
        text-decoration: none;
        font-weight: 500;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CABEÇALHO
# =========================================================
st.markdown("## 🎶 **Músicas mais ouvidas nos EUA**")
st.markdown(
    "Ranking baseado no **Billboard Hot 100**, com visual inspirado no Spotify. "
    "O Billboard publica rankings **semanais**; o sistema abstrai a seleção mensal "
    "para uma semana de referência válida."
)

# =========================================================
# SIDEBAR — FILTROS
# =========================================================
st.sidebar.markdown("## 📅 Período")

years = list(range(2026, 1957, -1))
months = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
]

year = st.sidebar.selectbox("Ano", years)
month = st.sidebar.selectbox("Mês", months)
month_number = months.index(month) + 1

buscar = st.sidebar.button("🔍 Buscar músicas")

# =========================================================
# PLACEHOLDER DE IMAGEM
# =========================================================
PLACEHOLDER_IMAGE = (
    "https://upload.wikimedia.org/wikipedia/commons/1/1b/Music_Icon.png"
)

# =========================================================
# CONTEÚDO PRINCIPAL
# =========================================================
if buscar:
    with st.spinner("Buscando ranking do Billboard..."):
        songs = get_top_songs(year, month_number)

    if not songs:
        st.warning("Nenhuma música encontrada para esse período.")
    else:
        st.markdown(f"## 🎧 **Top 100 — {month} de {year}**")
        st.markdown(
            "🟢 **Primeira semana válida do mês** "
            "_(o Billboard Hot 100 é publicado semanalmente)_"
        )

        cols = st.columns(2)

        for i, song_name in enumerate(songs):
            col = cols[i % 2]
            data = get_spotify_data(song_name)

            with col:
                # Sub-colunas para colocar imagem do lado do texto
                img_col, txt_col = st.columns([1, 2])
                
                with img_col:
                    if data['image']:
                        st.image(data['image'], width=180) # Tamanho reduzido
                    else:
                        st.image("https://via.placeholder.com/180x180.png?text=Sem+Capa", width=180)
                
                with txt_col:
                    st.markdown(f"### #{i + 1}")
                    st.write(f"**{song_name}**")
                    st.markdown(f"🟢 [Ouvir no Spotify]({data['link']})")
                
                st.write("") # Espaço extra
                st.markdown("---")

# =========================================================
# RODAPÉ
# =========================================================
st.markdown("---")
st.markdown(
    "<small>"
    "Projeto acadêmico • Python + Streamlit • "
    "Dados: Billboard Hot 100 • "
    "Capas: iTunes (fallback) • Links: Spotify"
    "</small>",
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
import plotly.express as px  # <-- A MÁGICA DOS GRÁFICOS

# 1. Configuração do Painel
st.set_page_config(page_title="Governança | Letramento Digital", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏛️ Dashboard de Governança: Letramento Digital</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Monitoramento de Verbas FUST, Políticas Públicas e Expansão Tecnológica</p>", unsafe_allow_html=True)
st.divider()

# 2. Estrutura Principal: As 3 Abas
tab1, tab2, tab3 = st.tabs(["👁️ 1. Fiscalização e Responsabilidade", "📊 2. Distribuição de Verbas", "🗺️ 3. Aplicação das Políticas (Mapa)"])

# ==========================================
# ABA 1: FISCALIZAÇÃO (Agora com Expansores)
# ==========================================
with tab1:
    st.header("Estrutura de Fiscalização e Gestão")
    st.markdown("Cadeia de responsabilidade legal para garantir a execução do letramento digital.")
    
    col1, col2, col3 = st.columns(3)
    col1.info("**🏢 Órgão Executor**\n\nSec. de Educação e Inovação.")
    col2.warning("**⚖️ Órgão Fiscalizador**\n\nTribunal de Contas (TCE) e Ministério Público.")
    col3.success("**👥 Controle Social**\n\nPortal da Transparência e Conselhos.")
    
    st.markdown("### 📋 Status do Ciclo de Auditoria")
    # Transformando a tabela simples em "Acordeões" (Expansores) profissionais
    with st.expander("✅ Ciclo 2023 - Infraestrutura de Rede (Aprovado)"):
        st.write("Auditoria focada na instalação de antenas. Parecer do TCE: Aprovado com ressalvas referentes à manutenção preventiva.")
    with st.expander("⏳ Ciclo 2024 - Letramento nas Escolas (Em Andamento)"):
        st.write("Foco na distribuição de tablets e capacitação de professores. O Ministério Público aguarda a documentação do segundo semestre.")
    with st.expander("📅 Ciclo 2025 - Inclusão 60+ (Fase de Planejamento)"):
        st.write("Fase de licitação para os cursos focados na terceira idade nos centros comunitários.")

# ==========================================
# ABA 2: VERBAS (Agora com Gráfico Interativo)
# ==========================================
with tab2:
    st.header("Mapeamento Financeiro e Orçamento")
    
    verba_recebida = 15000000
    verba_executada = 8500000
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Fundo Recebido (FUST)", "R$ 15,0 Milhões")
    c2.metric("Valor Executado", "R$ 8,5 Milhões", "56.6% de Execução", delta_color="normal")
    c3.metric("Saldo Remanescente", "R$ 6,5 Milhões", "- 43.4% a executar", delta_color="inverse")
    
    # ... (mantenha os st.metric que você já tem no topo da Aba 2) ...
    
    st.divider()
    
    # 1. Os Dados
    df_verbas = pd.DataFrame({
        "Política Pública": ["Internet nas Escolas", "Cidadão Digital", "Inclusão 60+", "Saldo Bloqueado"],
        "Verba (R$)": [4500000, 2500000, 1500000, 6500000]
    })
    
    # 2. Paleta de Cores Corporativa Escura (Azul Neon, Verde Menta, Amarelo e Cinza Escuro)
    cores_premium = ['#00BFFF', '#00FA9A', '#FFD700', '#2F4F4F']
    
    # 3. Criação do Gráfico Base
    fig = px.pie(
        df_verbas, 
        values="Verba (R$)", 
        names="Política Pública", 
        hole=0.65, # Buraco mais largo e elegante
        color_discrete_sequence=cores_premium
    )
    
    # 4. Refinando as fatias e o mouse hover (O "Verniz")
    fig.update_traces(
        textinfo='percent', 
        textposition='outside', # Joga os % para fora para não poluir as cores
        textfont_size=14,
        textfont_color="white",
        hovertemplate="<b>%{label}</b><br>Verba: R$ %{value:,.2f}<extra></extra>", # Limpa a caixinha do mouse
        marker=dict(line=dict(color='#0e1117', width=3)) # Cria uma borda escura entre as fatias
    )
    
    # 5. Ajuste fino de Layout (Legenda, Fundo e Centro)
    fig.update_layout(
        title=dict(text="Distribuição Estratégica", font=dict(size=22, color="white")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="h", # Legenda horizontal
            yanchor="bottom",
            y=-0.2, # Empurra lá para baixo
            xanchor="center",
            x=0.5,
            font=dict(color="lightgray", size=13),
            title=None # Remove a palavra "Política Pública" da legenda
        ),
        margin=dict(t=60, b=20, l=0, r=0), # Tira as margens excessivas
        annotations=[
            dict(text='<b>Total FUST</b><br>15 Milhões', x=0.5, y=0.5, font_size=16, showarrow=False, font_color="white")
        ] # Escreve no meio do Donut!
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# ABA 3: MAPA (Agora com Raios de Cobertura)
# ==========================================
with tab3:
    st.header("Distribuição Geográfica (Motor de IA)")
    st.markdown("Alocação inteligente dos novos Polos de Letramento com simulação de **raio de impacto (2km)**.")
    
    @st.cache_data
    def carregar_dados():
        df = pd.read_excel("dados.xlsx")
        def consertar_coord(coord, inicio):
            texto = str(coord).replace('.', '').replace(',', '').replace(' ', '')
            if texto.endswith('0'): texto = texto[:-1]
            if texto.startswith(inicio) and len(texto) > len(inicio):
                return float(texto[:len(inicio)] + '.' + texto[len(inicio):])
            try: return float(coord)
            except: return None
        df['lat'] = df['LATITUDE'].apply(lambda x: consertar_coord(x, '-8'))
        df['lon'] = df['LONGITUDE'].apply(lambda x: consertar_coord(x, '-34'))
        df = df.dropna(subset=['lat', 'lon', 'BAIRRO'])
        estimativa_ibge = {'BOA VIAGEM': 7500, 'PINA': 5200, 'IBURA': 1100, 'LINHA DO TIRO': 950, 'VÁRZEA': 2500}
        df['Renda_IBGE'] = df['BAIRRO'].str.strip().str.upper().map(estimativa_ibge).fillna(2000)
        return df

    df = carregar_dados()
    pesos = 1 / (df['Renda_IBGE'] + 1)
    ia = KMeans(n_clusters=12, random_state=42, n_init=10)
    ia.fit(df[['lat', 'lon']], sample_weight=pesos)
    coordenadas_ia = ia.cluster_centers_

    mapa = folium.Map(location=[-8.05, -34.90], zoom_start=12, tiles="CartoDB dark_matter")
    
    # Rede Antiga
    for _, linha in df.iterrows():
        folium.CircleMarker(location=[linha['lat'], linha['lon']], radius=1, color='#333333', fill=True).add_to(mapa)
    
    # Novos Polos com Raio de Ação
    for i, coord in enumerate(coordenadas_ia):
        # 1. Desenha o ícone do Livro (Polo)
        folium.Marker(
            location=[coord[0], coord[1]],
            icon=folium.Icon(color='green', icon='book', prefix='fa'),
            popup=f"Polo de Letramento #{i+1}"
        ).add_to(mapa)
        
        # 2. Desenha o Raio de Impacto Social (Bolinha translúcida ao redor)
        folium.Circle(
            location=[coord[0], coord[1]],
            radius=1800, # 1.8km de raio de influência do projeto
            color='#00FF00',
            fill=True,
            fill_opacity=0.15,
            weight=1
        ).add_to(mapa)

    st_folium(mapa, width="100%", height=500)
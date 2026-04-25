import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans

st.set_page_config(page_title="Conecta Recife | Otimizador IA", layout="wide", initial_sidebar_state="expanded")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📡 Dashboard Executivo: Conecta Recife</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Simulador de Alocação de Infraestrutura com IA e Dados do IBGE</p>", unsafe_allow_html=True)
st.divider()

with st.sidebar:
    st.header("⚙️ Parâmetros do Algoritmo")
    orcamento_antenas = st.slider("Selecione a Qtd. de Novas Antenas:", min_value=5, max_value=50, value=25)
    st.markdown("---")
    peso_social = st.checkbox("Ativar IA (Foco em Renda IBGE)", value=True)
    st.markdown("*Quando ativado, o algoritmo foca o investimento em áreas de vulnerabilidade social.*")

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

if peso_social:
    pesos = 1 / (df['Renda_IBGE'] + 1)
    kpi_foco = "Alta (Periferia)"
    kpi_cor = "normal"
else:
    pesos = None
    kpi_foco = "Cega (Centro)"
    kpi_cor = "inverse"

ia = KMeans(n_clusters=orcamento_antenas, random_state=42, n_init=10)
ia.fit(df[['lat', 'lon']], sample_weight=pesos)
coordenadas_ia = ia.cluster_centers_

custo_por_antena = 120000  
orcamento_total = (orcamento_antenas * custo_por_antena) / 1000000 

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rede Atual", f"{len(df)} pontos")
col2.metric("Expansão Física", f"+ {orcamento_antenas} polos")
col3.metric("Orçamento Necessário", f"R$ {orcamento_total:.1f} Milhões".replace('.', ','))
col4.metric("Precisão Social", kpi_foco, delta="Otimizado" if peso_social else "Desperdício", delta_color=kpi_cor)

mapa = folium.Map(location=[-8.05, -34.90], zoom_start=12, tiles="CartoDB dark_matter")

for _, linha in df.iterrows():
    folium.CircleMarker(
        location=[linha['lat'], linha['lon']], 
        radius=2, 
        color='#00BFFF', 
        fill=True,
        fill_opacity=0.7
    ).add_to(mapa)

for i, coord in enumerate(coordenadas_ia):
    folium.Marker(
        location=[coord[0], coord[1]],
        icon=folium.Icon(color='green' if peso_social else 'lightgray', icon='wifi', prefix='fa')
    ).add_to(mapa)

st_folium(mapa, width="100%", height=500)
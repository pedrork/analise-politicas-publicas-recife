import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import folium

print("Iniciando o Motor de Otimização...")

df = pd.read_excel("dados.xlsx")

# Limpa problemas de vírgula e transforma em número (a mesma faxina de antes)
df['Latitude'] = df['LATITUDE'].astype(str).str.replace(',', '.').astype(float, errors='ignore')
df['Longitude'] = df['LONGITUDE'].astype(str).str.replace(',', '.').astype(float, errors='ignore')
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
df = df.dropna(subset=['Latitude', 'Longitude', 'BAIRRO'])

estimativa_ibge = {
    'BOA VIAGEM': 7500,
    'PINA': 5200,
    'CASA FORTE': 8000,
    'DERBY': 4500,
    'SANTO AMARO': 1800,
    'CASA AMARELA': 2200,
    'VÁRZEA': 2500,
    'IBURA': 1100,
    'LINHA DO TIRO': 950,
    'NOVA DESCOBERTA': 1050,
    'COQUEIRAL': 900
}

df['Renda_IBGE'] = df['BAIRRO'].str.strip().str.upper().map(estimativa_ibge).fillna(2000)

df['Peso_Social'] = 1 / (df['Renda_IBGE'] + 1)

ORCAMENTO_NOVAS_ANTENAS = 15 

coordenadas = df[['Latitude', 'Longitude']]
pesos = df['Peso_Social']

ia = KMeans(n_clusters=ORCAMENTO_NOVAS_ANTENAS, random_state=42, n_init=10)
ia.fit(coordenadas, sample_weight=pesos)
novas_coordenadas = ia.cluster_centers_

mapa = folium.Map(location=[-8.05428, -34.8813], zoom_start=12)

for _, linha in df.iterrows():
    folium.CircleMarker(
        location=[linha['Latitude'], linha['Longitude']],
        radius=3, color='blue', fill=True,
        popup=f"{linha['BAIRRO']} (Atual)"
    ).add_to(mapa)

for i, coord in enumerate(novas_coordenadas):
    folium.Marker(
        location=[coord[0], coord[1]],
        icon=folium.Icon(color='green', icon='wifi', prefix='fa'),
        popup=f"Sugestão IA #{i+1} (Foco Social)"
    ).add_to(mapa)

mapa.save("prototipo_ia_recife.html")
print(f"✅ SUCESSO! A IA calculou {ORCAMENTO_NOVAS_ANTENAS} novos polos.")
print("🗺️ O mapa foi salvo como 'prototipo_ia_recife.html'. Abra na sua pasta!")
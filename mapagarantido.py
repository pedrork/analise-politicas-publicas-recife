import pandas as pd
import folium

print("⏳ Lendo a planilha do Excel...")
try:
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
    df_limpo = df.dropna(subset=['lat', 'lon'])

    print(f"✅ Dados limpos! Desenhando {len(df_limpo)} pontos no mapa...")

    mapa = folium.Map(location=[-8.05428, -34.8813], zoom_start=12)

    for _, linha in df_limpo.iterrows():
        bairro = linha['BAIRRO'] if 'BAIRRO' in df_limpo.columns else 'Ponto Conecta Recife'
        folium.CircleMarker(
            location=[linha['lat'], linha['lon']],
            radius=4,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            popup=bairro
        ).add_to(mapa)

    nome_arquivo = "MEU_MAPA_FUNCIONANDO.html"
    mapa.save(nome_arquivo)
    print(f"🎉 SUCESSO ABSOLUTO! O arquivo '{nome_arquivo}' foi criado na sua pasta.")
    print("👉 Vá na sua pasta e dê dois cliques nele para abrir no navegador!")

except Exception as e:
    print(f"🚨 Deu algum erro: {e}")
# analise-politicas-publicas-recife
Simulador de alocação inteligente de infraestrutura pública usando K-Medianas e dados do IBGE.

Este projeto é um Produto Mínimo Viável (MVP) desenvolvido para a disciplina/projeto de Consultoria em Tecnologia. O objetivo é otimizar a distribuição de infraestrutura pública (antenas de Wi-Fi) no Recife utilizando Inteligência Artificial e dados sociais.

## 🎯 O Problema
Atualmente, a infraestrutura tende a se concentrar em áreas centrais por inércia de mercado (Deserto Digital).

## 💡 A Solução
Utilizamos o algoritmo de clusterização **K-Medianas (Scikit-Learn)** ponderado por estimativas de renda do Censo do IBGE. O motor de IA atrai novos investimentos para as zonas de maior vulnerabilidade social.

## 🛠️ Tecnologias Utilizadas
* **Python** (Linguagem Core)
* **Pandas** (Limpeza e Estruturação de Dados)
* **Scikit-Learn** (Algoritmo de Inteligência Artificial)
* **Folium & Streamlit** (Criação do Dashboard Executivo e Mapas Interativos)

## 🚀 Como executar localmente
1. Clone este repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Rode o painel: `streamlit run geradordemapa.py`

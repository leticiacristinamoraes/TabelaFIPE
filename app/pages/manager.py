import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
from app.database.config import get_connection
from app.database.stores import get_stores, create_store, update_store, delete_store
from app.database.users import get_users, create_user, update_user, delete_user
from datetime import date
import plotly.express as px
from app.database.config import get_connection
from app.database.stores import get_stores, create_store, update_store, delete_store
from app.database.users import get_users, create_user, update_user, delete_user
from app.database.ranking_researchers import generate_research_graph, get_ranking_researchers_table

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.database.quotation_researcher import get_researcher_quotations
from app.database.quotation_consults import save_quotation_consult, get_quotation_consults

st.set_page_config(
    page_title="Gestor",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("👨‍💼 Pagina do Gestor")
st.write("Bem vindo à página, acesse a lista de pesquisadores, lojas e gerencie usuários")

if st.button("Voltar para a Home"):
   st.switch_page("main.py")

def listar_pesquisadores():
    """Busca pesquisadores cadastrados."""
    return [(user[0], user[1]) for user in get_users() if user[3] == 'pesquisador']

def painel_gestor():
    st.title("Painel do Gestor")

    aba_cadastro, aba_listagem, aba_pesquisadores, aba_relatorio = st.tabs(["Cadastrar Loja", "Listar Lojas", "Gerenciar Usuários", "Relatório de Cotações"])
    aba_cadastro, aba_listagem, aba_pesquisadores, aba_veiculos, aba_ranking, ranking_geral = st.tabs(["Cadastrar Loja", "Listar Lojas", "Gerenciar Usuários", "Gerenciar Veículos", "Ranking Top 10", "Ranking Geral"])

    with aba_cadastro:
        st.header("Cadastrar Nova Loja")
        nome = st.text_input("Nome da Loja")
        endereco = st.text_area("Endereço")
        cnpj = st.text_input("CNPJ")
        pesquisadores = listar_pesquisadores()
        pesquisador_opcoes = {p[1]: p[0] for p in pesquisadores}  
        pesquisador_escolhido = st.selectbox("Atribuir a um Pesquisador", ["Nenhum"] + list(pesquisador_opcoes.keys()))
        
        if st.button("Cadastrar Loja"):
            pesquisador_id = pesquisador_opcoes.get(pesquisador_escolhido) if pesquisador_escolhido != "Nenhum" else None
            create_store(nome, endereco, cnpj, pesquisador_id)
            st.success("Loja cadastrada com sucesso!")

    with aba_listagem:
        st.header("Lojas Cadastradas")
        lojas = get_stores()
        
        if not lojas:
            st.warning("Nenhuma loja cadastrada.")
        
        for loja in lojas:
            if len(loja) < 5:
                st.error(f"Erro ao acessar loja: {loja}")
                continue
            with st.expander(f"{loja[1]}"):
                novo_nome = st.text_input("Editar Nome", value=loja[1], key=f"nome_{loja[0]}")
                novo_endereco = st.text_area("Editar Endereço", value=loja[2], key=f"endereco_{loja[0]}")
                novo_cnpj = st.text_input("Editar CNPJ", value=loja[3], key=f"cnpj_{loja[0]}")
                index_pesquisador = 0  # "Nenhum" como padrão
                
                if loja[4] and loja[4] in pesquisador_opcoes.values():
                    pesquisador_nome = next((nome for nome, id in pesquisador_opcoes.items() if id == loja[4]), "Nenhum")
                    index_pesquisador = list(pesquisador_opcoes.keys()).index(pesquisador_nome) + 1
                
                novo_pesquisador = st.selectbox("Atribuir pesquisador", ["Nenhum"] + list(pesquisador_opcoes.keys()), index=index_pesquisador, key=f"pesquisador_{loja[0]}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Salvar Alterações", key=f"salvar_{loja[0]}"):
                        novo_pesquisador_id = pesquisador_opcoes.get(novo_pesquisador) if novo_pesquisador != "Nenhum" else None
                        update_store(loja[0], novo_nome, novo_endereco, novo_cnpj, novo_pesquisador_id)
                        st.success("Loja atualizada com sucesso!")
                with col2:
                    if st.button(f"Excluir Loja", key=f"excluir_{loja[0]}"):
                        delete_store(loja[0])
                        st.warning("Loja removida com sucesso!")

    with aba_pesquisadores:
        st.header("Gerenciar Usuários")
        aba_cadastrar, aba_listar = st.tabs(["Cadastrar Usuário", "Listar Usuários"])
        
        with aba_cadastrar:
            st.subheader("Cadastrar Novo Usuário")
            nome_usuario = st.text_input("Nome do Usuário")
            email_usuario = st.text_input("Email do Usuário")
            papel_usuario = st.selectbox("Papel", ["pesquisador", "gestor"])
            
            if st.button("Cadastrar Usuário"):
                create_user(nome_usuario, email_usuario, papel_usuario)
                st.success("Usuário cadastrado com sucesso!")
        
        with aba_listar:
            st.subheader("Usuários Cadastrados")
            usuarios = get_users()
            
            if usuarios:
                for i, usuario in enumerate(usuarios):
                    with st.expander(f"{usuario[1]} ({usuario[2]})"):  
                        novo_nome = st.text_input("Editar Nome", value=usuario[1], key=f"nome_{usuario[0]}_{i}")
                        novo_email = st.text_input("Editar Email", value=usuario[2], key=f"email_{usuario[0]}_{i}")
                        opcoes_papel = ["pesquisador", "gestor"]
                        index_papel = opcoes_papel.index(usuario[3]) if usuario[3] in opcoes_papel else 0  
                        novo_papel = st.selectbox("Editar Papel", opcoes_papel, index=index_papel, key=f"papel_{usuario[0]}_{i}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Salvar Alterações", key=f"salvar_usuario_{usuario[0]}_{i}"):
                                update_user(usuario[0], novo_nome, novo_email, novo_papel)  
                                st.success("Usuário atualizado com sucesso!")
                        with col2:
                            if st.button("Excluir Usuário", key=f"excluir_usuario_{usuario[0]}_{i}"):
                                delete_user(usuario[0])
                                st.warning("Usuário removido com sucesso!")
            else:
                st.warning("Nenhum usuário cadastrado.")
        
        with aba_relatorio:
            st.header("Relatório de Cotações por Pesquisador")
            sub_aba_consulta, sub_aba_minhas_consultas = st.tabs(["Cotações por Pesquisador", "Minhas Consultas"])
        
            with sub_aba_consulta:
                st.subheader("Consultar Cotações por Pesquisador")

                meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    start_month = st.selectbox("Mês Inicial", meses, index=0, key="start_month_consulta")
                with col2:
                    start_year = st.number_input("Ano Inicial", min_value=2000, max_value=2100, value=2024, step=1, key="start_year_consulta")
                with col3:
                    end_month = st.selectbox("Mês Final", meses, index=0, key="end_month_consulta")
                with col4:
                    end_year = st.number_input("Ano Final", min_value=2000, max_value=2100, value=2024, step=1, key="end_year_consulta")

                pesquisadores = listar_pesquisadores()  
                pesquisador_opcoes = ["Todos"] + [p[1] for p in pesquisadores]
                pesquisador_escolhido = st.selectbox("Selecionar Pesquisador", pesquisador_opcoes, key="pesquisador_consulta")

                if st.button("Consultar Cotações por Pesquisador"):
                    pesquisador_id = None if pesquisador_escolhido == "Todos" else next((p[0] for p in pesquisadores if p[1] == pesquisador_escolhido), None)

                    cotacoes = get_researcher_quotations(start_month, start_year, end_month, end_year, pesquisador_id)

                    if cotacoes:
                        

                        df = pd.DataFrame(cotacoes, columns=["Pesquisador", "Mês", "Total de Cotações"])
                        df["Mês"] = df["Mês"].str.strip()  

                        st.dataframe(df)
                    else:
                        st.warning("Nenhuma cotação encontrada para o período selecionado.")

                    save_quotation_consult(pesquisador_id, start_month, start_year, end_month, end_year)
                    st.success("Consulta salva com sucesso!")

            with sub_aba_minhas_consultas:
                st.subheader("Consultas Salvas por Pesquisador")

                pesquisador_id = None if pesquisador_escolhido == "Todos" else next((p[0] for p in pesquisadores if p[1] == pesquisador_escolhido), None)

                consultas = get_quotation_consults(pesquisador_id)

                if not consultas:
                    st.warning("Nenhuma consulta salva encontrada.")
                elif not isinstance(consultas, list):
                    st.error("Erro: O retorno não é uma lista de consultas.")
                else:
                    for idx, consulta in enumerate(consultas):

                        if not isinstance(consulta, dict):
                            st.error(f"Erro: Consulta {idx} não é um dicionário válido.")
                            continue

                        start_month = consulta.get("start_month", "Mês inválido")
                        end_month = consulta.get("end_month", "Mês inválido")
                        start_year = consulta.get("start_year", "Ano inválido")
                        end_year = consulta.get("end_year", "Ano inválido")
                        pesquisador_id = consulta.get("pesquisador_id", "Desconhecido")
                        quotations = consulta.get("quotations", [])

                        with st.expander(f"Consulta de {start_month} a {end_month} ({start_year} - {end_year})"):
                            st.write(f"**Pesquisador ID:** {pesquisador_id}")
                            st.write(f"Período inicial: {start_month} ({start_year})")
                            st.write(f"Período final: {end_month} ({end_year})")
                            
                            pesquisador_id = None if pesquisador_escolhido == "Todos" else next((p[0] for p in pesquisadores if p[1] == pesquisador_escolhido), None)

                            quotations = get_researcher_quotations(start_month, start_year, end_month, end_year, pesquisador_id)
                            
                            if quotations:
                                df = pd.DataFrame(quotations, columns=["Pesquisador", "Mês", "Total de Cotações"])
                                df["Mês"] = df["Mês"].str.strip()  


                                st.dataframe(df)
                            else:
                                st.warning("Nenhuma cotação encontrada para o período selecionado.")

    with aba_ranking:
        st.header("Top 10 Pesquisadores")

        # Input de Data Inicial e Final
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Selecione a Data Inicial", value=None)
        with col2:
            end_date = st.date_input("Selecione a Data Final", value=None, min_value=start_date if start_date else None)

        # Botão para gerar gráfico
        if st.button("Gerar Gráfico"):
            if not start_date or not end_date:
                st.warning("Por favor, selecione um intervalo de datas válido.")
            elif end_date < start_date:
                st.error("A Data Final não pode ser anterior à Data Inicial.")
            elif start_date and end_date:
                df = generate_research_graph(start_date, end_date)

                if df.empty:
                    st.warning("⚠️ Nenhum dado encontrado para o período selecionado.")
                else:
                    # Criar gráfico de barras verticais com Plotly
                    fig = px.bar(
                        df,
                        x="user_name", 
                        y="total_pesquisas", 
                        title="Top 10 Pesquisadores por Número de Pesquisas",
                        labels={"user_name": "Pesquisador", "total_pesquisas": "Total de Pesquisas"},
                        color="total_pesquisas",
                        color_continuous_scale="blues"
                    )

                    fig.update_layout(
                        xaxis_tickangle=-45,  # Inclina os rótulos do eixo X para melhor legibilidade
                        xaxis_title="Pesquisador",
                        yaxis_title="Total de Pesquisas"
                    )

                    # Exibir gráfico no Streamlit
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Por favor, selecione um intervalo de datas válido.")
    
    with ranking_geral:
        st.header("Ranking geral dos Pesquisadores")
        df = get_ranking_researchers_table()
    
        if df.empty:
            st.warning("Nenhum resultado encontrado.")
        else:
            st.dataframe(df)  # Exibe a tabela completa

if __name__ == "__main__":
    painel_gestor()
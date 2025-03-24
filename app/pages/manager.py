import streamlit as st
import pandas as pd
import sys

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from app.database.config import get_connection
from app.database.stores import get_stores, create_store, update_store, delete_store
from app.database.users import get_users, create_user, update_user, delete_user
from datetime import date
from app.database.config import get_connection
from app.database.prices import count_inputs_researcher, count_total
from app.database.stores import get_stores, create_store, update_store, delete_store
from app.database.users import get_users, create_user, update_user, delete_user
from app.database.ranking_researchers import generate_research_graph, get_ranking_researchers_table
from app.database.researcher_commission import insert_commission, commission_consult
from app.database.research_stats import get_research_data
from app.database.dezess import mostrar_top_10_grafico
#Modulo da feature P13. A função contém a UI da nova feature a ser implementada.
from app.lib.grafico_cotacoes_loja import component_cotacoes_loja

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

    aba_cadastro, aba_listagem, aba_pesquisadores, aba_metricas_pesquisadores, aba_gerenciar_pesquisadores, aba_relatorio, aba_ranking, ranking_geral, aba_grafico_loja, aba_Topdezmensal = st.tabs(["Cadastrar Loja", "Listar Lojas", "Gerenciar Usuários", "Gerenciar Pesquisadores", "Metricas dos Pesquisadores", "Relatório de Cotações","Ranking Top 10", "Ranking Geral"])

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

        with aba_gerenciar_pesquisadores:
            st.header("🔬 Gerenciar Pesquisadores")
            st.subheader("Consulta de Produção do Pesquisador")
        
            pesquisadores = listar_pesquisadores()
            pesquisadores_dict = {p[0]: p[1] for p in pesquisadores}
            pesquisador_id = st.selectbox("Selecione o Pesquisador", options=list(pesquisadores_dict.keys()), format_func=lambda x: pesquisadores_dict[x])
        
            col1, col2 = st.columns(2)
            with col1:
                ano_inicio = st.selectbox("Ano Inicial", options=list(range(2020, 2026)), index=3)
                mes_inicio = st.selectbox("Mês Inicial", options=list(range(1, 13)), index=0)
        
            with col2:
                ano_fim = st.selectbox("Ano Final", options=list(range(2020, 2026)), index=3)
                mes_fim = st.selectbox("Mês Final", options=list(range(1, 13)), index=11)
        
            df = pd.DataFrame(columns=["search_date", "search_count"])
        
            if st.button("📈 Gerar Relatório"):
                dados = get_research_data(pesquisador_id, ano_inicio, mes_inicio, ano_fim, mes_fim)
        
                if dados is not None and not dados.empty:
                    df = pd.DataFrame(dados, columns=["search_date", "search_count"])
                else:
                    df = pd.DataFrame(columns=["search_date", "search_count"])
        
            if df.empty:
                st.warning("⚠️ Nenhuma pesquisa encontrada para este período.")
            else:
                st.success("🔎 Resultados da Produção")
        
                col1, col2 = st.columns([1, 2])
        
                with col1:
                    st.write("📋 **Tabela de Produção**")
                    st.dataframe(df, height=300)
        
                with col2:
                    st.write("📈 **Gráfico de Produção**")
                    st.bar_chart(df.set_index("search_date"))
                 
        with aba_metricas_pesquisadores:
            st.header("Métricas dos pesquisadores")
            aba_cotacoes, aba_comissao = st.tabs(["Cotações", "Comissão"])

            with aba_cotacoes:
                st.header("Cotações")
                pesquisadores2 = listar_pesquisadores()
                pesquisador_opcoes2 = {p[1]: p[0] for p in pesquisadores2}  # {'nome': id}
                pesquisador_escolhido2 = st.selectbox("Pesquisador", ["Nome do pesquisador"] + list(pesquisador_opcoes2.keys()), key="nome_pesquisador")
                # Entrada de datas
                data_inicial = st.date_input("Data Inicial", key="data_inicial")
                data_final = st.date_input("Data Final", key="data_final")

                if st.button("Buscar", key="key_calcular_comissoes"):

                    # Verificando se o nome digitado é válido apenas quando o botão for pressionado
                    if pesquisador_escolhido2 not in pesquisador_opcoes2:
                        st.error("Nome do pesquisador inválido! Por favor, selecione um pesquisador da lista.")
                        st.stop()

                    pesquisador_id2 = pesquisador_opcoes2[pesquisador_escolhido2]

                    try:
                        # Convertendo para string no formato correto
                        data_inicial_str = data_inicial.strftime("%Y-%m-%d")
                        data_final_str = data_final.strftime("%Y-%m-%d")

                        # Validando se a data final é menor que a data inicial
                        if data_final < data_inicial:
                            st.error("A Data Final não pode ser anterior à Data Inicial.")
                            st.stop()
                    except Exception as e:
                        st.error(f"Erro ao processar as datas")
                        st.stop()

                    # Buscar e exibir os dados
                    tabela = count_inputs_researcher(pesquisador_id2, data_inicial_str, data_final_str)
                    df = pd.DataFrame(tabela, columns=['Data', 'Quantidade'])
                    total = count_total(pesquisador_id2, data_inicial_str, data_final_str)
                    st.write((f"Total:{total[0][0]}"))
                    st.bar_chart(df.set_index('Data'))

                # if pesquisador_escolhido2 not in pesquisador_opcoes2:
                #     st.error("Nome do pesquisador inválido! Por favor, selecione um pesquisador da lista.")
                #     st.stop()
                # pesquisador_id2 = pesquisador_opcoes2.get(pesquisador_escolhido2) if pesquisador_escolhido2 != "Nenhum" else None
                # # Entrada de datas
                # data_inicial = st.date_input("Data Inicial", key="data_inicial")
                # data_final = st.date_input("Data Final", key="data_final")

                # try:
                #     # Convertendo para string no formato correto
                #     data_inicial_str = data_inicial.strftime("%Y-%m-%d")
                #     data_final_str = data_final.strftime("%Y-%m-%d")

                #     # Validando se a data final é menor que a data inicial
                #     if data_final < data_inicial:
                #         st.error("A Data Final não pode ser anterior à Data Inicial.")
                #         st.stop()
                # except Exception as e:
                #     st.error(f"Erro ao processar as datas: {e}")
                #     st.stop()

                
                # if st.button("Buscar", key="key_calcular_comissoes"):
                #     tabela = count_inputs_researcher(pesquisador_id2, data_inicial, data_final)
                #     df = pd.DataFrame(tabela, columns=['Data', 'Quantidade'])
                #     # fig, ax = plt.subplots(figsize=(8,6))
                #     # df.plot(x='Data', y='Quantidade', kind='bar',ax=ax)
                #     # ax.set_frame_on(False)
                #     # #adicionando um título
                #     # ax.set_title(f"Quantidade de cotações no mês do(a) pesquisador(a) {pesquisador_escolhido2}",loc='left',pad=30,fontdict={'fontsize':20},color='#3f3f4e')
                #     # st.pyplot(fig)
                #     st.bar_chart(df.set_index('Data'))
        
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


        #Aba nova da feature P13. Ela chama a função onde pode ser realizado a consulta.
        with aba_grafico_loja:
            component_cotacoes_loja()

            
      with aba_Topdezmensal:           
        
        mostrar_top_10_grafico()
            with aba_comissao:
                st.header("Comissões")
                aba_listar_comissao, aba_calcular_comissao = st.tabs(["Listar comissões", "Calcular comissão"])

                with aba_listar_comissao:
                    st.header("Consulta de comissões")                   
                    mes = st.selectbox("Mês", [1,2,3,4,5,6,7,8,9,10,11,12], key="mes_comissao_listar")
                    ano = st.selectbox("Mês", [2024,2025], key="ano_comissao_listar")
                        
                    if st.button("Buscar", key="key_listar _comicoes"):
                        comissoes = commission_consult(mes,ano)
                        st.write(comissoes)

                with aba_calcular_comissao:
                    st.header("Calculo de comissões")  
                    mes = st.selectbox("Mês", [1,2,3,4,5,6,7,8,9,10,11,12], key="mes_comissao_calcular")
                    ano = st.selectbox("Mês", [2024,2025], key="ano_comissao_calcular")
                    
                    if st.button("Calcular", key="key_calcular _comissoes"):
                        comissoes = insert_commission(mes,ano)
                        st.success(comissoes)       
            
if __name__ == "__main__":
    painel_gestor()

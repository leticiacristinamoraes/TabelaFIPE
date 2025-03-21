import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
from database.stores import get_stores, create_store, update_store, delete_store
from database.users import get_users, create_user, update_user, delete_user
from database.vehicles import get_vehicles, create_vehicle, update_vehicle, delete_vehicle
from database.research_stats import get_research_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(
    page_title="Gestor",
    page_icon="👨‍🎼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("👨‍🎼 Pagina do Gestor")
st.write("Bem vindo à página, acesse a lista de pesquisadores, lojas e gerencie usuários")

def listar_pesquisadores():
    return [(user[0], user[1]) for user in get_users() if user[3] == 'pesquisador']

def painel_gestor():
    aba_loja, aba_listar, aba_usuarios, aba_veiculos, aba_pesquisadores = st.tabs([
        "Cadastrar Loja", "Listar Lojas", "Gerenciar Usuários", "Gerenciar Veículos", "Gerenciar Pesquisadores"])

    with aba_loja:
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

    with aba_listar:
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
                pesquisadores = listar_pesquisadores()
                pesquisador_opcoes = {p[1]: p[0] for p in pesquisadores}
                index_pesquisador = 0
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

    with aba_usuarios:
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
                        novo_papel = st.selectbox("Editar Papel", ["pesquisador", "gestor"], key=f"papel_{usuario[0]}_{i}")

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

    with aba_veiculos:
        st.header("Gerenciar Veículos")
        veiculos = get_vehicles()
        for i, veiculo in enumerate(veiculos):
            with st.expander(f"{veiculo[1]} - {veiculo[2]}"):
                novo_modelo = st.text_input("Editar Modelo", value=veiculo[1], key=f"modelo_veiculo_{veiculo[0]}_{i}")
                novo_ano = st.number_input("Editar Ano", value=veiculo[2], min_value=1900, max_value=2050, key=f"ano_veiculo_{veiculo[0]}_{i}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Salvar Alterações", key=f"salvar_veiculo_{veiculo[0]}_{i}"):
                        update_vehicle(veiculo[0], novo_modelo, novo_ano)
                        st.success("Veículo atualizado com sucesso!")
                with col2:
                    if st.button("Excluir Veículo", key=f"excluir_veiculo_{veiculo[0]}_{i}"):
                        delete_vehicle(veiculo[0])
                        st.warning("Veículo removido com sucesso!")

    with aba_pesquisadores:
        st.header("🔬 Gerenciar Pesquisadores")
        st.subheader("Consulta de Produção do Pesquisador")

        pesquisadores = [(p[0], p[1]) for p in get_users() if p[3] == "pesquisador"]
        pesquisadores_dict = {p[0]: p[1] for p in pesquisadores}

        if pesquisadores:
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
        else:
            st.info("Nenhum pesquisador encontrado.")

if __name__ == "__main__":
    painel_gestor()

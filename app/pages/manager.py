import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.config import get_connection
from database.stores import get_stores, create_store, update_store, delete_store
from database.users import get_users, create_user, update_user, delete_user
from database.prices import count_inputs_researcher, count_total
from database.researcher_commission import insert_commission, commission_consult


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

def listar_pesquisadores():
    """Busca pesquisadores cadastrados."""
    return [(user[0], user[1]) for user in get_users() if user[3] == 'pesquisador']

def painel_gestor():
    st.title("Painel do Gestor")
    aba_cadastro, aba_listagem, aba_pesquisadores, aba_veiculos, aba_metricas_pesquisadores = st.tabs(["Cadastrar Loja", "Listar Lojas", "Gerenciar Usuários", "Gerenciar Veículos","Metricas dos Pesquisadores"])

    with aba_cadastro:
        st.header("Cadastrar Nova Loja")
        nome = st.text_input("Nome da Loja")
        endereco = st.text_area("Endereço")
        cnpj = st.text_input("CNPJ")
        pesquisadores = listar_pesquisadores()
        pesquisador_opcoes = {p[1]: p[0] for p in pesquisadores}  # {'nome': id}
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
                    with st.expander(f"{usuario[1]} ({usuario[2]})"):  # Exibir nome e e-mail no título
                        novo_nome = st.text_input("Editar Nome", value=usuario[1], key=f"nome_{usuario[0]}_{i}")
                        novo_email = st.text_input("Editar Email", value=usuario[2], key=f"email_{usuario[0]}_{i}")
                        opcoes_papel = ["pesquisador", "gestor"]
                        index_papel = opcoes_papel.index(usuario[3]) if usuario[3] in opcoes_papel else 0  
                        novo_papel = st.selectbox("Editar Papel", opcoes_papel, index=index_papel, key=f"papel_{usuario[0]}_{i}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Salvar Alterações", key=f"salvar_usuario_{usuario[0]}_{i}"):
                                update_user(usuario[0], novo_nome, novo_email, novo_papel)  # Atualizar com nome, email e papel
                                st.success("Usuário atualizado com sucesso!")
                        with col2:
                            if st.button("Excluir Usuário", key=f"excluir_usuario_{usuario[0]}_{i}"):
                                delete_user(usuario[0])
                                st.warning("Usuário removido com sucesso!")
            else:
                st.warning("Nenhum usuário cadastrado.")
        
        with aba_veiculos:
            st.header("Gerenciar Veículos")
            st.write("Em construção...")
#                   >>>>>>>>>>> Funcionalidade P12/1 <<<<<<<<<<<<
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

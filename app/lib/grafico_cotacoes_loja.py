import datetime
import streamlit as st
import pandas as pd

from database.stores import get_stores
from database.prices import get_cotations_count_by_time

'''Arquivo da UI da feature P13.'''

#Usado para realizar a consulta da cotação em um periodo dado.
#Chama a função que retorna o numero de cotações com seus meses e anos.
def get_cotations_list(store_id,date_start, date_final):
    cotations_list = get_cotations_count_by_time(store_id,date_start,date_final)
    return cotations_list

def component_cotacoes_loja():
    chart_data=None

    st.header("Cotações por loja")
    left, right = st.columns(2)
    with left:
        #pega todas as lojas disponíveis.
        stores = get_stores()
        stores_options = {s[1]: s[0] for s in stores}  # {'nome': id}

        #Cria um select box para loja e retorna a loja selecionada pelo usuario.
        selected_store = st.selectbox("Selecionar loja para a pesquisa", ["Nenhum"] + list(stores_options.keys()), key='stores_options')

        #Cria um input box para data inicial e data final para consulta.
        date_inicial_str = st.date_input("Data inicial da pesquisa", value=None,key='data-inicial')
        date_final_str = st.date_input("Data final da pesquisa", value=None, key='data-final')

        #Cria o botão usado para realizar a consulta.
        if st.button("Pesquisar cotações", key="button-cotacoes"):
            if selected_store == "Nenhum":
                st.warning("Loja não selecionada ou inexistente.")
            elif date_final_str< date_inicial_str:
                st.warning("data final é maior que a inicial. Escolha novamente.")
            else:
                cotation_list = get_cotations_list(stores_options[selected_store], date_inicial_str,date_final_str)
                cotation_dict = {'ano_mes':[year_month for year_month in cotation_list.keys()],
                                'cotacao_total':[int(cotacao) for cotacao in cotation_list.values()]}

                chart_data = pd.DataFrame(cotation_dict)
                chart_data = chart_data.set_index('ano_mes')
        with right:
            st.write(f"Tabela de cotações por mês da loja {selected_store}")
            st.dataframe(chart_data)
            st.write(f"Gráfico cotações por mês da loja {selected_store}")
            st.bar_chart(chart_data, x_label="ano/mês", y_label="Cotação total do ano/mês")
        
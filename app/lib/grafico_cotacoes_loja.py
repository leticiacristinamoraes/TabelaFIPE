import datetime
import streamlit as st
import pandas as pd

from database.stores import get_stores
from database.prices import get_cotations_by_time



def get_prices_by_store_id(store_id):
    pass
def get_cotations_list(store_id,date_start, date_final):
    cotations_list = get_cotations_by_time(store_id,date_start,date_final)
    return cotations_list
def component_cotacoes_loja():
    st.header("COtações por loja")
    st.write("em construção....")
    stores = get_stores()
    stores_options = {s[1]: s[0] for s in stores}  # {'nome': id}
    selected_store = st.selectbox("Selecionar loja para a pesquisa", ["Nenhum"] + list(stores_options.keys()), key='stores_options')

    date_inicial_str = st.date_input("Data inicial da pesquisa", value=None,key='data-inicial')
    date_final_str = st.date_input("Data final da pesquisa", value=None, key='data-final')

    if st.button("Pesquisar cotações", key="button-cotacoes"):
        cotation_list = get_cotations_by_time(stores_options[selected_store], date_inicial_str,date_final_str)
        stores_options = {int(s[2]): int(s[0]) for s in cotation_list}
        chart_data = pd.DataFrame.from_dict(stores_options, orient='index')
        st.line_chart(chart_data, x_label="data", y_label="cotação")
        
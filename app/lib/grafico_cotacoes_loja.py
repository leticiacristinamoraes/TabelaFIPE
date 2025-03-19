import datetime
import streamlit as st
import pandas as pd

from database.stores import get_stores
from database.avg_price_store import get_cotation_by_data



def get_prices_by_store_id(store_id):
    pass
def get_cotations_list(store_id,date_start, date_final):
    cotations_list = get_cotation_by_data(store_id,date_start,date_final)
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
        cotation_list = get_cotations_list(stores_options[selected_store], date_inicial_str,date_final_str)
        cotation_dict = {'data':[datetime.datetime(p.year,p.month,1) for p in cotation_list.keys()],
                         'total':[int(p) for p in cotation_list.values()]}
        print(cotation_dict)
        chart_data = pd.DataFrame(cotation_dict)
        chart_data['data'] = pd.to_datetime(chart_data['data'],  format="%Y-%m")
        
        chart_data.set_index('data', inplace=True)
        config = {
            "_index": st.column_config.DateColumn("Month", format="MMM YYYY"),
            "Total": st.column_config.NumberColumn("Total ($)"),
        }

        st.dataframe(chart_data, column_config=config)
        monthly = chart_data['total'].resample('ME').mean()
        
        st.line_chart(monthly)
        
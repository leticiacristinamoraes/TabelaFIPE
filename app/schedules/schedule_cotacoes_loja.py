'''Arquivo de implementação da tarefa agendada para calculo da cotação mensal de todas as lojas'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
import time
import streamlit as st
import pandas as pd
import calendar
from database.stores import get_stores
from database.month_cotation_store import calculate_month_cotation_store, create_cotation_store, get_cotation_by_data, get_cotations_count_by_month


# Pega as cotações referente ao mês na tabela "prices"
def get_cotations_list(store_id:int,date_start:datetime.date, date_final:datetime.date):
    cotations_list = get_cotations_count_by_month(store_id,date_start,date_final)
    return cotations_list
# Pega o retorno do calculo de cotações referente ao mês atual
def get_calculate_month_cotation_store(total, value_multiplier):
    result = calculate_month_cotation_store(total, value_multiplier)
    return result

# Chama a função que irá inserir a cotação da loja na tabela month_cotation_store
def get_create_cotation_store(store_id, new_total, new_date):
    result = create_cotation_store(store_id=store_id, new_total=new_total,date=new_date)
    return result

# Função que irá pegar todas as lojas e realizar as outras chamadas para o calculo e armazenamento
def task_cotacoes_loja(new_date_start: datetime.date,new_date_final:datetime.date):
    all_stores = get_stores()

    for store in all_stores:
        count_total_year_month = get_cotations_list(store[0], new_date_start, new_date_final)
        if count_total_year_month is not None:
            new_calculate = get_calculate_month_cotation_store(count_total_year_month['total'],1)
            ids = get_create_cotation_store(store_id=store[0], new_total=new_calculate, new_date=new_date_final)
    return "tarefa realizada com sucesso"

# Função que é chamada quando o arquivo é chamado pela tarefa agendada. Ela pega o mês atual.
def start_task_cotacoes_loja():
    date_now = datetime.datetime.now()
    _, last_day = calendar.monthrange(date_now.year, date_now.month)
    
    result = task_cotacoes_loja(new_date_start=datetime.date(date_now.year,date_now.month,1), 
                                new_date_final=datetime.date(date_now.year,date_now.month,last_day))
    
    if result is not None:
        return result
    return None

    
if __name__=='__main__':
    result = start_task_cotacoes_loja()
    
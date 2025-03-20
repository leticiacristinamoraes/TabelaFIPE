import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
import time
import streamlit as st
import pandas as pd
import calendar
from database.stores import get_stores
from database.avg_price_store import calculate_month_price_store, create_price_store, get_cotation_by_data, get_cotations_count_by_month


def get_cotations_list(store_id:int,date_start:datetime.date, date_final:datetime.date):
    cotations_list = get_cotations_count_by_month(store_id,date_start,date_final)
    return cotations_list

def get_calculate_month_price_store(total, value_multiplier):
    result = calculate_month_price_store(total, value_multiplier)
    return result

def get_create_price_store(store_id, new_total, new_date):
    result = create_price_store(store_id=store_id, new_total=new_total,date=new_date)
    return result

def task_cotacoes_loja(new_date_start: datetime.date,new_date_final:datetime.date):
    all_stores = get_stores()

    for store in all_stores:
        count_total_year_month = get_cotations_list(store[0], new_date_start, new_date_final)
        if count_total_year_month is not None:
            new_calculate = get_calculate_month_price_store(count_total_year_month['total'],1)
            print(new_calculate)
            ids = get_create_price_store(store_id=store[0], new_total=new_calculate, new_date=new_date_final)
    return "tarefa realizada com sucesso"

def start_task_cotacoes_loja():
    date_now = datetime.date(2025,1,1)
    _, last_day = calendar.monthrange(date_now.year, date_now.month)
    
    result = task_cotacoes_loja(new_date_start=datetime.date(date_now.year,date_now.month,1), new_date_final=datetime.date(date_now.year,date_now.month,last_day))
    if result is not None:
        return result
    return None

    

    
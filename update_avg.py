import streamlit as st
import schedule
import time
import threading
from db.repositories.avg_price_repo import AvgPricePostgresqlRepository



# Função para atualizar os preços
def atualizar_precos():
    repo = AvgPricePostgresqlRepository()
    repo.calculate_and_store_avg_prices()
    print("Preços médios atualizados.")

# Função para rodar o agendador
def rodar_agendador():
    """Executa o agendador em loop para verificar tarefas pendentes."""
    schedule.every().day.at("03:00").do(atualizar_precos)  # Define a tarefa para 03:00 AM

    while True:
        schedule.run_pending()
        time.sleep(60)  # Espera 60 segundos antes de verificar novamente


# Garantir que o agendador só seja iniciado uma vez
if "agendador_iniciado" not in st.session_state:
    st.session_state["agendador_iniciado"] = True  # Marca como iniciado
    thread = threading.Thread(target=rodar_agendador, daemon=True)
    thread.start()



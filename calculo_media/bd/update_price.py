#atualização automática

#TabelaFIPE-base/db/scripts/update_avg_price.py

import schedule
import time
from db.repositories.avg_price_repo import AvgPricePostgresqlRepository

repo = AvgPricePostgresqlRepository()

def atualizar_precos():
    print("Calculando médias de preços...")
    repo.calculate_and_store_avg_prices()
    print("Preços médios atualizados.")

# Rodar diariamente às 2h da manhã
schedule.every().day.at("02:00").do(atualizar_precos)

while True:
    schedule.run_pending()
    time.sleep(60)

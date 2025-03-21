import datetime
import time
import unittest
import sys
import os

import emoji
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.stores import get_stores
from database.month_cotation_store import (
    create_month_cotation_store_table,
    calculate_month_cotation_store, 
    create_cotation_store, 
    get_cotations_count_by_month,
    drop_cotation_store
    )
from schedules.schedule_cotacoes_loja import task_cotacoes_loja, start_task_cotacoes_loja



'''
schedules teste envolve as funções da pagina schedule_cotation_store.py
funções a serem testadas:
'''
class TestScheduleTaskMonthCotation(unittest.TestCase):

    def setUp(self):
        create_month_cotation_store_table()
        self.store_id = 1
        self.date_start = datetime.date(2024,8,1)
        self.date_final = datetime.date(2024,8,31)

        self.new_total= None
        self.value_multiplier = 1
        return super().setUp()
    
    def test_0_get_all_stores(self):
        print("Pegando todas as lojas...")
        time.sleep(20)
        result_stores = get_stores()
        
        self.assertIsNotNone(result_stores)
        time.sleep(1)
        print("resultado do teste: " + result_stores)
        print(f"Teste: Get_all_Stores: CONCLUIDO. ")


    def test_1_get_cotations_count_by_month(self):
        print("Criando uma cotação da tabela 'prices'...")
        print(f"valores inseridos loja: {self.store_id}, data inicial: {self.date_start}, data final: {self.date_final}")
        print("resultado esperado {'total': 18, 'year': 2024, 'month': 8}...")

        result_cotations_month = get_cotations_count_by_month(store_id=self.store_id, 
                                                              date_start=self.date_start,
                                                              date_final=self.date_final)
        time.sleep(2)
        self.assertDictEqual(result_cotations_month, {'total': 18, 'year': 2024, 'month': 8})
        print("resultado do teste: " + result_cotations_month)
        self.new_total=result_cotations_month['total']
        print(self.new_total)
        print(f"get_cotations_count_by_month: CONCLUIDO. \n")

    def test_2_calculate_month_cotation_store(self):
        print("Calculando uma cotacao com valor fixo R$1 por cotacao...")
        print(f"valores inseridos cotacao: {self.new_total}")
        print("resultado esperado 18...")
        result_calculate = calculate_month_cotation_store(prices=18,
                                                          value_multiplier=self.value_multiplier)
        
        self.assertEqual(first=result_calculate,second=18)
       
        self.new_total = result_calculate
        time.sleep(2)
        print(self.new_total)
        print("resultado do teste: " + self.new_total)
        print(f"create_calculate_motn_cotation_store: CONCLUIDO. \n")
    def test_3_create_cotation_store(self):
        result_created = create_cotation_store(store_id=self.store_id,
                                               new_total=18,
                                               date=self.date_final)
        
        self.assertIsNotNone(result_created)
        time.sleep(2)
        print("resultado do teste: " + result_created)
        print(f"create_cotation_store: CONCLUIDO. \n")

    def test_4_task_cotacoes_loja(self):
        print("teste para saber se a função de agendamento está sendo efetiva")
        print(f"valores inseridos loja: {self.store_id}, data inicial: 2025/02/01, data final: 2025/02/28")
        print("resultado esperado 'tarefa realizada com sucesso'")
        result_task_confirm = task_cotacoes_loja(new_date_start=datetime.date(2025,2,1), 
                                                 new_date_final=datetime.date(2025,2,28))
        
        self.assertEqual(first=result_task_confirm,second="tarefa realizada com sucesso")
        time.sleep(2)
        print(result_task_confirm)
        
        print(f"task_cotacoes_loja: CONCLUIDO. \n")

    def test_5_start_task_cotacoes_loja(self):
        print("A tarefa agendada funcionando de fato. com datas referentes ao mês atual. ")
        print(f"valores inseridos loja: todas as lojas, data inicial: 2025/03/01, data final: 2025/03/31")
        result_task_confirm = start_task_cotacoes_loja()
        
        self.assertEqual(first=result_task_confirm,second="tarefa realizada com sucesso")
        
        print("resultado do teste: " + result_task_confirm)
        print(f"task_cotacoes_loja: CONCLUIDO. \n")
        time.sleep(10)

def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__': 
    with open('testing.out', 'w') as f: 
        main(f) 
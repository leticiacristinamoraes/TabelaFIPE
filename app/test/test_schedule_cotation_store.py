import datetime
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.stores import get_stores
from database.month_cotation_store import (
    create_month_cotation_store_table,
    calculate_month_cotation_store, 
    create_cotation_store, 
    get_cotations_count_by_month,
    drop_cotation_store
    )
from schedules.schedule_cotacoes_loja import task_cotacoes_loja



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
        result_stores = get_stores()

        self.assertIsNotNone(result_stores)
        print(result_stores)

    def test_1_get_cotations_count_by_month(self):
        result_cotations_month = get_cotations_count_by_month(store_id=self.store_id, 
                                                              date_start=self.date_start,
                                                              date_final=self.date_final)
        
        self.assertDictEqual(result_cotations_month, {'total': 18, 'year': 2024, 'month': 8})
        print(result_cotations_month)
        self.new_total=result_cotations_month['total']
        print(self.new_total)

    def test_2_calculate_month_cotation_store(self):
        result_calculate = calculate_month_cotation_store(prices=18,
                                                          value_multiplier=self.value_multiplier)
        
        self.assertEqual(first=result_calculate,second=18)
       
        self.new_total = result_calculate
        print(self.new_total)
        
    def test_3_create_cotation_store(self):
        result_created = create_cotation_store(store_id=self.store_id,
                                               new_total=18,
                                               date=self.date_final)
        
        self.assertIsNotNone(result_created)
        print(result_created)

    def test_4_task_cotacoes_loja(self):
        result_task_confirm = task_cotacoes_loja(new_date_start=datetime.date(2024,9,1), 
                                                 new_date_final=datetime.date(2024,9,30))
        
        self.assertEqual(first=result_task_confirm,second="tarefa realizada com sucesso")
        print(result_task_confirm)


def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__': 
    with open('testing.out', 'w') as f: 
        main(f) 
import datetime
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.month_cotation_store import (
    create_cotations_store_table, 
    create_cotation_store,
    drop_cotation_store, 
    update_cotation_store,
    calculate_month_cotation_store,
    update_month_cotation_store,
    get_cotation_count_by_month,
    get_cotation_by_data

    )
from database.stores import get_stores
import schedules



class TestcotationStore(unittest.TestCase):

    def test_0_create_cotation_store_success(self):
        create_cotations_store_table()
    
    def test_1_populate_cotation_store_error(self):
        #função ainda não existe
        store_id=1
        new_total=200
        date=datetime.date(2025, 2, 1)
        result = create_cotation_store(store_id=store_id, 
                                    new_total=new_total, 
                                    date=date)
        self.assertIsNone(result)
        print('resultado da adição de item na tabela month_cotation_store: '+result)

    def test_2_populate_cotation_store_success(self):
        #função existente
        result = create_cotation_store(store_id=1, new_total=200, date=datetime.date(2024,8,31))
        self.assertIsNotNone(result)
        print('resultado da adição de item na tabela month_cotation_store: '+result)

    def test_3_get_cotation_store_by_data_using_one_month_error(self):
        #função ainda não existe, deve retornar erro.
        store_id=1
        date_start=datetime.date(2024, 8, 1)
        date_final=datetime.date(2024, 8, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)

    def test_4_get_cotation_store_by_data_using_one_month_success(self):
        #Valor existe na tabela, deve ser retornado dict com {total,ano, mês}
        store_id=1
        date_start=datetime.date(2024, 8, 1)
        date_final=datetime.date(2024, 8, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)

        self.assertDictEqual(cotations_by_time, {'total': 200, 'year': 2024, 'month': 8})
        print(cotations_by_time)

    def test_5_get_cotation_store_by_data_using_one_month_None(self):
        #valor não existe na tabela, deve retornar nulo.
        store_id=1
        date_start=datetime.date(2023, 2, 1)
        date_final=datetime.date(2023, 2, 28)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)

    def test_6_get_cotation_store_by_data_different_months_success(self):
        #valores com mes inicial diferente do mes final, deve retornar os dados em dict.
        store_id=1
        date_start=datetime.date(2025, 1, 1)
        date_final=datetime.date(2025, 3, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNotNone(cotations_by_time)
        print(cotations_by_time)
        cotation_dict = {'data':[p for p in cotations_by_time.keys()],
                         'total':[int(p) for p in cotations_by_time.values()]}
        self.assertDictEqual()

    def test_7_get_cotation_store_by_data_one_month_exist_and_the_other_not(self):
        #valores com mes inicial diferente do mes final, mas um mês existe na tabela o outro não.
        #deve retornar os dados em dict.
        store_id=1
        date_start=datetime.date(2025, 3, 1)
        date_final=datetime.date(2025, 4, 30)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNotNone(cotations_by_time)
        print(cotations_by_time)
        cotation_dict = {'data':[p for p in cotations_by_time.keys()],
                         'total':[int(p) for p in cotations_by_time.values()]}
        self.assertDictEqual()

    def test_8_get_cotation_store_by_data_with_date_final_before_than_date_start(self):
        #valores com o mes final sendo anterior ao do inicio, deve retornar error.
        store_id=1
        date_start=datetime.date(2025, 3, 31)
        date_final=datetime.date(2025, 1, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)

    def test_9_get_cotation_store_by_data_with_store_not_existing(self):
        #Loja não está na tabela cotation_store, deve retornar None
        store_id=6
        date_start=datetime.date(2025, 3, 31)
        date_final=datetime.date(2025, 3, 1)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)
    '''
    def test_1_task_cotacoes_loja(self):
        result = schedules.start_task_cotacoes_loja()
        self.assertIsNotNone(result)
        pass
    '''      
        
       
        
def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__': 
    with open('testing.out', 'w') as f: 
        main(f) 
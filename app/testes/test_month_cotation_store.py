import datetime
import time
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.month_cotation_store import (
    create_month_cotation_store_table, 
    create_cotation_store,
    drop_cotation_store,
    get_cotation_by_data

    )
from database.stores import get_stores
import schedules



class TestcotationStore(unittest.TestCase):

    def test_0_create_cotation_store_success(self):
        
        print("teste 0")
        print("resultado esperado é a tabela criada")
        time.sleep(2)
        print("resultado esperado 'tarefa realizada com sucesso'")
        create_month_cotation_store_table()


    #Adiciona dados a tabela cotation store
    def test_1_populate_cotation_store_success(self):
        print(f"teste 1")
        print(f"valores inseridos loja: store_id:1, new_total: 18, data: 2025/08/31")
        print("resultado esperado 'tarefa realizada com sucesso'")
        time.sleep(2)
        result = create_cotation_store(store_id=1, new_total=18, date=datetime.date(2025,8,31))
        print(result)
        self.assertIsNotNone(result)

        print('resultado da adição de item na tabela month_cotation_store: '+result)
        print(f"create_cotation_store: CONCLUIDO. \n")

    def test_2_populate_cotation_store_error(self):
        print(f"teste 2")
        print(f"valores inseridos loja: store_id:1, new_total: 200, data: 2025/08/31")
        print("resultado esperado 'tarefa não realizada pois já há no banco essa id com essa data.")
        time.sleep(2)
        store_id=1
        new_total=200
        date=datetime.date(2025, 8, 31)
        result = create_cotation_store(store_id=store_id, 
                                    new_total=new_total, 
                                    date=date)
        print(result)
        if self.assertIsNone(result) is None:
            print('Resultado atingido')
        else:
            print('Resultado incorreto')
        print(f"create_cotation_store: CONCLUIDO. \n")

    #Valor existe na tabela, deve ser retornado dict com {total,ano, mês}
    def test_4_get_cotation_store_by_data_using_one_month_success(self):
        print(f"teste 4")
        print(f"valores inseridos loja: store_id:1, new_total: 18, data: 2025/08/31")
        print("resultado esperado 'tarefa realizada com sucesso'")
        time.sleep(2)
        store_id=1
        date_start=datetime.date(2024, 8, 1)
        date_final=datetime.date(2024, 8, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)

        self.assertIsNotNone(cotations_by_time)
        print(cotations_by_time)
        print(f"Teste 4 get_cotation_store_by_data_using_one_month_success: CONCLUIDO. \n")
    #valor não existe na tabela, deve retornar nulo.
    def test_5_get_cotation_store_by_data_using_one_month_None(self):
        print(f"teste 5")
        print(f"valores inseridos loja: store_id: 1, data inicial: 2024/08/01, data final:None")
        print("resultado esperado 'tarefa não realizada'")
        time.sleep(2)
        store_id=1
        date_start=datetime.date(2024, 8, 1)
        date_final= None
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)
        print(f" teste 5 get_cotation_store_by_data_using_one_month_None: CONCLUIDO. \n")

    #valores com mes inicial diferente do mes final, deve retornar os dados em dict.
    def test_6_get_cotation_store_by_data_different_months_success(self):
        print(f"teste 6")
        print(f"valores inseridos loja: store_id: 1, data inicial: 2025/01/01, data final:2025/03/31")
        print("resultado esperado 'tarefa realizada com sucesso'")
        time.sleep(2)
        store_id=1
        date_start=datetime.date(2025, 1, 1)
        date_final=datetime.date(2025, 3, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNotNone(cotations_by_time)

        cotation_dict = {'data':[p for p in cotations_by_time.keys()],
                         'total':[int(p) for p in cotations_by_time.values()]}
        print('cotation_dict ')
        print(f"Teste 6 get_cotation_store_by_data_different_months_success: CONCLUIDO. \n")
    #valores com mes inicial diferente do mes final, mas um mês existe na tabela o outro não.
    #deve retornar os dados em dict.
    def test_7_get_cotation_store_by_data_one_month_exist_and_the_other_not(self):
        print(f"teste 7")
        print(f"valores inseridos loja: store_id: 1, data inicial: 2025/03/01, data final:2025/04/30")
        print("resultado esperado 'tarefa realizada com sucesso'")
        time.sleep(2)
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
        print('cotation_dict')
        print(f"teste 7 get_cotation_store_by_data_one_month_exist_and_the_other_not: CONCLUIDO. \n")

    #valores com o mes final sendo anterior ao do inicio, deve retornar error.
    def test_8_get_cotation_store_by_data_with_date_final_before_than_date_start(self):
        print(f"teste 8")
        print("resultado esperado 'tarefa não realizada'")
        time.sleep(2)
        store_id=1
        date_start=datetime.date(2025, 3, 31)
        date_final=datetime.date(2025, 1, 31)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)
        print(f"teste 8 get_cotation_store_by_data_with_date_final_before_than_date_start: CONCLUIDO. \n")

    #Loja não está na tabela cotation_store, deve retornar None
    def test_9_get_cotation_store_by_data_with_store_not_existing(self):
        print(f"teste 9")
        print("resultado esperado 'tarefa não realizada'")
        time.sleep(2)
        store_id=6
        date_start=datetime.date(2025, 3, 31)
        date_final=datetime.date(2025, 3, 1)
        cotations_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        
        self.assertIsNone(cotations_by_time)
        print(cotations_by_time)
        print(f"Teste 9 get_cotation_store_by_data_with_store_not_existing: CONCLUIDO. \n")
    


def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__': 
    with open('testing.out', 'w') as f: 
        main(f) 
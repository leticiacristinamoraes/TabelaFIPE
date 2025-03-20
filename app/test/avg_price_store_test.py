import datetime
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.avg_price_store import (
    create_prices_store_table, 
    create_price_store,
    drop_price_store, 
    update_price_store,
    calculate_month_price_store,
    update_month_price_store,
    get_cotations_count_by_month,
    get_cotation_by_data

    )
from database.stores import get_stores
import schedules

class TestAvgPriceStore(unittest.TestCase):

    def test_0_create_price_store(self):
        create_prices_store_table()
    
    def test_1_get_price_store_by_data_success(self):
        store_id=1
        date_start=datetime.date(2025, 2, 1)
        date_final=datetime.date(2025, 2, 28)
        prices_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNotNone(prices_by_time)
        self.assertDictEqual(prices_by_time, {'total': 200, 'year': 2025, 'month': 2})
        print(prices_by_time)

    def test_2_get_price_store_by_data_none(self):
        store_id=1
        date_start=datetime.date(2023, 2, 1)
        date_final=datetime.date(2023, 2, 28)
        prices_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNone(prices_by_time)
        print(prices_by_time)

    def test_3_get_price_store_by_data_different_months(self):
        store_id=1
        date_start=datetime.date(2025, 1, 1)
        date_final=datetime.date(2025, 3, 31)
        prices_by_time = get_cotation_by_data(store_id=store_id, 
                                                      date_start=date_start,
                                                      date_final=date_final)
        self.assertIsNotNone(prices_by_time)
        print(prices_by_time)
        cotation_dict = {'data':[p for p in prices_by_time.keys()],
                         'total':[int(p) for p in prices_by_time.values()]}
        self.assertDictEqual()
    '''
    def test_1_task_cotacoes_loja(self):
        result = schedules.start_task_cotacoes_loja()
        self.assertIsNotNone(result)
        pass
    '''      
        
       
        
if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
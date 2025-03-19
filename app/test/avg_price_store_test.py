import datetime
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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


class TestAvgPriceStore(unittest.TestCase):

    def test_0_create_price_store(self):
        create_prices_store_table()

    def test_1_calculate_and_update_price_store(self):
        pass
        prices_by_time = get_cotations_count_by_month(1, datetime.date(2024, 12, 1),datetime.date(2024, 12, 31))
        self.assertIsNotNone(prices_by_time)
        print(prices_by_time)
        new_calculate = calculate_month_price_store(prices_by_time['total'],1)
        self.assertIsNotNone(new_calculate)
        print(new_calculate)
        ids = create_price_store(1, new_calculate, datetime.date(prices_by_time['year'], prices_by_time['month'], 1))
        self.assertIsNotNone(ids)
        print(ids)
    def test_2_calculate_price_store(self):
        prices_cot = get_cotation_by_data(1,datetime.date(2024, 12, 1),datetime.date(2025, 1, 31) )
        self.assertIsNotNone(prices_cot)
        print(prices_cot)

  
        
        
       
        
if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
import datetime
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.avg_price_store import (
    create_prices_store_table, 
    create_price_store, 
    update_price_store,
    calculate_month_price_store,
    update_month_price_store,
    get_cotations_by_month

    )


class TestAvgPriceStore(unittest.TestCase):

    def test_0_create_price_store(self):
        create_prices_store_table()
        pass

    def test_2_calculate_price_store(self):
        pass

    def test_1_calculate_and_update_price_store(self):
        prices_by_time = get_cotations_by_month(1, datetime.date(2024, 12, 1),datetime.date(2024, 12, 31))
        self.assertIsNotNone(prices_by_time)
        print(prices_by_time)
        prices_list = [float(p[0]) for p in prices_by_time]
        self.assertIsNotNone(prices_list)
        print(prices_list)
        new_calculate = calculate_month_price_store(sum(prices_list),1)
        self.assertIsNotNone(new_calculate)
        print(new_calculate)
        ids = create_price_store(1, new_calculate, datetime.date(2024, 8, 15))
        self.assertIsNotNone(ids)

        
        
        
        print(ids)
        
if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
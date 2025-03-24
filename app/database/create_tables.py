from database.month_cotation_store import create_month_cotation_store_table
from database.users import create_users_table
from database.brands import create_brands_table
from database.models import create_models_table
from database.stores import create_stores_table
from database.vehicles import create_vehicles_table
from database.prices import create_prices_table
from database.average_price import create_average_price_table
from database.dezess import create_producaomens_table, criar_funcao_topdez, criar_funcao_media
from database.researcher_commission import create_researcher_commission_table
from database.quotation_researcher import create_quotation_researcher_table
from database.quotation_consults import create_quotation_consults_table
from database.ranking_researchers import create_ranking_researchers_table

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def create_all_tables():
    create_users_table()
    create_brands_table()
    create_models_table()
    create_stores_table()
    create_vehicles_table()
    create_prices_table()
    create_average_price_table()
    create_month_cotation_store_table()
    create_producaomens_table()
    criar_funcao_media()
    criar_funcao_topdez()

    create_researcher_commission_table()
    create_quotation_researcher_table()
    create_quotation_consults_table()
    create_ranking_researchers_table()

    print("Todas as tabelas foram criadas com sucesso!")

if __name__ == "__main__":
    create_all_tables()

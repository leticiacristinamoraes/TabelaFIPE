from database.users import create_users_table
from database.brands import create_brands_table
from database.models import create_models_table
from database.stores import create_stores_table
from database.vehicles import create_vehicles_table
from database.prices import create_prices_table
from database.average_price import create_average_price_table
from database.ranking_researchers import create_ranking_researchers_table

def create_all_tables():
    create_users_table()
    create_brands_table()
    create_models_table()
    create_stores_table()
    create_vehicles_table()
    create_prices_table()
    create_average_price_table()
    create_ranking_researchers_table()

    print("Todas as tabelas foram criadas com sucesso!")

if __name__ == "__main__":
    create_all_tables()

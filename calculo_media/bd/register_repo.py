#TabelaFIPE-base/db/repositories/register_repo.py

#Adicionar estas funções no final do arquivo

def get_prices_by_car(self, car_id):
    """ Consulta todos os preços cadastrados de um carro específico """
    query = select(RegisterDBModel).where(RegisterDBModel.car_id == car_id)
    result = self.__session.execute(query).fetchall()

    if result:
        return [{"id": row[0].id, "price": row[0].price, "date": row[0].created_date} for row in result]
    return []

def get_prices_by_model(self, brand, model):
    """ Consulta todos os preços cadastrados de um modelo específico """
    car_query = select(CarDBModel.id).where(
        (CarDBModel.brand == brand) & (CarDBModel.model == model)
    )
    car_result = self.__session.execute(car_query).fetchall()

    if not car_result:
        return []

    car_ids = [row[0] for row in car_result]
    query = select(RegisterDBModel).where(RegisterDBModel.car_id.in_(car_ids))
    result = self.__session.execute(query).fetchall()

    return [{"id": row[0].id, "price": row[0].price, "date": row[0].created_date} for row in result]

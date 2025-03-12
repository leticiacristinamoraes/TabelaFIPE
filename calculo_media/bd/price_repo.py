#TabelaFIPE-base/db/repositories/avg_price_repo.py

#Adicionar estas funções no final do arquivo

def calculate_and_store_avg_prices(self):
    """ Calcula a média de preços para cada modelo de carro e armazena no banco """
    query = (
        select(RegisterDBModel.car_id, func.avg(RegisterDBModel.price).label("avg_price"))
        .group_by(RegisterDBModel.car_id)
    )

    result = self.__session.execute(query).fetchall()

    for row in result:
        car_id = row[0]
        avg_price = row[1]

        existing_avg = self.__session.execute(
            select(AvgPriceDBModel).where(AvgPriceDBModel.car_id == car_id)
        ).fetchone()

        if existing_avg:
            self.__session.query(AvgPriceDBModel).filter_by(car_id=car_id).update(
                {"avg_price": avg_price}
            )
        else:
            avg_price_db_model = AvgPriceDBModel(
                id=uuid.uuid4(),
                car_id=car_id,
                avg_price=str(avg_price)
            )
            self.__session.add(avg_price_db_model)

    self.__session.commit()

def get_avg_price_by_model(self, brand, model):
    """ Retorna a média de preços de um modelo específico """
    car_query = select(CarDBModel.id).where(
        (CarDBModel.brand == brand) & (CarDBModel.model == model)
    )
    car_result = self.__session.execute(car_query).fetchall()

    if not car_result:
        return None

    car_ids = [row[0] for row in car_result]
    query = select(func.avg(RegisterDBModel.price)).where(RegisterDBModel.car_id.in_(car_ids))
    result = self.__session.execute(query).scalar()

    return result if result else None

import random
from os import getenv

import sqlalchemy as sa
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy.orm import sessionmaker

from app.DataBase.schemas.default_product_schema import DefaultProduct
from app.DataBase.schemas.user_schema import User
from app.Enums.enums import LangEnum

faker = Faker()


def generate_random_user():

    return User(
        name=faker.name(),
        email=faker.unique.email(),
        password=faker.password(12, True, True, True, True),
        birthdate=faker.date_of_birth(minimum_age=18, maximum_age=90),
        language=random.choice(list(LangEnum)),
    )


class Populate:
    def __init__(self, url: str) -> None:
        engine = sa.create_engine(url)
        Session = sessionmaker(bind=engine)
        session = Session()

        users = [generate_random_user() for _ in range(50)]
        session.add_all(users)
        session.commit()

        session.close()

        default_products: list[DefaultProduct] = list()

        # DefaultProducts.append(DefaultProduct(
        #     name="Manga",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Banana",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Arroz",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Feijão",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Carne",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Frango",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Café",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Açúcar",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Sal",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Óleo",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultProducts.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Leite",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Queijo",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Presunto",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Pão",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Padaria"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Macarrão",
        #     unity_types_id=UnityTypes.append.get(name="Pacote"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Molho de tomate",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Farinha de trigo",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Ovos",
        #     unity_types_id=UnityTypes.append.get(name="Caixa"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Maçã",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Laranja",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Cebola",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Alho",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Batata",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Tomate",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Suco",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Refrigerante",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Suco de pozinho",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Água",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Água com gáz",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Sabonete",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Shampoo",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Condicionador",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Papel higiênico",
        #     unity_types_id=UnityTypes.append.get(name="Pacote"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Detergente",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Amaciante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Desinfetante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Alvejante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Limpador multiuso",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Creme dental",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Escova de dentes",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Enxaguante bucal",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Desodorante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Sabão em pó",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Esponja de cozinha",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Leite condensado",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Creme de leite",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Gelatina",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Chá",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Vinagre",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Mostarda",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Ketchup",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Molho de pimenta",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Salsicha",
        #     unity_types_id=UnityTypes.append.get(name="Pacote"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Linguiça",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Peixe",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Atum",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Sardinha",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Margarina",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Manteiga",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Iogurte",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Geléia",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Cereal",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Granola",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Aveia",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Biscoitos",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Bolacha",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Chocolate",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Achocolatado",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Balas",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Chiclete",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Pipoca",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Amendoim",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Castanhas",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Nozes",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Pistache",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Cerveja",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Vinho",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Espumante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Vodka",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Whisky",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Tequila",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Rum",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Martini",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Campari",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Licor",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Azeitonas",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Picles",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Frutas em calda",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Geleia real",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Mel",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Creme de avelã",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Pasta de amendoin",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Marshmallows",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Açúcar mascavo",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Adoçante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Melado",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Chantilly",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Patê",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Ricota",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultProduct(
        #     name="Requeijão",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultProducts.append.get(name="Laticíneos"),
        # )


if __name__ == "__main__":
    load_dotenv()

    DEBUG = bool(int(getenv("DEBUG", "0")))
    DB_DIALECT = getenv("DB_DIALECT", "postgresql")
    DB_USER = getenv("DB_USER", "postgres")
    DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
    DB_IP = getenv("DB_IP", "localhost")
    DB_PORT = getenv("DB_PORT", "5432")
    DB_NAME = getenv("DB_NAME", "postgres")

    SQLALCHEMY_DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"
    Populate(SQLALCHEMY_DATABASE_URL)

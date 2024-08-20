import random
from os import getenv

import sqlalchemy as sa
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy.orm import sessionmaker

from app.Enums.enums import LangEnum
from app.Models.models import User

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

        # DefaultProducts = list()
        #
        # DefaultProducts.append(DefaultCategory(
        #     name="Manga",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Banana",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Arroz",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Feijão",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Carne",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Frango",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Café",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Açúcar",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Sal",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Óleo",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Leite",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Queijo",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Presunto",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Pão",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Padaria"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Macarrão",
        #     unity_types_id=UnityTypes.append.get(name="Pacote"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Molho de tomate",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Farinha de trigo",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Ovos",
        #     unity_types_id=UnityTypes.append.get(name="Caixa"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Maçã",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Laranja",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Cebola",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Alho",
        #     unity_types_id=UnityTypes.append.get(name="Gramas"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Batata",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Tomate",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Hortifruti"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Suco",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Refrigerante",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Suco de pozinho",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Água",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Água com gáz",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Sabonete",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Shampoo",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Condicionador",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Papel higiênico",
        #     unity_types_id=UnityTypes.append.get(name="Pacote"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Detergente",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Amaciante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Desinfetante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Alvejante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Limpador multiuso",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Creme dental",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Escova de dentes",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Enxaguante bucal",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Desodorante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Higiene Pessoal"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Sabão em pó",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Esponja de cozinha",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Limpeza"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Leite condensado",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Creme de leite",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Gelatina",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Chá",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Vinagre",
        #     unity_types_id=UnityTypes.append.get(name="Litros"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Mostarda",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Ketchup",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Molho de pimenta",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Condimentos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Salsicha",
        #     unity_types_id=UnityTypes.append.get(name="Pacote"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Linguiça",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Peixe",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Atum",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Sardinha",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Carnes"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Margarina",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Manteiga",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Iogurte",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Geléia",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Cereal",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Granola",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Aveia",
        #     unity_types_id=UnityTypes.append.get(name="Kilos"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Biscoitos",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Bolacha",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Chocolate",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Achocolatado",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Balas",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Chiclete",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Pipoca",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Amendoim",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Castanhas",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Nozes",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Pistache",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Cerveja",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Vinho",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Espumante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Vodka",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Whisky",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Tequila",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Rum",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Martini",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Campari",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Licor",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bebidas"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Azeitonas",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Picles",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Frutas em calda",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Geleia real",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Mel",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Creme de avelã",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Pasta de amendoin",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Marshmallows",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Açúcar mascavo",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Adoçante",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Melado",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Chantilly",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Bazar"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Patê",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Enlatados"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Ricota",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
        # )
        # DefaultProducts.append(DefaultCategory(
        #     name="Requeijão",
        #     unity_types_id=UnityTypes.append.get(name="Unidade"),
        #     default_categorys_id=DefaultCategorys.append.get(name="Laticíneos"),
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

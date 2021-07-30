import datetime
from peewee import *

"""
    В этом модуле объявлены 2 класса для работы с базой данных, а также функции для работы с данными через экземпляры
    этих классов.
    База данных состоит из двух таблиц: Категория(Идентификационный номер) и Продукт(Номер манипулы). Каждой категории 
    может соответствовать несколько продуктов.
"""

dbhandle = SqliteDatabase('database.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "categories"
        order_by = ('created_at',)


class Product(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    category = ForeignKeyField(Category, related_name='fk_cat_prod', to_field='id', on_delete='cascade',
                               on_update='cascade')
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "products"
        order_by = ('created_at',)


def find_all_categories():
    return Category.select()


def find_all_products():
    return Product.select()


def prod_data():
    """
        Функция возвращает список словарей: {Идентефикационный номер: номер манипулы}
    """
    products = find_all_products()
    product_data = []

    for product in products:
        product_data.append({product.category.name: product.name})
    return product_data


def cat_data():
    """
        Функция возвращает список с идентификационными номерами
    """
    categories = find_all_categories()
    category_data = []
    for category in categories:
        category_data.append(category.name)
    return category_data


def full_data():
    """
        Функция возвращает словарь: {Идентефикационный номер: Список номеров манипул для данного номера, ...}
    """
    full_data = {}
    for cat in cat_data():
        temp_data = []
        for prod in prod_data():
            if cat == list(prod.keys())[0]:
                temp_data.append(prod.get(cat))
        full_data[cat] = temp_data
    return full_data

from peewee import *
import datetime


db = MySQLDatabase('store_app', user='root', password='',
                   host='localhost')


class Category(Model):
    category_name = CharField(40)

    class Meta:
        database = db


class Suppliers(Model):
    suppliers_name = CharField(40)

    class Meta:
        database = db


class Product(Model):
    product_name = CharField(40)
    category = ForeignKeyField(Category, backref='category', null=True)
    product_code = IntegerField()
    product_buy = IntegerField()
    product_sale = IntegerField()
    product_image = CharField(255)
    product_address = TextField()
    product_date = DateTimeField(default=datetime.datetime.now)
    product_quantity = IntegerField()
    supplier = ForeignKeyField(Suppliers, backref='supplier', null=True)

    class Meta:
        database = db


class Invoise(Model):
    number_invoise = CharField(40)
    created_date = DateTimeField(default=datetime.datetime.now)
    customer = CharField(40)
    conatct = CharField()
    phone = CharField(20)
    item = CharField(40)
    quantity = IntegerField()
    amoute = DoubleField()

    class Meta:
        database = db





class Users(Model):
    name = CharField(40)
    email = CharField()
    password = CharField(15)

    class Meta:
        database = db


class UserPermission(Model):
    user = CharField()
    tab_home = IntegerField()
    tab_product = IntegerField()
    tab_stock = IntegerField()
    tab_product_sale = IntegerField()
    tab_setting = IntegerField()
    tab_permission = IntegerField()
    tab_show_Invoice = IntegerField()
    tab_report = IntegerField()

    class Meta:
        database = db


db.connect()
db.create_tables([Category, Suppliers, Product,Invoise, Users, UserPermission])

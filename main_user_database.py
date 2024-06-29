from pathlib import Path
import json

from peewee import SqliteDatabase, Model, TextField, \
    ForeignKeyField, IntegerField, CharField, FloatField, AutoField

db_site_info = SqliteDatabase(Path('site_info.db'))


class BaseModelDatabase(Model):
    class Meta:
        database = db_site_info


class Country(BaseModelDatabase):
    country = TextField(primary_key=True, column_name='Country')
    market = TextField(column_name='Market')
    locale = TextField(column_name='Locale')
    currencyTitle = TextField(column_name='Currency Title')
    currency = TextField(column_name='Currency')


class City(BaseModelDatabase):
    localizedName = TextField(primary_key=True)
    country = ForeignKeyField(Country, backref='country')
    entityId = IntegerField()


class Airport(BaseModelDatabase):
    id = TextField()
    country = ForeignKeyField(Country, backref='airport_country')
    city = ForeignKeyField(City, backref='airport_city')
    title = TextField()
    suggestionTitle = TextField()
    skyId = TextField(primary_key=True)
    entityId = IntegerField()


def write_database(db, model, data):
    with db.atomic():
        print(data)
        model.insert_many(data).execute()


class InterfaceDB:
    @staticmethod
    def write_db():
        return write_database


write_data = InterfaceDB.write_db()
db_site_info.create_tables([Country, City, Airport])
# data_country = list()
# data_city = list()
# data_airport = list()

with open('get_config.json', 'r') as file:
    data_file = json.load(file)
    for i_data in data_file['data']:
        data_country = list()
        data_country.append(
            {
                'country': i_data['country'],
                'market': i_data['market'],
                'locale': i_data['locale'],
                'currencyTitle': i_data['currencyTitle'],
                'currency': i_data['currency']
            }
        )
        print(data_country)
        write_data(db_site_info, Country, data_country)

with open('auto_complete.json', 'r') as file:
    data_file = json.load(file)
    for i_data in data_file['data']:
        data_city = list()
        data_city.append(
            {
                'localizedName': i_data['navigation']['relevantHotelParams']['localizedName'],
                'country': i_data['presentation']['subtitle'],
                'entityId': int(i_data['navigation']['relevantHotelParams']['entityId'])
            }
        )
        data_airport = list()
        data_airport.append(
            {
                'id': i_data['id'],
                'country': i_data['presentation']['subtitle'],
                'city': i_data['navigation']['relevantHotelParams']['localizedName'],
                'title': i_data['presentation']['title'],
                'suggestionTitle': i_data['presentation']['suggestionTitle'],
                'skyId': i_data['navigation']['relevantFlightParams']['skyId'],
                'entityId': int(i_data['navigation']['entityId'])
            }
        )
        write_data(db_site_info, City, data_city)
        write_data(db_site_info, Airport, data_airport)



# write_data(db_site_info, Country, data_country)
# write_data(db_site_info, City, data_city)
# write_data(db_site_info, Airport, data_airport)

# python -m pip install sqlalchemy
# https://dev.mysql.com/downloads/connector/python/

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import inspect


df=pd.read_csv('population.csv', sep=',')

engine = create_engine('mysql+mysqlconnector://***:***@****-ddl.azr-netherlands-1.svc.singlestore.com/***')

df.to_sql(name='population',con=engine,if_exists='fail',index=False) 

inspector=inspect(engine)

for name in inspector.get_table_names('zipcode'):
    print(name)
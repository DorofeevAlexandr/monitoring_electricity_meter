import datetime as dt
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import time

import adapters
from time_series_base import client_influxdb, write_electro_counters_values, read_electro_counters_values
from electro_counters import (read_electro_counters_params_in_base, read_electro_counters_update_in_base)


def postgres_engine():
    load_dotenv()
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST', 'db')
    # db_host = 'localhost'
    db_port = str(os.environ.get('DB_PORT', 5432))

    # Connecto to the database
    db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    # print(db_string)
    result_engine = create_engine(db_string)
    print(result_engine)
    return result_engine

def read_counters_save_current_params(p_engine):
    with Session(autoflush=False, bind=p_engine) as db:
        try:
            registers = adapters.get_registers()
            counters_params = read_electro_counters_params_in_base(session=db)
            read_electro_counters_update_in_base(db, counters_params, registers)
        except Exception as e:
            print('error', e)
            print(registers)
            print(counters_params)
        return  counters_params


if __name__ == '__main__':
    engine = postgres_engine()
    client = client_influxdb()
    dt_last_save_current_params = dt.datetime.now()
    dt_last_save_lengths = dt.datetime.now()
    while True:
        time.sleep(600)
        if dt.datetime.now() - dt_last_save_current_params >= dt.timedelta(seconds=1):
            counters_params = read_counters_save_current_params(p_engine=engine)
            if counters_params:
                write_electro_counters_values(client=client,
                                              counters_params=counters_params)
            dt_last_save_current_params = dt.datetime.now()

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv


def client_influxdb():
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "12"
    url = "http://influxdb:8086"
    print(token)
    return influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def write_electro_counters_values(client, counters_params:list):
    bucket = "ElectroCounters"
    org = "12"
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for counter in counters_params:
        number = counter['number']
        client_name = counter['client_name']
        energy_indic = counter['energy_indic']
        energy_k = counter['energy']
        point = (
            Point(f"Counter_{number}")
            .tag("client_name", client_name)
            .field("energy_indic", energy_indic)
            .field("energy", energy_k)
            )

        write_api.write(bucket=bucket, org=org, record=point)
        # print(point)


def read_electro_counters_values(client):
    org = "12"
    query_api = client.query_api()

    query = """from(bucket: "ElectroCounters")
     |> range(start: -100m)
     |> filter(fn: (r) => r._measurement == "Counter_2")"""
    tables = query_api.query(query, org=org)

    for table in tables:
      for record in table.records:
        pass
        # print(record)

import datetime as dt
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from django.http import HttpResponse
import io
import influxdb_client, os
import operator
import random
import xlsxwriter

from electricity_meter.models import ElectroCounters


def get_counters_params():
    counters_names = {}
    counters = ElectroCounters.objects.order_by('number')
    for c in counters:
        counters_names[c.number] = {
                          'client_name': c.client_name,
                          'address': c.address,
                          'transformation_coefficient': c.transformation_coefficient,
                          'energy_indic': str(c.energy_indic / 1000),
                          'energy': str(c.energy / 1000),
                          }
    return counters_names


def get_counters_from_base():
    res_counters = []
    counters = ElectroCounters.objects.order_by('number')
    for c in counters:
        res_counters.append({'number': c.number,
                          'client_name': c.client_name,
                          'address': c.address,
                          'transformation_coefficient': c.transformation_coefficient,
                          'energy_indic': str(c.energy_indic / 1000),
                          'energy': str(c.energy / 1000),
                          })
    return res_counters


def client_influxdb():
    load_dotenv()
    token = os.environ.get("INFLUXDB_TOKEN")
    # token = os.environ.get("TEST_SERVER_INFLUXDB_TOKEN")
    org = "12"
    url = "http://influxdb:8086"
    # url = "http://127.0.0.1:8086"
    # url = os.environ.get("TEST_SERVER_INFLUXDB_URL")
    print(token)
    return influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def generate_random_hex_color(const_collor_number=-1):
    if const_collor_number == 0:
         r, g, b = 200, 17, 34
    elif const_collor_number == 1:
        r, g, b = 50, 0, 150
    elif const_collor_number == 2:
        r, g, b = 43, 129, 48
    elif const_collor_number == 3:
        r, g, b = 137, 73, 161
    elif const_collor_number == 4:
        r, g, b = 242, 228, 57
    elif const_collor_number == 5:
        r, g, b = 83, 17, 34
    elif const_collor_number == 6:
        r, g, b = 122, 202, 173
    elif const_collor_number == 7:
        r, g, b = 174, 155, 22
    elif const_collor_number == 8:
        r, g, b = 198, 126, 172
    elif const_collor_number == 9:
        r, g, b = 26, 30, 31
    else:
        # Генерируем три случайных целых числа в диапазоне 0–255 для RGB
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    # print(r, g, b)
    # Форматируем в виде #RRGGBB
    return f"#{r:02X}{g:02X}{b:02X}"


def power_consumption(values):
    for cn in values:
        len_values = len(values[cn]['count_val'])
        for ind, val in enumerate(values[cn]['count_val']):
            if ind + 1 < len_values:
                next_val = values[cn]['count_val'][ind + 1]
            else:
                next_val = 0
            if val != 0 and next_val != 0:
                power_consumption = int(next_val - val)
                power_consumption = 0 if power_consumption > 10_000_000 else power_consumption
            else:
                power_consumption = 0
            values[cn]['count_val'][ind] = max(power_consumption, 0)


def summ_power_consumption(values):
    result = []
    times = []
    for counter in values:
        len_values = len(values[counter]['count_val'])
        if len(result) < len_values:
            len_result = len(result)
            result.extend([0 for _ in range(len_values - len_result)])
            times.extend(values[counter]['times'][len_result : len_values])
        result = list(map(lambda x, y: x + y, result, values[counter]['count_val']))

    values['Суммарное потребление'] = {'count_val': result,
                           'times': times,
                           'color': '#000000',
                           }


def get_times(time_start: dt.datetime, time_end:dt.datetime, step_minutes=60):
    times = []
    step_time = dt.timedelta(minutes=step_minutes)
    cur_time = time_start
    while cur_time < time_end:
        times.append(cur_time)
        cur_time = cur_time + step_time
    times.append(time_end)
    return times


def get_time_period(date: dt.date, data_reading_period='1 day', st_step_time='1h'):
    time_start = dt.datetime(year=date.year,
                             month=date.month,
                             day=date.day,
                             hour=0,
                             minute=0,
                             second=0)
    if data_reading_period == '1 day':
        time_end = time_start +  dt.timedelta(days=1)
    elif data_reading_period == '1 month':
        end_date = date + relativedelta(months=1)
        time_end = dt.datetime(year=end_date.year,
                                 month=end_date.month,
                                 day=end_date.day,
                                 hour=0,
                                 minute=0,
                                 second=0)
    else:
        time_end = time_start

    if st_step_time == '1h':
        time_start = time_start - dt.timedelta(hours=1)
    if st_step_time == '1d':
        time_start = time_start - dt.timedelta(days=1)

    return time_start, time_end


def get_counter_number(counter_st_number:str)->int:
    st_number = counter_st_number[-1]
    try:
        number = int(st_number)
    except ValueError:
        number = 0
    return  number


def parse_electro_counters_values(tables):
    times = {}
    values = {}
    counters_params = get_counters_params()
    # print(counters_params)
    for table in tables:
        for record in table.records:
            # print('--------------')
            # print(record)
            # print(record['_time'], record['_field'], record['_value'])
            measurement_time = (dt.datetime(year=record['_time'].year,
                                            month=record['_time'].month,
                                            day=record['_time'].day,
                                            hour=record['_time'].hour,
                                            minute=record['_time'].minute) +
                                dt.timedelta(hours=3))

            if measurement_time not in times.keys():
                times[measurement_time] = {}
            counter_number = get_counter_number(record['_measurement'])
            # print(counter_number)
            if counter_number == 0:
                continue
            client_name = f'{counter_number} - {counters_params[counter_number]['client_name']}'
            if client_name not in values.keys():
                values[client_name] = {'count_val' : [],
                                       'times' : [],
                                       'color': generate_random_hex_color(const_collor_number=len(values)),
                                       }
                # print(client_name)

            values[client_name]['count_val'].append(record['_value'] * counters_params[counter_number]['transformation_coefficient'])
            values[client_name]['times'].append(measurement_time)

    return times, values

def read_electro_counters_values(client, date: dt.date, data_reading_period='1 day', st_step_time='1h'):
    org = "12"
    query_api = client.query_api()

    time_start, time_end = get_time_period(date, data_reading_period)

    st_time_start = f'{time_start.isoformat()}+03:00'
    st_time_end = f'{time_end.isoformat()}+03:00'

    query = f"""from(bucket: "ElectroCounters")    
     |> range(start: {st_time_start}, stop: {st_time_end})
     |> aggregateWindow(every: {st_step_time}, fn: max, createEmpty: false)
     |> group(columns: ["_time"])
     |> filter(fn: (r) => r._field == "energy_indic")"""
    # print(query)


    tables = query_api.query(query, org=org)
    times, values = parse_electro_counters_values(tables=tables)
    power_consumption(values)
    summ_power_consumption(values)
    # print(times)
    # print(values)
    return times, values


def get_reports_electro_counters(values:dict, cur_month):
    reports = {}
    for client_name, l_value in values.items():
        if client_name not in reports.keys():
            reports[client_name] = [[0 for _ in range(31)] for _ in range(24)]
        for ind, time in enumerate(l_value['times']):
            if time.month != cur_month:
                continue
            day = time.day
            hour = time.hour
            reports[client_name][hour][day - 1] = str(l_value['count_val'][ind] / 1000)
    return reports


def calculate_result_value(reports:dict):
    for report in reports.values():
        result = [0 for _ in range(31)]
        for hour_values in report:
            result = list(map(operator.add, result, map(float, hour_values)))
        report.append(result)


def save_report_in_excel(reports:dict, date:dt.date, title:str):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    bold_format = workbook.add_format({'bold': True, 'border': 2, 'align': 'center'})
    def_format = workbook.add_format({'bold': False, 'border': 1})

    for client_name, counter_values in reports.items():
        worksheet = workbook.add_worksheet(client_name[0:30])

        worksheet.write(0, 0, title)
        worksheet.write(1, 0, client_name)

        worksheet.set_column(0, 0, 17)

        worksheet.merge_range("A3:AF3", "Сутки потребления электроэнергии", bold_format)

        row_offset = 3
        col_offset = 0
        worksheet.write(row_offset, col_offset, 'Часы', bold_format)
        for day in range(31):
            worksheet.write(row_offset, col_offset + day + 1, day + 1, bold_format)

        row_offset = 4
        col_offset = 0
        for ind_r, hour_values in enumerate(counter_values):
            if ind_r != 24:
                worksheet.write(row_offset + ind_r, col_offset, f'{ind_r} - {ind_r + 1}',bold_format)
            else:
                worksheet.write(row_offset + ind_r, col_offset, 'Итого за сутки', bold_format)

            for ind_c, day_values in enumerate(hour_values):
                worksheet.write(row_offset + ind_r, col_offset + ind_c + 1,
                                float(day_values), def_format)

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )
    response['Content-Disposition'] =  f'attachment; filename=Report_{date.strftime('%m_%Y')}.xlsx'
    return response


if __name__ == '__main__':
    print('--------------------')
    client = client_influxdb()
    read_electro_counters_values(client=client,
                                 date=dt.date.today())

from datetime import datetime

from models import ElectroCounters


COUNTER_SIMULATION = False


def get_counter_indicator_value(registers, address):
    try:
        if registers:
            w0 = registers[address + 0]
            w1 = registers[address + 1]
            return w1 * 65536 + w0
        return 0
    except:
        return 0


def read_electro_counters_update_in_base(session, counters_params, registers):
    for counter in counters_params:
        if COUNTER_SIMULATION:
            energy_indic = datetime.now().second
        else:
            energy_indic = get_counter_indicator_value(registers, counter['address'])
        energy_k = energy_indic * counter['transformation_coefficient']
        counter['energy'] = energy_k
        update_counter_in_base(session,
                              counter_params=counter,
                              energy_indic=energy_indic,
                              energy=energy_k)


def read_electro_counters_params_in_base(session):
    params = []
    counters = session.query(ElectroCounters).all()
    for counter in counters:
        params.append({
            'id' : counter.id,
            'number' : counter.number,
            'client_name' : counter.client_name,
            'address' : counter.address,
            'transformation_coefficient' : counter.transformation_coefficient,
            'energy_indic': counter.energy_indic,
            'energy' : counter.energy,
            })
    return sorted(params, key=lambda x: x['number'])



def update_counter_in_base(session, counter_params, energy_indic=0, energy=0):
    number = counter_params['number']
    counter = session.query(ElectroCounters).filter(ElectroCounters.number==number).first()
    if counter:
        counter.energy_indic = energy_indic
        counter.energy = energy
        counter.updated_dt = datetime.now()
    else:
        counter = ElectroCounters(line_number=counter_params['number'])
    session.add(counter)
    session.commit()

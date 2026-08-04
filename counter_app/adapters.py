from dotenv import load_dotenv
import os
import time
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient


load_dotenv()


ELECTRO_COUNTER_ADAPTER_HOST = os.environ.get('ELECTRO_COUNTER_ADAPTER_HOST')
ELECTRO_COUNTER_ADAPTER_PORT = 502


# set global
regs = {key: 0 for key in range(0, 100)}

# init a thread lock
regs_lock = Lock()


def get_counter_indicator_value(registers, address):
    import struct

    try:
        if registers:
            w0 = registers[address + 0]
            w1 = registers[address + 1]
            buffer = struct.pack('HH', w0, w1)
            # print(buffer)
            # parameter.value = '%.3f' % struct.unpack('f', buffer)[0]
            value = struct.unpack('f', buffer)[0]
            print(address, w0, w1, value)
            return value
        return 0
    except:
        return 0


# modbus polling thread
def polling_thread():
    global regs
    c = ModbusClient(host=ELECTRO_COUNTER_ADAPTER_HOST, port=ELECTRO_COUNTER_ADAPTER_PORT)
    # polling loop
    while True:
        # keep TCP open
        if not c.is_open():
            c.open()
        # do modbus reading on socket
        reg_list_0 = c.read_holding_registers(0, 100)
        # if read is ok, store result in regs (with thread lock synchronization)
        if reg_list_0:
            with regs_lock:
                for i in range(0, 100):
                    regs[0 + i] = reg_list_0[i]

        # 1s before next polling
        time.sleep(10)

# start polling thread
tp = Thread(target=polling_thread)
# set daemon: polling thread will exit if main thread exit
tp.daemon = True
tp.start()

def get_registers():
    with regs_lock:
         # regs = {0: 3, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
         #        10: 0, 11: 40905, 12: 88, 13: 65535, 14: 65535, 15: 8090, 16: 10, 17: 32923, 18: 4, 19: 0,
         #        20: 0, 21: 2140, 22: 45, 23: 65535, 24: 65535, 25: 42328, 26: 17, 27: 6325, 28: 2, 29: 0,
         #        30: 0, 31: 24552, 32: 15, 33: 65535, 34: 65535, 35: 28503, 36: 12, 37: 9783, 38: 0, 39: 0,
         #        40: 0, 41: 12450, 42: 56, 43: 65535, 44: 65535, 45: 62958, 46: 21, 47: 17873, 48: 0, 49: 0,
         #        50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0,
         #        60: 0, 61: 0, 62: 0, 63: 0, 64: 0, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0,
         #        70: 0, 71: 0, 72: 0, 73: 0, 74: 0, 75: 0, 76: 0, 77: 0, 78: 0, 79: 0,
         #        80: 0, 81: 0, 82: 0, 83: 0, 84: 0, 85: 0, 86: 0, 87: 0, 88: 0, 89: 0,
         #        90: 0, 91: 0, 92: 0, 93: 0, 94: 0, 95: 0, 96: 0, 97: 0, 98: 0, 99: 0
         #        }
         result = regs.copy()
    return result


if __name__ == '__main__':
    while True:

        reg = get_registers()
        print(get_registers())
        print(get_counter_indicator_value(reg, 10))
        print(get_counter_indicator_value(reg, 11))
        print(get_counter_indicator_value(reg, 12))
        print(get_counter_indicator_value(reg, 13))
        print(get_counter_indicator_value(reg, 14))
        print(get_counter_indicator_value(reg, 15))
        print(get_counter_indicator_value(reg, 16))
        print(get_counter_indicator_value(reg, 17))
        print(get_counter_indicator_value(reg, 18))
        print(get_counter_indicator_value(reg, 19))
        print(get_counter_indicator_value(reg, 20))
        # time.sleep(10)
        exit()

import serial, time, socket, os

port = '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0'
labels = ['lox_tank_top', 'lox_tank_bot', '3', 'chamber', '5']
log = open('/home/rocket/logs/thermocouple.csv', 'a')

def millis():
    return int(time.time_ns() / 1000000)

while True:
    try:
        serial_port = serial.Serial(port, 9600, timeout=0.1)
    except:
        continue
    finally:
        break

addr = ('127.0.0.1', 2000)
client = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

prev = millis()

while True:
    try:
        line = serial_port.readline()
    except:
        os._exit(1)
    line = line.decode()
    data = line[:-2].split(',')
    if len(data) == len(labels):
        now = millis()
        log.write(str(now) + ',' + line)
        if now > prev + 500:
            for l, d in zip(labels, data):
                if d != 'null':
                    bytes = (l + ' ' + l + '=' + d + ' ' + str(now * 1000000)).encode()
                    client.sendto(bytes, addr)
            prev = now

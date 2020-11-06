from bme280 import load_calibration_params
from bme280 import sample
from smbus2 import SMBus

port = 1
address = 0x76
bus = SMBus(port)

calibration_params = load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
print(f"Now: {data.timestamp}")
print(f"Temp: {data.temperature * 1.8 + 32} F")
print(f"Pressure: {data.pressure}")
print(f"Humidity: {data.humidity}")


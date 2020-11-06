import smbus2
import bme280

port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
print(f"Now: {data.timestamp}")
print(f"Temp: {data.temperature * 1.8 + 32} F")
print(f"Pressure: {data.pressure}")
print(f"Humidity: {data.humidity}")


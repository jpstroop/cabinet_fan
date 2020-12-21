Raspberry Pi project to control AC cooling fans for a media cabinet based on readings from a BME280.

## To Run

There are sensible defaults, and they assume the steps/setting explained below under [Hardware](#Hardware). Everything can be overridden in [config.json](./config.json). This file can be a sibling of main.py, or can be copied to `~/cabinet_fan.json`. The latter instance will be preferred if it exists.

## Dependencies

### System:

```bash
$ sudo apt-get install python-smbus i2c-tools
```

### Python:

Developed using Python `3.8.6`.

See [Pipfile](./Pipfile) or [requirements.txt](./requirements.txt) and install using your tool of choice.

### Hardware

#### BME280

 * Follow these [instructions](https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python) or just use `raspi-config` to enable the I2C interface.
 * Test your connection with `i2cdetect -y 1`

    You should see something like:
    ```
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- 76 --
    ```

#### HD44780

 * [Instructions](https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/overview/)

## Run as a Service

See [`thermostat.service`](./thermostat.service). I usually download the source tarball to `/home/pi/apps`. Assuming you've done that, the setting in that script should work just fine. You may need to adjust the version information in the directory name and the location of the Python executable.

To enable the service:

```bash
sudo systemctl link /home/pi/apps/cabinet_fan-0.0.4/thermostat.service
sudo systemctl daemon-reload
sudo systemctl enable thermostat.service
sudo systemctl start thermostat.service
```

It should just work.

## Schematic

![Schematic 0.0.1](/schema0.0.1.png?raw=true)

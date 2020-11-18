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

#### BMP280

Enable SPI and the auxiliary SPI by adding:

```
dtparam=spi=on
dtoverlay=spi1-3cs
```

to `/boot/config.txt` and restarting your pi. I'd love to say there's a single great tutorial out there on running multiple BMP280s on one pi, but no such luck. I used [this device](https://www.amazon.com/gp/product/B07S98QBTQ/) and was able to get everything working. The pins on that device map as follows:

| Sensor | Raspberry pi               |
| ------ | -------------------------- |
| VCC    | 3v3 power                  |
| GND    | ground                     |
| SCL    | SCLK (GPIO 11 / 21)        |
| SDA    | MOSI (GPIO 10 / 20)        |
| CSB    | (Chip Select - you choose) |
| SDO    | MISO (GPIO 9 / 19)         |

#### HD44780

This is more straightforward. Setup is based on these [instructions](https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/overview/). I used [these](https://www.amazon.com/gp/product/B00HJ6AFW6/).

## Schematic

![Schematic 0.0.1](/schema0.0.1.png?raw=true)

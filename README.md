# Fancabinet 

Raspberry Pi project to control AC cooling fans for a media cabinet based on readings from a BME280.

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

 * [Instructions](https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python)
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

 * [Instructions](https://tutorials-raspberrypi.com/raspberry-pi-lcd-display-16x2-characters-display-hd44780/)

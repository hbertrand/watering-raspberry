import csv
import datetime
import time

import RPi.GPIO as GPIO


def init_gpio(pin_sensor, pin_pump):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin_sensor, GPIO.IN)
    GPIO.setup(pin_pump, GPIO.OUT)
    GPIO.output(pin_pump, GPIO.LOW)
    GPIO.output(pin_pump, GPIO.HIGH)


def water_plant(pin_pump):
    # Turn the pump on for 1 second
    GPIO.output(pin_pump, GPIO.LOW)
    time.sleep(3)
    GPIO.output(pin_pump, GPIO.HIGH)

    # Write in the log
    date = datetime.datetime.now()
    with open('static/plant_log.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([date.year, date.month, date.day, date.hour, date.minute])


def water_loop(pin_sensor, pin_pump):
    while 1:
        water_plant(pin_pump)

        time.sleep(3600*12)


if __name__ == "__main__":
    pin_sensor = 7
    pin_pump = 11

    init_gpio(pin_sensor, pin_pump)

    try:
        water_loop(pin_sensor, pin_pump)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup()

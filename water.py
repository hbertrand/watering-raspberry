import argparse
import csv
import datetime
import sys
import time

import RPi.GPIO as GPIO


def init_gpio(pin_pump):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin_pump, GPIO.OUT)
    GPIO.output(pin_pump, GPIO.LOW)
    GPIO.output(pin_pump, GPIO.HIGH)


def water_plant(pin_pump, index):
    # Turn the pump on for 2 second
    GPIO.output(pin_pump, GPIO.LOW)
    time.sleep(index * 2.5)
    GPIO.output(pin_pump, GPIO.HIGH)

    # Write in the log
    date = datetime.datetime.now()
    with open('static/plant_log_{}.csv'.format(index), 'a') as f:
        writer = csv.writer(f)
        writer.writerow([date.year, date.month, date.day, date.hour, date.minute])


def water_loop(pin_pump, index):
    while 1:
        water_plant(pin_pump, index)

        time.sleep(3600*12)


if __name__ == "__main__":
    # Argparser
    parser = argparse.ArgumentParser(description='Water my plants.')

    parser.add_argument('--plant', type=int, required=True,
                        help='Which plant to water, as an int')

    args = parser.parse_args(sys.argv[1:])

    pin_pump_dict = {
        1: 11,
        2: 13
    }

    assert args.plant in pin_pump_dict

    pin_pump = pin_pump_dict[args.plant]

    init_gpio(pin_pump)

    try:
        water_plant(pin_pump, args.plant)
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup()

    GPIO.cleanup()

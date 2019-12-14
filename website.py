import csv

from flask import Flask, render_template

app = Flask(__name__)


def read_plant_log(index):
    plant_log = []
    with open('static/plant_log_{}.csv'.format(index), 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            year, month, day, hour, minute = row
            formatted_row = '{}-{}-{} {:02}:{:02}'.format(year, month, day, int(hour), int(minute))
            plant_log.append(formatted_row)

    if len(plant_log) > 20:
        plant_log = plant_log[-20:]

    return plant_log


@app.route('/')
def hello():
    plant_log_1 = read_plant_log(1)
    plant_log_2 = read_plant_log(2)

    return render_template('index.html', plant_log_1=plant_log_1, plant_log_2=plant_log_2)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=15080, debug=False)

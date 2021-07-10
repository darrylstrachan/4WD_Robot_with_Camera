from gpiozero import LED
import os
import time
from flask import Flask, jsonify
from gpiozero import Robot

rear_wheels = Robot(left=(5, 6), right=(23,24))#right=(5,6))
front_wheels = Robot(left=(19, 26), right=(12,16)) #, right=(19,26))#right=(12,16))

app = Flask(__name__)

@app.route("/")
def hello_world():
    json_file = {}
    json_file['query'] = 'Hello_World'
    return jsonify(json_file)

@app.route("/raspberry/led_test/on")
def led_test_on():
    json_file = {}
    led = LED(18)
    #while True:
    led.on()
    time.sleep(5)
    led.off()
    time.sleep(5)
    json_file['result'] = 'LED is turned On'
    return jsonify(json_file)

@app.route("/raspberry/led_test/off")
def led_test_off():
    json_file = {}
    led = LED(18)
    led.off()
    json_file['result'] = 'LED is turned Off'
    return jsonify(json_file)

@app.route("/auth/<username>/<password>")
def auth(username, password):
    result = {}
    if username == "darryl":
        if password == "password":
            result['auth'] = 'success'
            return jsonify(result)
        else:
            result['auth'] = 'failure'
            return jsonify(result)


@app.route("/temperature/")
def temperature_of_raspberry_pi():
    result = {}
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    cpu_temp = cpu_temp.replace("temp=", "")
    cpu_temp = cpu_temp.rstrip("\n")
    result['temperature'] = cpu_temp
    return jsonify(result)

@app.route("/move-robot/<direction>")
def move_robot(direction):
    result = {}
    if direction == "up":
        rear_wheels.backward()
        front_wheels.forward()
        time.sleep(1)
        rear_wheels.stop()
        front_wheels.stop()
    if direction == "down":
        rear_wheels.forward()
        front_wheels.backward()
        time.sleep(1)
        rear_wheels.stop()
        front_wheels.stop()
    if direction == "left":
        rear_wheels.right()
        front_wheels.right()
        time.sleep(1)
        rear_wheels.stop()
        front_wheels.stop()
    if direction == "right":
        rear_wheels.left()
        front_wheels.left()
        time.sleep(1)
        rear_wheels.stop()
        front_wheels.stop()
    result['direction'] = direction
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0")



#!/usr/bin/env python
from __future__ import print_function, division
from gpiozero import Motor

motor = Motor(23,24)



# from RPIO import PWM
# import RPIO

# import SimpleHTTPServer
# import SocketServer
#
# class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path = '/simplehttpwebpage_content.html'
#         return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
#
# Handler = MyRequestHandler
# server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)
#
# server.serve_forever()

# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(16, GPIO.OUT)
#
# p = GPIO.PWM(16, 1000)
# p.start(0.5)
# input('Press return to stop:')   # use raw_input for Python 2
# p.stop()
# GPIO.cleanup()




# servo = PWM.Servo()
#
# # Set servo on GPIO17 to 1200µs (1.2ms)
# servo.set_servo(17, 1200)
#
# # Set servo on GPIO17 to 2000µs (2.0ms)
# servo.set_servo(17, 2000)
#
# # Clear servo on GPIO17
# servo.stop_servo(17)
#
# RPIO.setup(24, RPIO.OUT)
# RPIO.output(24, True)
#
# PWM.setup()
# # 100us, 10kHz
# # PWM.init_channel(0, 100)
# PWM.init_channel(0)
#
# # while True:
# #     add_channel_pulse(0, 23, 0, )
#
# # Add some pulses to the subcycle
# PWM.add_channel_pulse(0, 23, 0, 50)
# PWM.add_channel_pulse(0, 23, 100, 50)
#
# while True:
#     print('.')
#
# # Stop PWM for specific GPIO on channel 0
# PWM.clear_channel_gpio(0, 23)
#
# # Shutdown all PWM and DMA activity
# PWM.cleanup()
#
# RPIO.cleanup()
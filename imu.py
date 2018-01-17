#!/usr/bin/python

import smbus
import math
import time
from os import system


#reading a byte
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_accel_xout():
	return read_word_2c(0x3b)
	
def get_accel_yout():
	return read_word_2c(0x3d)
	
def get_accel_zout():
	return read_word_2c(0x3f)

def get_accel_xout_scaled():
	return (get_accel_xout / 16384.0)
	
def get_accel_yout_scaled():
	return (get_accel_yout / 16384.0)
	
def get_accel_zout_scaled():
	return (get_accel_zout / 16384.0)

def get_gyro_xout():
	return read_word_2c(0x43)
	
def get_gyro_yout():
	return read_word_2c(0x45)
	
def get_gyro_zout():
	return read_word_2c(0x47)
	
def get_gyro_xout_scaled():
	return (get_gyro_xout/131)
	
def get_gyro_yout_scaled():
	return (get_gyro_yout/131)
	
def get_gyro_zout_scaled():
	return (get_gyro_zout/131)
	
def get_current_x_rotation():
	return get_x_rotation(get_accel_xout_scaled, get_accel_yout_scaled, get_accel_zout_scaled)

def get_current_y_rotation():
	return get_y_rotation(get_accel_xout_scaled, get_accel_yout_scaled, get_accel_zout_scaled)

	
	
	
def initialize_imu():
	# Power management registers
	power_mgmt_1 = 0x6b
	power_mgmt_2 = 0x6c

	bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
	address = 0x68       # This is the address value read via the i2cdetect command

	# Now wake the 6050 up as it starts in sleep mode
	bus.write_byte_data(address, power_mgmt_1, 0)
	
def run_imu():
	
	initialize_imu()
	
	while True:
		time.sleep(0.1)
		gyro_xout = read_word_2c(0x43)
		gyro_yout = read_word_2c(0x45)
		gyro_zout = read_word_2c(0x47)

		print "gyro_xout : ", gyro_xout, " scaled: ", (gyro_xout / 131)
		print "gyro_yout : ", gyro_yout, " scaled: ", (gyro_yout / 131)
		print "gyro_zout : ", gyro_zout, " scaled: ", (gyro_zout / 131)

		accel_xout = read_word_2c(0x3b)
		accel_yout = read_word_2c(0x3d)
		accel_zout = read_word_2c(0x3f)

		accel_xout_scaled = accel_xout / 16384.0
		accel_yout_scaled = accel_yout / 16384.0
		accel_zout_scaled = accel_zout / 16384.0

		print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
		print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
		print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

		print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

		time.sleep(0.5)
		system('clear')
#!/usr/bin/python
#make sure to run the initialize_imu() function before running any of the addresses otherwise the code will error out.
import smbus
import math
import time
from os import system
import os.path

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


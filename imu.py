Skip to content
This repository
Search
Pull requests
Issues
Marketplace
Explore
 @SleepyToddlers
Sign out
0
0 0 SleepyToddlers/code
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Insights  Settings
code/imu.py
a08c001  on Jan 21
@fsqiu fsqiu removed py_cache
@dmsnie @fsqiu
     
265 lines (195 sloc)  7.27 KB
#!/usr/bin/python
# External Libraries
import smbus
import math
import time

''' Reading / Setup Functions ---------------------------------------------------- '''
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

''' X,Y,Z Accel Output Functions ---------------------------------------------------- '''
def get_accel_xout():
	return (read_word_2c(0x3b) / 16384.0)

def get_accel_yout():
	return (read_word_2c(0x3d) / 16384.0)

def get_accel_zout():
	return (read_word_2c(0x3f) / 16384.0)

def print_accel():
	print("x: ", "{0:.4f}".format(get_accel_xout()), " | ",
	      "y: ", "{0:.4f}".format(get_accel_yout()), " | ",
		  "z: ", "{0:.4f}".format(get_accel_zout()), " | ")

''' X,Y,Z Gyroscope Output Functions ---------------------------------------------------- '''
def get_gyro_xout():
	return (read_word_2c(0x43) / 131)

def get_gyro_yout():
	return (read_word_2c(0x45) / 131)

def get_gyro_zout():
	return (read_word_2c(0x47) / 131)

def print_gyro():
	return("{0:.4f}".format(get_gyro_xout()), "|",
	       "{0:.4f}".format(get_gyro_yout()), "|",
		   "{0:.4f}".format(get_gyro_zout()), "\n")



''' Equations for rotation data '''

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


def get_x_roll():
    radians = math.atan2(get_accel_xout(),
                         get_accel_zout())

    return math.degrees(radians)

def get_y_roll():
    radians = math.atan2(get_accel_yout(),
                         get_accel_zout())

    return math.degrees(radians)

# Green dot points up towards head
def get_sleep_position():
    x_roll = get_x_roll() # Get current roll angle

    # Run scenarios to determine position
    if  -45 < x_roll < 45: # Back
        return ('{0:.4f}'.format(x_roll) + '|Back')
    elif 45 <= x_roll <= 135: # Left Side
        return ('{0:.4f}'.format(x_roll) + '|Left Side')
    elif -135 <= x_roll <= -45: # Right Side
        return ('{0:.4f}'.format(x_roll) + '|Right Side')
    else: # Back
        return ('{0:.4f}'.format(x_roll) + '|Stomach')



''' Roll = atan2(Y, Z) * 180/PI; '''
''' Pitch = atan2(X, sqrt(Y*Y + Z*Z)) * 180/PI; '''

''' Print the rotation data '''
def print_x_rotation():
    temp = get_x_rotation(get_accel_xout(), 
                          get_accel_yout(), 
                          get_accel_zout())

    return '{0:.4f}'.format(temp)

def print_y_rotation():
    temp = get_y_rotation(get_accel_xout(), 
                          get_accel_yout(), 
                          get_accel_zout())

    return ''.join('{0:.4f}'.format(temp))

def print_rotation():
    return print_x_rotation(), "|", print_y_rotation()

'''
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
'''

'''
	Begin the initialization of the accelerometer and set up variables
'''

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

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

#note that for the data, the VCC is in the upper left corner for al of these
def write_data_to_file():
	filename = "45Down.txt"
	with open(filename,"w") as datafile:
		temp_datapoints = 1000
		temp_counter =0
		datafile.write("comment")
		datafile.write(',')
		datafile.write("45 degrees Down")
		datafile.write('\n')
		datafile.write("gyro_xout")
		datafile.write(',')
		datafile.write("gyro_yout")
		datafile.write(',')
		datafile.write("gyro_zout")
		datafile.write(',')		
		datafile.write("accel_xout")
		datafile.write(',')
		datafile.write("accel_yout")
		datafile.write(',')
		datafile.write("accel_zout")
		datafile.write('\n')
		while temp_counter<temp_datapoints:
			temp_counter += 1
			time.sleep(0.05)
			datafile.write("{0:.4f}".format(get_gyro_xout()))
			datafile.write(',')
			datafile.write("{0:.4f}".format(get_gyro_yout()))
			datafile.write(',')
			datafile.write("{0:.4f}".format(get_gyro_zout()))
			datafile.write(',')
			datafile.write("{0:.4f}".format(get_accel_xout()))
			datafile.write(',')
			datafile.write("{0:.4f}".format(get_accel_yout()))
			datafile.write(',')
			datafile.write("{0:.4f}".format(get_accel_zout()))
			datafile.write('\n')
		

		
	
	
#initializing imu stuff needed in order to have the bus system work
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)



def run_imu():
	
	write_data_to_file()
	
	# while True:
		# time.sleep(0.1)
		# gyro_xout = read_word_2c(0x43)
		# gyro_yout = read_word_2c(0x45)
		# gyro_zout = read_word_2c(0x47)

		# print "gyro_xout : ", gyro_xout, " scaled: ", (gyro_xout / 131)
		# print "gyro_yout : ", gyro_yout, " scaled: ", (gyro_yout / 131)
		# print "gyro_zout : ", gyro_zout, " scaled: ", (gyro_zout / 131)

		# accel_xout = read_word_2c(0x3b)
		# accel_yout = read_word_2c(0x3d)
		# accel_zout = read_word_2c(0x3f)

		# accel_xout_scaled = accel_xout / 16384.0
		# accel_yout_scaled = accel_yout / 16384.0
		# accel_zout_scaled = accel_zout / 16384.0

		# print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
		# print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
		# print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

		# print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		# print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)


© 2018 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About
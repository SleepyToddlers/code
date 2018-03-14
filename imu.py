'''
    This is a library to control the IMU. this will take an 
    IMU, and then output the sleeping position of the patient.

    Dependent upon the following libraries
        1. smbus
        2. math

    Roll = atan2(Y, Z) * 180/PI;
    Pitch = atan2(X, sqrt(Y*Y + Z*Z)) * 180/PI; 
'''
# Dependencies
import smbus
import math



# The driver of the imu object
class IMU(object):

	# Initialize the class
	def __init__(self):
		#initializing imu stuff needed in order to have the bus system work
		# Power management registers
		power_mgmt_1 = 0x6b
		power_mgmt_2 = 0x6c

		bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
		address = 0x68       # This is the address value read via the i2cdetect command

		# Now wake the 6050 up as it starts in sleep mode
		bus.write_byte_data(address, power_mgmt_1, 0)

		current_sleep_position = ''
		
	# return the sleep position of the patient
	@property
	def sleep_position(self):
		x_roll = self.get_x_roll() # Get current roll angle

		# Run scenarios to determine position
		if  -45 < x_roll < 45: # Back
			return ('{0:.4f}'.format(x_roll) + ',Back')
		elif 45 <= x_roll <= 135: # Left Side
			return ('{0:.4f}'.format(x_roll) + ',LeftSide')
		elif -135 <= x_roll <= -45: # Right Side
			return ('{0:.4f}'.format(x_roll) + ',RightSide')
		else: # Back
			return ('{0:.4f}'.format(x_roll) + ',Stomach')

	def get_x_roll(self):
		radians = math.atan2(self.get_accel_xout(),
							self.get_accel_zout())

		return math.degrees(radians)

	def get_accel_xout(self):
		return (self.read_word_2c(0x3b) / 16384.0)

	def get_accel_zout(self):
		return (self.read_word_2c(0x3f) / 16384.0)

		''' Reading / Setup Functions --------------------------------- '''
	def read_byte(self, adr):
		return bus.read_byte_data(address, adr)

	def read_word(self, adr):
		high = bus.read_byte_data(address, adr)
		low = bus.read_byte_data(address, adr+1)
		val = (high << 8) + low
		return val

	def read_word_2c(self, adr):
		val = self.read_word(adr)
		if (val >= 0x8000):
			return -((65535 - val) + 1)
		else:
			return val

	def dist(a,b):
		return math.sqrt((a*a)+(b*b))
''' ------------------------------------------------------------ '''

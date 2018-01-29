from __future__ import division
import max30100
from collections import deque
import time

#getting IR RMS values
def get_IR_RMS():
	return get_RMS(ir_readings)-get_IR_DC()
#	return get_RMS([x-get_IR_DC() for x in ir_readings])

#getting red RMS values
def get_red_RMS():
	return get_RMS(red_readings)-get_red_DC()
#	return get_RMS([x-get_red_DC() for x in red_readings])

#finding RMS values
def get_RMS(l):
	return (sum(squared_list(l),0.0)/len(l))**(0.5)

def squared_list(l):
	return [x**2 for x in l]

#Finding the DC values
def get_IR_DC():
	return avg(dc_ir_readings)

#finding the DC values
def get_red_DC():
	return avg(dc_red_readings)
#finding the DC values
def clear_deques():
	ir_readings.clear()
	red_readings.clear()

#finding the average of a deque
def avg(l):
	return sum(l,0.0)/len(l)
#statement to find the heart rate
def get_heart_rate():
	return heart_rate

#get the current SpO2 Value
def get_spo2():
	return SpO2
	
#to ensure that rising and falling doesn't affect it, make sure that the previous value is lower.
#to find period between heartbeats, find a threshold value in which a heartbeat occurs
#if it hits that threshold value, measure the datapoints since it last hit that threshold value
# that is the period
#once it hits that period, take the readings since it last hit that threshold and find RMS value


def write_data_to_file():
	#with open(filename,"a+") as datafile:
	#	datafile.write("{0:.4f}".format(get_spo2()))
	#	datafile.write(',')
	#	datafile.write("{0:.4f}".format(get_heart_rate()))
	#	datafile.write(',')
	#	datafile.write("{0:.4f}".format(current_IR_read))
	#	datafile.write(',')
	#	datafile.write("{0:.4f}".format(get_IR_DC()))
	#	datafile.write(',')
	#	datafile.write("{0:.4f}".format(get_IR_RMS()))
	#	datafile.write(',')
	#	datafile.write("{0:.4f}".format(get_red_DC()))
	#	datafile.write(',')
	#	datafile.write("{0:.4f}".format(get_red_RMS()))
	#	datafile.write('\n')
	print("{0:.4f}".format(get_spo2()))
	#print("{0:.4f}".format(current_IR_read-get_IR_DC()))
	#print("{0:.4f}".format(current_red_read - get_red_DC()))


buffer_size = 400
mx30 = max30100.MAX30100()
mx30.enable_spo2()
ir_readings = deque([0.0],maxlen = buffer_size)
red_readings = deque([0.0],maxlen = buffer_size)

dc_buffer_size = 10
dc_ir_readings = deque([0.0],maxlen = dc_buffer_size)
dc_red_readings =deque([0.0],maxlen = dc_buffer_size)

current_IR_read =1
last_IR_read = 1

last_red_read = 0
current_red_read = 0

heart_rate = 0
old_SpO2 =0
SpO2=0
last_heart_beat_time = time.clock()
current_heart_beat_time = time.clock()

heart_rate_threshold = 8000.0

magic_number = 0

#opening file for future writes

filename = "PulseOxMod.txt"
with open(filename,'w+') as datafile:
	datafile.write("spo2")
	datafile.write(',')
	datafile.write("heartrate")
	datafile.write('\n')
	

while True:
	mx30.read_sensor()
	current_IR_read = mx30.ir - magic_number
	current_red_read = mx30.red - magic_number
	
	#append readings to the array
	if current_IR_read != None and current_red_read != None:
		ir_readings.append(current_IR_read)
		red_readings.append(current_red_read)
		dc_red_readings.append(current_red_read)
		dc_ir_readings.append(current_IR_read)
	
	#if a heartbeat is detected
	if current_IR_read > heart_rate_threshold and  last_red_read < current_red_read and last_IR_read < current_IR_read:
		#change the heart rate
		last_heart_beat_time = current_heart_beat_time
		current_heart_beat_time = time.clock()
		heart_beat_period = current_heart_beat_time-last_heart_beat_time
		detected_heart_rate = 60.0/heart_beat_period
		#set the heart rate to be the average of the two.
		heart_rate = (heart_rate+detected_heart_rate) / 2.0
		
	#consider putting this into the "heartbeat detected" if statement
	#R = (ACrms of Red / DC of Red) / (ACrms of IR / DC of IR)
	#%SpO2 = 110-25*R
	
	try:
		R = (get_red_RMS() / get_red_DC())/(get_IR_RMS() / get_IR_DC())
	except ZeroDivisionError:
		R = 0
		pass
	old_SpO2 = SpO2
	#setting the new SpO2 value to be the average of the two.
	#SpO2 = (old_SpO2+(110.0-25.0*R))/2.0
	SpO2 = (old_SpO2+(105-16*R))/2
	write_data_to_file()
	
	last_IR_read = current_IR_read
	last_red_read = current_red_read
	
	
	
	

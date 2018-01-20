import max30100

mx30 = max30100.MAX30100()
mx30.enable_spo2()

while True
	mx30.read_sensor()
	tempIR = mx30.ir
	tempred = mx30.red
	#do some calculations here

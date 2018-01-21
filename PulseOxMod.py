import max30100

mx30 = max30100.MAX30100()
mx30.enable_spo2()

while True
	mx30.read_sensor()
	tempIR = mx30.ir
	tempred = mx30.red
	#do some calculations here
	#find the AC RMS of the IR
	#find the AC RMS of the Red
	#find DC of Red
	#find DC of IR
	#R = (ACrms of Red / DC of Red) / (ACrms of IR / DC of IR)
	#%SpO2 = 110-25*R
	
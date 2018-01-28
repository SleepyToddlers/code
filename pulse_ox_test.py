# Imports
import math
import max30100
import time

# Set up the pulse ox
mx = max30100.MAX30100()

# Turn on
mx.enable_spo2()

# Variables for buffer
red = []
ir = []
DC_RED = 0
AC_RED = 0
DC_IR  = 0
AC_IR  = 0

# Start reading
for i in range(0, 100):
    mx.read_sensor()

# Wait time to get rid of first part

# First loop for amount of times
for i in range(0, 1000):
    red.clear()
    ir.clear()

    # To dictate list size
    for j in range(0, 600):
        # Read the sensor
        mx.read_sensor()

        # Store the value
        red.append(mx.red)
        ir.append(mx.ir)

    # Calculate SPO2
    DC_RED = sum(red)/float(len(red))
    AC_RED = math.sqrt(sum([i**2 for i in red])/float(len(red)))
    DC_IR  = sum(ir)/float(len(ir))
    AC_IR  = math.sqrt(sum([i**2 for i in ir])/float(len(ir)))

    SPO2 = 110 - 25*math.log10((AC_RED + DC_RED)/DC_RED) / math.log10((AC_IR+DC_IR)/DC_IR)

    print(SPO2)
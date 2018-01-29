# Imports
import math
import max30100
import time
from collections import deque

# Set up the pulse ox
mx = max30100.MAX30100()

# Turn on
mx.enable_spo2()

mx.set_led_current(led_current_red=4.4, led_current_ir=50.0)
mx.max_buffer_len = 5000

# Variables for buffer
red = []
ir = []
DC_RED = 0
AC_RED = 0
DC_IR  = 0
AC_IR  = 0
ALPHA = 0.95

w_r_1 = []
w_r_0 = []
w_i_1 = []
w_i_0 = []

# File for debugging
file = open('pulse_ox_debug.txt', 'w')

# Que
ir_filter  = deque([0.0],maxlen = 500)
red_filter = deque([0.0],maxlen = 500)

# First loop for amount of times
while True:
    mx.read_sensor() # Read the value

    # Begin the calculations
    if len(mx.buffer_red) == 1:
        # Do nothing
        pass
    elif len(mx.buffer_red) == 2: # Get first w
        # Remove the dc offset
        #ir_filter.append(mx.buffer_ir[-1] + ALPHA*mx.buffer_ir[-2])
        #red_filter.append(mx.buffer_red[-1] + ALPHA*mx.buffer_red[-2])

        # Set up w_0
        w_r_0.append(mx.buffer_red[1] + ALPHA*mx.buffer_red[0])
        w_i_0.append(mx.buffer_ir[1] + ALPHA*mx.buffer_ir[0])

        # Write to file
        file.write(str(mx.red) + ',' + str(mx.ir) + ',' + str(red_filter[-1]) + ',' + str(ir_filter[-1]) + '\n')
    elif len(mx.buffer_red) > 2:
        w_r_0.append(mx.buffer_red[-1] + ALPHA*w_r_0[-1])
        w_i_0.append(mx.buffer_ir[-1] + ALPHA*w_i_0[-1])

        red_filter.append(w_r_0[-1] - w_r_0[-2])
        ir_filter.append(w_i_0[-1] - w_i_0[-2])

        #w_r_0 = red_filter[-1]
        #w_i_0 = ir_filter[-1]

        #w_r_1 = mx.buffer_red[-1] + ALPHA*w_r_0
        #w_i_1 = mx.buffer_ir[-1]  + ALPHA*w_i_0
        
        # Calculate the new voltage
        #ir_filter.append(w_i_1-w_i_0)
        #red_filter.append(w_r_1-w_r_0)

        # Write to file
        file.write(str(mx.red) + ',' + str(mx.ir) + ',' + str(red_filter[-1]) + ',' + str(ir_filter[-1]) + '\n')

    # Now see if calibration is done
    if len(red_filter) > 400:
        # Make calculations
        AC_RED = math.sqrt(sum([i**2 for i in red_filter])/len(red_filter))
        AC_IR  = math.sqrt(sum([i**2 for i in ir_filter])/len(ir_filter))

        SPO2 = 110 - 25*math.log10(AC_RED)/math.log10(AC_IR)

        print('{0:.0f}'.format(SPO2))
    else:
        pass
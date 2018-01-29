# Imports
import math
import max30100
import time

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

w_r_1 = 0.0
w_r_0 = 0.0
w_i_1 = 0.0
w_i_0 = 0.0

# Que
ir_filter  = deque([0.0],maxlen = 1000)
red_filter = deque([0.0],maxlen = 1000)

# First loop for amount of times
while True:
    mx.read_sensor() # Read the value

    # Begin the calculations
    if len(mx.buffer_red) = 0
        # Do nothing
    elif len(mx.buffer_red) = 1: # Do stuff
        # Remove the dc offset
        ir_filter.append(mx.buffer_ir[-1] + ALPHA*mx_buffer_ir[-2])
        red_filter.append(mx.buffer_red[-1] + ALPHA*mx_buffer_red[-2])
    else:
        w_r_0 = red_filter[-1]
        w_i_0 = ir_filter[-1]

        # Calculate the new voltage
        ir_filter.append((mx.buffer_ir[-1] + ALPHA*mx_buffer_ir[-2])-w_i_0)
        red_filter.append((mx.buffer_red[-1] + ALPHA*mx_buffer_red[-2])-w_r_0)

    # Now see if calibration is done
    if len(red_filter) > 500
        # Make calculations
        AC_RED = math.sqrt(sum([i**2 for in red_filter]/len(red_filter)))
        AC_IR  = math.sqrt(sum([i**2 for in ir_filter]/len(ir_filter)))

        SPO2 = 110 - 25*math.log10(AC_RED)/math.log10(AC_IR)

        print(SPO2)
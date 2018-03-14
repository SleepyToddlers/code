# Libraries
from adc import ADC# Gives 4 channels of inputs
import imu # Accelerometer
#import filters # Digital filters for data
from collections import deque # To contain the data
import time

# Two cases here, first to test connnections
# Second to run program
# Worry about test case later

# Time Variable
TEST_DURATION = 1 # In hours

# Variables
sleep_position = deque()
nas_temp       = deque()
belt           = deque()
hr             = deque()
mic            = deque()
adc = ADC()

# Set up a deque to determine when to filter
start_time = time.time()
end_time = start_time * 60 * TEST_DURATION

# Open the file
file = open('ted_shirt_verification.txt', 'w')

# Write the time
file.write(str(start_time))

# Get the data
while(time.time() < end_time):
    for i in range(0,5000):
        a,b,c,d = adc.read_data()
        hr.append(str(a))
        nas_temp.append(str(b))
        belt.append(str(c))
        mic.append(str(d))
        sleep_position.append(str(imu.sleep_position()))


file.write(str(time.time() - start_time))

# Write to the file
for i in range(0, len(hr)):
    file.write(hr[i] + ',' + nas_temp[i] + ',' + belt[i] + ',' + mic[i] + ',' + sleep_position[i] + '\n')

file.write(str(time.time() - start_time))
file.close()

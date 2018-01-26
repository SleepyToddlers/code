import Adafruit_ADS1x15

# Variable for sampling, says 128 sps
# For one min of data 128samples / 1 sec * 60 sec / 1 min 
MINUTES_TO_RECORD = 1
SAMPLES_PER_SECOND = 128

# Set up the sensors
adc_48 = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1) # belt and temp
adc_49 = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1) # snore and ekg

# Open the file
file = open('integration_testing.txt', 'w')

# Write to the file with the data
for i in range(0, MINUTES_TO_RECORD*SAMPLES_PER_SECOND*60):
    # Get sensor data
    belt = str(adc_48.read_adc_difference(0, gain=4))
    temp = str(adc_48.read_adc_difference(3, gain=4))
    snor = str(adc_49.read_adc(3, gain=1))

    # format output
    output = belt + ',' + temp + ',' + snor + '\n'
    file.write(output)

file.close()
print('All done')
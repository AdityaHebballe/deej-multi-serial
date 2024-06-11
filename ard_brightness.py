import serial
import tinytuya
import time

# Set up TinyTuya device
d = tinytuya.BulbDevice(
    dev_id='device id',
    address='device ip',  
    local_key='device key', 
    version=3.5 
)

ser = serial.Serial('/dev/pts/5', 9600) # edit serial port as required

def set_brightness(value):
    # Map the Arduino value (0-1023) to brightness percentage (0-100)
    brightness = int(value * 100 / 1023)
    d.set_brightness_percentage(brightness, 'nowait')

previous_a3_value = -1  # Initialize with an invalid value to ensure the first read triggers an update
threshold = 20           # Set a threshold for significant changes

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            values = line.split('|')
            
            if len(values) >= 4:
                a3_value = int(values[3])  # Read the value from the fourth potentiometer (A3)
                
                # Check if the value has changed significantly
                if abs(a3_value - previous_a3_value) > threshold:
                    set_brightness(a3_value)
                    previous_a3_value = a3_value
                    print(f"Brightness set to {a3_value * 100 / 1023:.2f}%")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

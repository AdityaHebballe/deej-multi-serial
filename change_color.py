import serial
import tinytuya
import time
import subprocess  # For running system commands to simulate play/pause

# Set up TinyTuya device
d = tinytuya.BulbDevice(
    dev_id='d7350bb8dec86d4cacv92v',
    address='192.168.1.156',  # Or set to 'Auto' to auto-discover IP address
    local_key='uyKos]3O_%N+ps{e', 
    version=3.5
)
d.set_retry(retry=True)
#d.set_socketPersistent(True)
data = d.status()
print('Dictionary %r' % data)

# Set up serial connection
ser = serial.Serial('/dev/ttyS0fake0', 9600)  # Replace '/dev/pts/5' with your Arduino serial port

def set_brightness(value):
    # Map the Arduino value (0-1023) to brightness percentage (0-100)
    brightness = int(value * 100 / 1023)
    d.set_brightness_percentage(brightness, 'nowait')

previous_a3_value = -1  # Initialize with an invalid value to ensure the first read triggers an update
threshold = 20        # Set a threshold for significant changes

# Initialize button press state
previous_button_state1 = -1  # Initialize with an invalid state to ensure the first read triggers a toggle for mode button
previous_button_state2 = -1  # Initialize with an invalid state to ensure the first read triggers a toggle for play/pause button
current_mode = 'colour'  # Initial mode is 'colour'

def toggle_play_pause():
    subprocess.call(["xdotool", "keydown", "XF86AudioPlay"])  # Press play/pause key
    time.sleep(0.1)  # Give some time for the key press to register
    subprocess.call(["xdotool", "keyup", "XF86AudioPlay"])  # Release play/pause key

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            values = line.split('|')
            
            if len(values) >= 6:
                a3_value = int(values[3])  # Read the value from the fourth potentiometer (A3)
                button_state1 = int(values[4])  # Read the mode toggle button state (assumed to be in the fifth position)
                button_state2 = int(values[5])  # Read the play/pause button state (assumed to be in the sixth position)

                # Check if the value has changed significantly
                if abs(a3_value - previous_a3_value) > threshold:
                    set_brightness(a3_value)
                    previous_a3_value = a3_value
                    print(f"Brightness set to {a3_value * 100 / 1023:.2f}%")

                # Check for any change in button state to toggle mode
                if button_state1 != previous_button_state1:
                    if current_mode == 'colour':
                        current_mode = 'white'
                        d.set_mode('white', 'nowait')
                        set_brightness(a3_value)
                        print("Mode set to white")
                    else:
                        current_mode = 'colour'
                        d.set_mode('colour', 'nowait')
                        set_brightness(a3_value)
                        print("Mode set to colour")
                previous_button_state1 = button_state1

                # Check for play/pause button press
                if button_state2 != previous_button_state2:
                    toggle_play_pause()
                    print("Toggled play/pause")
                previous_button_state2 = button_state2

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

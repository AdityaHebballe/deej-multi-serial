#!/bin/bash

# Get the list of ttyUSB devices
TTY_DEVICES=$(ls /dev/ttyUSB* 2>/dev/null)

# Check if any ttyUSB devices are found
if [ -z "$TTY_DEVICES" ]; then
    echo "No ttyUSB devices found in /dev"
    exit 1
fi

# Get the single available ttyUSB device
REAL_TTY=$TTY_DEVICES

MUX_PATH="/tmp/ttyS0mux"

echo "Setting up multiplexer for $REAL_TTY..."

# Start the tty bus
tty_bus -s $MUX_PATH &
sleep 1

# Attach the real TTY to the multiplexer
tty_attach -s $MUX_PATH $REAL_TTY &
sleep 1

# Create fake TTY devices
tty_fake -s $MUX_PATH /dev/ttyS0fake0 &
tty_fake -s $MUX_PATH /dev/ttyS0fake1 &
sleep 1

echo "Multiplexer setup complete."
echo "Real TTY: $REAL_TTY"
echo "Fake TTYs: /dev/ttyS0fake0, /dev/ttyS0fake1"

wait

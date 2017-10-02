#!/bin/bash
#

echo "Restart USB video capture device"
echo '1-2' |sudo tee /sys/bus/usb/drivers/usb/unbind
sleep 5
echo '1-2' |sudo tee /sys/bus/usb/drivers/usb/bind

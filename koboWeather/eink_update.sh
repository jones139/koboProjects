#!/bin/sh
# Updates e-ink display
dd if=/dev/fb0 of=/tmp/fb
cat /tmp/fb | /usr/local/Kobo/pickel showpic
/usr/local/Kobo/pickel blinkoff

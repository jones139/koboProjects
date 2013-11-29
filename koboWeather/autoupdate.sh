#!/bin/sh
echo "Creating cron directory"
mkdir -p /var/spool/cron/crontabs
echo "Copying crontab file"
cp /mnt/onboard/.apps/koboWeather/cron /var/spool/cron/crontabs/root
if [ ! "$(pidof crond)" ]
then
    echo "Starting crond"
    crond &
else
    echo "crond is already running"
fi
echo ""
echo "The weather forecast will now update every hour (until you turn off or reboot the device)."

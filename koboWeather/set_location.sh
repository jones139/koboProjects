#!/bin/sh
echo ""
echo "For the weather forecast to work, please enter your latitude and longitude."
echo "There is an easy to use map at http://stereopsis.com/flux/map.html"
echo ""
read -p "Enter your latitude: " lat
read -p "Enter your longitude: " lon
echo $lat > /mnt/onboard/.apps/koboWeather/location
echo $lon >> /mnt/onboard/.apps/koboWeather/location

#!/bin/sh

for i in *.svg; do
echo "i="$i
basefilename=`basename $i .svg`
echo $basefilename
convert -size 24x24 $basefilename.svg $basefilename.png
#ffmpeg -i "$i" \
#-vf transpose=2 -f rawvideo -pix_fmt rgb565 -s 600x800 -y "$output" < /dev/null


done
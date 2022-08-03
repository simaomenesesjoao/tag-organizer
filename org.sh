#!/bin/bash

dir=/home/simao/builds/organizer/
aw=$(xdotool getactivewindow)
pid=$(xdotool getwindowpid $aw)
wdir=$(grep -z "\bPWD" /proc/$pid/environ)
wdir2=$(echo ${wdir:4}/)
echo win:$aw > $dir/log.dat
echo pid:$pid >> $dir/log.dat
echo wdir:$wdir >> $dir/log.dat
echo wdir2:$wdir2 >> $dir/log.dat

a=$(cat -v /proc/$pid/cmdline | awk -F@  '{print $2}')
b=$(echo ${a:0:-1})
filename=${wdir2}${b}
echo filename:$filename >> $dir/log.dat

str=$(python $dir/tagger.py $filename)
echo str:$str >> $dir/log.dat

c=$(/usr/bin/python /home/simao/builds/organizer/tag.py -a $filename $str)
echo pytag:$c >> $dir/log.dat


#!/bin/bash
# Just copy a bunch of stuff to an esp board

if [ -z $1 ]; then
	echo "Usage: ./deploy.sh [PORT]"
	exit 1
fi

for FILE in `ls *.py`; do
	ampy --port $1 put $FILE
	if [ $? == 0 ]; then
		echo "Put $FILE"
	else
		exit $?
	fi
done

if [ -z `ampy --port $1 ls | grep uosc -` ]; then
	ampy --port $1 mkdir uosc
	if [ $? == 0 ]; then
		echo "Made uosc dir"
	else
		exit $?
	fi
fi

for FILE in `ls uosc/*.py`; do
	ampy --port $1 put $FILE $FILE
	if [ $? == 0 ]; then
		echo "Put $FILE"
	else
		exit $1
	fi
done

if [ -f "config" ]; then
	ampy --port $1 put config
else
	echo "No config found, hopefully you know what you're doing."
fi
ampy --port $1 reset
echo "Put config, rebooting..."

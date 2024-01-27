#!/bin/sh

BIOMES="plains forest desert savanna"
BIOM
BIOME=$(echo "$BIOMES" | tr " " "\n" | dmenu -p "biome: ")
if [ -z "$BIOME" ]; then
	echo "No biome selected!"
	exit 1
fi

DELAY="50"

LOOP="true"
while [ -n "$LOOP" ]; do
	xdotool mousedown 1
	sleep 0.05

	xdotool key t
	sleep 0.05
	xdotool type --delay="$DELAY" "//chunk"
	sleep 0.05
	xdotool key Return
	sleep 0.1

	xdotool key t
	sleep 0.05
	xdotool type --delay="$DELAY" "//contract 100 down"
	sleep 0.05
	xdotool key Return
	sleep 0.1

	xdotool key t
	sleep 0.05
	xdotool type --delay="$DELAY" "//copy"
	sleep 0.05
	xdotool key Return
	sleep 0.1

	xdotool key t
	sleep 0.05
	xdotool type --delay="$DELAY" "//schem save $BIOME-$(date --iso-8601=seconds | tr ":" "_" | cut -f 1 -d "+")"
	sleep 0.05
	xdotool key Return
	sleep 0.1

	xdotool key t
	sleep 0.05
	xdotool type --delay="$DELAY" "//deselect"
	sleep 0.05
	xdotool key Return
	sleep 0.1

	xdotool key t
	sleep 0.05
	xdotool type --delay="$DELAY" "/tp chronoyan ^ ^ ^16"
	sleep 0.05
	xdotool key Return
	sleep 0.1

	LOOP=$(echo "continue stop" | tr " " "\n" | dmenu -p "biome: " | sed 's/stop*//g')
done

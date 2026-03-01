#!/usr/bin/bash

MIDI=$1

midicsv $MIDI > step0.out

/usr/bin/python3 utils/csvencode.py step0.out

/usr/bin/python3 utils/encode.py step1.out

mv step2.out $MIDI.enc
rm step0.out step1.out

echo "encoded file produced: $MIDI.enc"

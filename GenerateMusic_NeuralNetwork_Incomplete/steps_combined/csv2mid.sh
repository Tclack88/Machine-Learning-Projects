#!/usr/bin/bash

if [ "$#" -ne 2 ]
	then
	echo USAGE: $0 INFILE OUTFILE
	exit 1
fi

INFILE=$1
OUTFILE=$2

/usr/bin/python3 utils/correct_output.py $INFILE

/usr/bin/python3 utils/decode.py $INFILE

/usr/bin/python3 utils/decodetocsv.py step3.out

mv step4.out $INFILE.dec
rm step3.out converted

csvmidi $INFILE.dec > $OUTFILE && rm $INFILE.dec && echo "midi file produced: $OUTFILE"

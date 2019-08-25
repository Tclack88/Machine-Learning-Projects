# Generate Music with Neural Network (Incomplete)

See blog post about the subject [here]("https://tclack88.github.io/blog/code,/personal/2019/08/15/music-generation-fail.html")

## step 1:

midicsv a bunch of files
`for f in $(ls *.mid); do midicsv $f $f.out; done`

## step 2:

"csvencode.py" all the files (it calls cleaner.sh in the procoess)

`for f in $(ls *.csv); do csvencode.py $f; done`

"encode.py" all the files
`for f in $(ls *.out); do encode.py $f; done`

## step 3:

Combine all files:

`cat *.enc > master_songs.enc`

## step 4:
make model and generate music!

WORK IN PROGRESS

## step 5:
decode generated music

`decode.py generated_music.enc`

## step 6:
return to csv

`decodetocsv.py decoded_music`

## step 7
csv to midi

`csvmidi decoded_music.csv decoded_music.mid`

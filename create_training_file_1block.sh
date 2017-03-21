#!/bin/bash

#./create_file.sh <frames_folder> <metrics_folder> <csvfile_name>
EXTENSION=""
BLOCK_MOVEMENT=yes
N_BLOCKS=3

FRAMES_ROUTE="$HOME/Projects/Images/$1"
METRICS_ROUTE="$HOME/Projects/Images/$2"
FRAMES_FOLDER="/frame$EXTENSION"
METRICS_FOLDER="/metricasframe$EXTENSION"

echo 'Frames route is '$FRAMES_ROUTE' '
echo 'Metrics route is '$METRICS_ROUTE' '

echo 'Creating file '$3' '

x=1
while [ $x -le $N_BLOCKS ]
do
  python3 CrearFicheroEntrenamiento1bloque.py $FRAMES_ROUTE $METRICS_ROUTE $3_$x $x $FRAMES_FOLDER $METRICS_FOLDER $BLOCK_MOVEMENT
  let x=x+1
done

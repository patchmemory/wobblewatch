#!/bin/bash

i=0
for file in S???/D*.txt
do 
    let i=$i+1
    echo $i $file
    ofile="`echo $file | cut -d '.' -f 1`.pkl"
    if [ -f "$ofile" ]
    then
        echo
        echo "Found dictionary file: "
        echo "    $ofile" 
        echo "Moving on..."
        echo
    else 
        echo 
        python3 ../../code/TimeWindowLabel.py $file nofall
        echo 
    fi
done

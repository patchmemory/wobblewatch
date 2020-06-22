#!/bin/bash

for item in `cat remove.list`
do 
    rm -v $item
done
rm remove.list
touch remove.list

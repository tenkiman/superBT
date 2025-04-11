#!/bin/bash -i

rsync -alv --exclude SAV --exclude='robots*' --exclude 'index*' --exclude "*Ops*" --exclude "*Neum*" /w21/dat/tc/names/ /sbt/superBT-V04/dat-v03/tc/names/


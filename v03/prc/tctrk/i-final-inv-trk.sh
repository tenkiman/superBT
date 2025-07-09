#!/bin/bash -i

sfile="inv/trk/inv-trk-$1-$2-stdout-log.txt"
efile="inv/trk/inv-trk-$1-$2-stderr-log.txt"

if [ -e $sfile ]; then
    echo "$sfile  exists -- delete"
    rm -i $sfile
else
    echo "$sfile does not exist."
fi
if [ -e $efile ]; then
    echo "$efile  exists -- delete"
    rm -i $efile
else
    echo "$efile does not exist."
fi

cmd="a-inv-tmtrk.py  -Y $1-$2  > >(tee -a $sfile) 2> >(tee -a $efile  >&2)"
echo $cmd
eval "$cmd"


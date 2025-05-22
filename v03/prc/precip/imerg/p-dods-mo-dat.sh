#!/bin/bash -i

tdir=/data/w22/dat/pr/imerg/cmorph_grid/monthly
yyyymm=202412

gcmd="grads -lbc"
#cmd="$gcmd \""run p-dods-mo-dat.gs $tdir 202412"\""
cmd="$gcmd \"run p-dods-mo-dat.gs $tdir $yyyymm\""
echo $cmd
$cmd

exit;

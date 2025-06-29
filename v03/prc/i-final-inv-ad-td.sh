#!/bin/bash -i

cmd="i-all-sbt-ad-tc.py -Y $1.$2 > >(tee -a inv-ad-td-$1-$2-stdout.log) 2> >(tee -a inv-ad-td-$1-$2-stderr.log >&2)"
echo $cmd
eval "$cmd"


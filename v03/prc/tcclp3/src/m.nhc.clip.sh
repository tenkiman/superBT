#!/bin/sh

gfortran -fallow-argument-mismatch -ffixed-line-length-132 nhc.clipper.f -o nhc.clipper.x

#g95 nhc.clipper.f dataio.f upcase.f -o nhc.clipper.x

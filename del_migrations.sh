#!/bin/sh

for d in * ;
do
  [ -d ${d}/migrations ] && rm -rf ${d}/migrations
done

#
# User Projection Degree. G(671, 197780). 429 (0,6393) nodes with in-deg > avg deg (589,5), 0 (0,0000) with >2*avg.deg (Mon Sep 27 05:24:26 2021)
#

set title "User Projection Degree. G(671, 197780). 429 (0,6393) nodes with in-deg > avg deg (589,5), 0 (0,0000) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'inDeg.UserProjectionDegree.png'
plot 	"inDeg.UserProjectionDegree.tab" using 1:2 title "" with linespoints pt 6

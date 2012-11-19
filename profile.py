#!/usr/bin/env python

import cProfile
import pstats

from polycomp import (
    compress,
    decompress,
)


with open("cross_country.txt") as f:
    cross_country_poly = f.read().rstrip()

print("Length of cross-country polyline: {0}".format(len(cross_country_poly)))

#import profile
#pr = profile.Profile()
#for i in range(5):
#    print(pr.calibrate(100000))

cProfile.Profile.bias = 5.00374496255e-06

wow = decompress(cross_country_poly)
print("Number of points: {0}".format(len(wow)))

cProfile.run('decompress(cross_country_poly)', 'prof')
p = pstats.Stats('prof')
p.sort_stats('cumulative').print_stats(10)

bam = compress(wow)

cProfile.run('compress(wow)', 'prof')
p = pstats.Stats('prof')
p.sort_stats('cumulative').print_stats(10)

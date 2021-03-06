#! /usr/bin/env python3

import sys,glob,os
from os import makedirs, path as op
op.dirname(sys.executable)
import gippy
import gippy.algorithms as alg
import shutil

def generate_stats():
    geotifs = [op.join(os.getcwd(), f) for f in os.listdir('.') if f.endswith('.tif')]
    geojsons = [op.join(os.getcwd(), geoj) for geoj in os.listdir('.') if geoj.endswith('.geojson')]
    output_path = op.join(os.getcwd(), 'outputs')
    output_files = []
    if not op.isdir(output_path):
        makedirs(output_path)
    for geotif in geotifs:
        for geojson in geojsons:
            fname = op.splitext(geotif)[0]
            basename = fname.split('/')[-1]
            filename = op.splitext(geojson)[0]
            geo_fname = filename.split('/')[-1]
            date=basename[10:16]
            tile = basename[28:35]
            geoimg = gippy.GeoImage.open([geotif])
            geoimg.set_nodata(0)
            geovec = gippy.GeoVector(geojson)
            res = geoimg.resolution()
            output_filename = '{}_{}_{}.csv'.format(geo_fname, date, tile)
            f = open(output_filename, 'w')
            f.write('min,max,mean,stddev,skew,count\n')
            fout = geoimg.basename() + '_{}.tif'.format(str(geo_fname))
            imgout = alg.cookie_cutter([geoimg], fout, geovec[0], xres=res.x(), yres=res.y(), proj=geoimg.srs())
            stats = imgout[0].stats()
            f.write( ','.join([str(s) for s in stats]) + '\n')
            f.close()
            if output_filename not in output_files:
                output_files.append(output_filename)
            shutil.move(os.path.join('.', fout), os.path.join(output_path, fout))
            print('{} site stats extracted!'.format(geojson))
    return output_files

if __name__ == '__main__':
    generate_stats()

import numpy as np

from ismartcsv import read_file

filename = "./assets/data/rs/GPSRS20190703.CSV"
config_file = "./assets/configurations/rs_config.yaml"

dfile = read_file(filename,config_file)
slice_file = dfile[10:1000:10]
interp_func = slice_file.get_interpolator()
interp_dfile = interp_func(np.arange(0.4,5,0.001))

interp_dfile.plot()
dfile.plot()
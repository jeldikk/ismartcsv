from ismartcsv import read_file, read_folder

filename = "./assets/data/uvw/uvwD20191009T220158.csv"
foldername = "./assets/data/uvw/"
config_file = "./assets/configurations/uvw_config.yaml"

dfile = read_file(filename,config_file)
dfolder = read_folder(foldername, config_file)


# dfile.plot()
# dfolder.plot()
import datetime


from ismartcsv import read_file, read_folder



def datetime_parser(dt_str, fmt):
    print(dt_str)
    return 

def datetime_encoder(dt_obj, fmt):
    pass

def filename_parser(fn_str, fmt):
    pass

def filename_encoder(fn_obj, fmt):
    pass


options = {
    'DATETIME_PARSER': datetime_parser,
    'DATETIME_ENCODER': datetime_encoder,
    'FILENAME_PARSER': filename_parser,
    'FILENAME_ENCODER': filename_encoder
}




config_file = "./assets/configurations/aws_config.yaml"
data_file = "./assets/data/aws/AWS20180401.CSV"
data_folder = "./assets/data/aws/"


dfile = read_file(data_file,config_file)
# dfolder = read_folder(data_folder,config_file)


dfile.plot()
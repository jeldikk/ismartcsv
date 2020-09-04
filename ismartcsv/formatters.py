import datetime

from .utilities import timestamp2str, str2timestamp

class formatter(object):

    def __init__(self):
        pass

    def parse(self, arg):

        if not isinstance(arg,str):
            raise ValueError(f'parse can take only strings, but found {type(arg)}')


    def encode(self, arg):

        if not isinstance(arg, object):
            raise ValueError(f"encode can take an object type")


    @staticmethod
    def make_formatter(ftype,format=None):
        
        if ftype == 'datetime':
            return datetime_formatter(format)

        if ftype == 'filename':
            return filename_formatter(format)
        
        elif ftype in ['float', 'int']:
            return field_formatter(ftype)
        
        else:
            raise ValueError(f"field type {ftype} not found in implementations")


class filename_formatter(formatter):
    
    def __init__(self,format):

        if format == None:
            self.__encfunc = None
            self.__parsefunc = None
        else:
            self.__encfunc = timestamp2str
            self.__parsefunc = str2timestamp

        self.__format = format


    def set_encoder(self,encoder_func):
        self.__encfunc = encoder_func


    def set_parser(self, parser_func):
        self.__parsefunc = parser_func

    
    def parse(self,arg):
        formatter.parse(self,arg)
        return self.__parsefunc(arg,self.__format)

    def encode(self,arg):
        formatter.encode(self,arg)
        return self.__encfunc(arg,self.__format)
         


class datetime_formatter(formatter):

    def __init__(self,format):

        if format == None:
            self.__encfunc = None
            self.__parsefunc = None
        else:
            self.__encfunc = timestamp2str
            self.__parsefunc = str2timestamp

        self.__format = format



    def set_encoder(self, encoder_func):
        self.__encfunc = encoder_func


    def set_parser(self, parser_func):
        self.__parsefunc = parser_func

    def parse(self,arg):
        formatter.parse(self,arg)
        self.__parsefunc(arg,self.__format)

    def encode(self,arg):
        formatter.encode(self,arg)
        self.__encfunc(arg,self.__format)




class field_formatter(formatter):
    
    def __init__(self,format):
        # print(f"field type of {format}")
        self.__format = format


    def parse(self,args):
        
        fmt = self.__format
        if fmt == 'int':
            return int(args)
        elif fmt == 'float':
            return float(args)


    def encode(self,args,decimals = 3):
        
        if isinstance(args,int):
            return int(args)
        elif isinstance(args,float):
            return round(args,decimals)
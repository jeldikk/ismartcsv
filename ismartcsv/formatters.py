"""

@author: jeldikk
"""

import datetime

from .utilities import timestamp2str, str2timestamp

class formatter(object):
    """base class for formatter subclasses

    Args:
        object (python object): Every class should inheret this object parent class
    """
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
        """static factory method call to create concrete subclass instances

        Args:
            ftype (str): field type of field variant(possible: filename, datetime, int, float)
            format (str, optional): filename or datetime format defined by user. Defaults to None.

        Raises:
            ValueError: raises if ftype is not one of ('filename', 'datetime', 'int', 'float')

        Returns:
            formatter: instance of concrete subclass inheriting formatter baseclass
        """
        
        if ftype == 'datetime':
            return datetime_formatter(format)

        if ftype == 'filename':
            return filename_formatter(format)
        
        elif ftype in ['float', 'int']:
            return field_formatter(ftype)
        
        else:
            raise ValueError(f"field type {ftype} not found in implementations")


class filename_formatter(formatter):
    """concrete class of formatter parent class

    Args:
        formatter (formatter): parent class specifying interface to be defined by concrete subclasses
    """
    
    def __init__(self,format):
        """constructor to create a instance of concreate filename_formatter class

        Args:
            format (str): default format defined using filename_format attribute of config_file meta section
        """

        if format == None:
            self.__encfunc = None
            self.__parsefunc = None
        else:
            self.__encfunc = timestamp2str
            self.__parsefunc = str2timestamp

        self.__format = format


    def set_encoder(self,encoder_func):
        """set a customised encoder function which will be called on .encode method call

        Args:
            encoder_func ([function]): This is a two argument function, first argument is the python object and other is the format given in constructor
        """
        self.__encfunc = encoder_func


    def set_parser(self, parser_func):
        """set a customised parser function which will be called on .parse method call

        Args:
            parser_func ([function]): [A two argument function, first arg is the string and other is argument is provided while definig constructor]
        """
        self.__parsefunc = parser_func

    
    def parse(self,arg):
        """parse takes a string and creates a python object using parsefunction defined

        Args:
            arg (str): filename to be parsed to create a python object

        Returns:
            object: creates a python object, most probably a datetime instance useful for storing filestamp property of datafile
        """
        formatter.parse(self,arg)
        return self.__parsefunc(arg,self.__format)

    def encode(self,arg):
        """encodes takes a python object and returns a string using encodefunction defined

        Args:
            arg (object): python object to be passed as argument to encode function defined

        Returns:
            str: returns a formatted string based on encode function set.
        """
        formatter.encode(self,arg)
        return self.__encfunc(arg,self.__format)
         


class datetime_formatter(formatter):
    """concreate class of formatter parent class

    Args:
        formatter (formatter): parent class sepcifying interfaces to be defined by concreate subclasses
    """

    def __init__(self,format):
        """constructor to create an instance of concreate datetime_formatter class

        Args:
            format (str): default format defind using datetime_format attribute of config_file meta section
        """


        # print("datetime_formatter :", format)
        if format == None:
            self.__encfunc = None
            self.__parsefunc = None
        else:
            self.__encfunc = timestamp2str
            self.__parsefunc = str2timestamp

        self.__format = format



    def set_encoder(self, encoder_func):
        """set a customised encoder function which will be called on .encode method call

        Args:
            encoder_func (function): function which takes python object and format as its arguments
        """


        self.__encfunc = encoder_func


    def set_parser(self, parser_func):
        """set a customised parser function which will be called on .parse method call

        Args:
            parser_func (function): function which takes a string and format as its arguments
        """


        self.__parsefunc = parser_func

    def parse(self,arg):
        """parse takes a string and creates a python object using parsefunction defined

        Args:
            arg (str): datetime field string to be parsed to create python object

        Returns:
            object: create a python datetime object
        """


        formatter.parse(self,arg)
        return self.__parsefunc(arg,self.__format)

    def encode(self,arg):
        """encode takes a python object and returns a string using encodefunction defined

        Args:
            arg (object): python object to be passed as argument to encode function defined

        Returns:
            str: returns a formatted string based on encode function set
        """


        formatter.encode(self,arg)
        return self.__encfunc(arg,self.__format)




class field_formatter(formatter):
    """concrete class of formatter parent class

    Args:
        formatter (formatter): parent class specifying interface to be defined by concrete subclasses
    """
    
    def __init__(self,format):
        # print(f"field type of {format}")
        """constructor for handling integer and float field types

        Args:
            format ([type]): [description]
        """
        self.__format = format

    
    def parse(self,args):
        """parse takes a string and creates a python object

        Args:
            args (str): Number string to be parsed to create a python object

        Returns:
            object: python object, most probably an int or float instance
        """
        
        fmt = self.__format
        if fmt == 'int':
            return int(args)
        elif fmt == 'float':
            return float(args)


    def encode(self,args,decimals = 3):
        """encode takes a python object and returns a string for serializing to output stream

        Args:
            args (object): python object to be converted to string
            decimals (int, optional): if field type is float use this to specify number of decimal places to be considered. Defaults to 3.

        Returns:
            object: returns a formatted string based on args given
        """
        
        if isinstance(args,int):
            return f'{int(args)}'
            
        elif isinstance(args,float):
            return f'{round(args,decimals)}'
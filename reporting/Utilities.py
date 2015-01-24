__author__ = 'claesmathias'


import numpy as np


class Utilities():

    @staticmethod
    def set_dictionary_xml(dict, xml_element):
        for key in dict.keys():
                dict[key] = xml_element.find(key).text

    @staticmethod
    def set_dictionary(dict, element):
        for key in dict.keys():
                dict[key] = np.append(dict[key], int(element[key]))
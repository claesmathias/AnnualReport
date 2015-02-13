__author__ = 'claesmathias'


from pylab import *
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

    @staticmethod
    def to_thousand(x, pos):
        'The two args are the value and tick position'
        return '$%1.1fk' % (x)

    @staticmethod
    def to_millions(x, pos):
        'The two args are the value and tick position'
        return '$%1.1fM' % (x*1e-3)

    @staticmethod
    def to_percent(y, position):
        # Ignore the passed in position. This has the effect of scaling the default
        # tick locations.
        s = str(100 * y)

        # The percent symbol needs escaping in latex
        if matplotlib.rcParams['text.usetex'] == True:
            return s + r'$\%$'
        else:
            return s + '%'
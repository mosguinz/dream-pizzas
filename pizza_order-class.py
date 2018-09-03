"""Dream Pizzas ordering console for phone operators."""

import re
import sys
from collections import OrderedDict

# Order specifications
DELIVERY_CHARGE = 3.00
MAX_PIZZA = 5

# String templates
LINE = '-' * 63
DOUBLE_LINE = '=' * 63
EXAMPLES = '\n\nExamples:\n' + ' {}\n' * 3 + ' {}'
ERROR = LINE + '\nERROR\n{}\n' + LINE

# Regex for input validation
ORDER_TYPE_REGEX = r'[d|p]{1}$'
ORDER_CONFIRM_REGEX = r'[y|n]{1}$'
PIZZA_MENU_REGEX = r'^([\d]+)|(<finish>)$'
NAME_REGEX = r"[a-z -']+$"
STREET_REGEX = r'^([a-z_-]+ )?\d+[a-z]? [\w _-]+$'
SUBURB_TOWN_CITY_REGEX = r'([\d]+)?[a-z ]+$'
POSTCODE_REGEX = r'\d{4}$'
MOBILE_REGEX = r'^(0|(\+64(\s|-)?)){1}(\d){2}(\s|-)?\d{3}(\s|-)?\d{4}$'
LANDLINE_REGEX = r'^(0|(\+64(\s|-)?)){1}\d{1}(\s|-)?\d{3}(\s|-)?\d{4}$'
NUMBER_REGEX = '|'.join('(?:{0})'.format(regex)
                        for regex in (MOBILE_REGEX, LANDLINE_REGEX))

# Menu
PIZZA_LIST = OrderedDict({'BBQ Italian Sausage': 8.50,
                          'BBQ Pork and Onion': 8.50,
                          'Beef and Onion': 8.50,
                          'Ham and Cheese': 8.50,
                          'Hawaiian': 8.50,
                          'Pepperoni': 8.50,
                          'Simply Cheese': 8.50,
                          'Cheesy Chicken Chorizo and Bacon': 13.50,
                          'Chicken and Camembert': 13.50,
                          'Chicken Supreme': 13.50,
                          'Loaded Supreme': 13.50,
                          'Mega Meatlovers': 13.50,
                          })
MENU_SIZE = len(PIZZA_LIST)

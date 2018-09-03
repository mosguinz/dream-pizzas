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


def confirm_order(confirm):
    """Print end-of-order confirmation box."""
    print('\n\n' + DOUBLE_LINE + '\n')
    if confirm:
        print('ORDER SUBMITTED')
    else:
        print('ORDER CANCELLED')
    print('Press Enter key to continue.')
    input('\n' + DOUBLE_LINE + '\n\n')
    raise KeyboardInterrupt


def print_menu(menu):
    """Self-explanatory."""
    for index, pizza in enumerate(menu, 1):
        print('{}.\t{:<32}{:>21}{:>6.2f}'.format(
            index, pizza, '$', menu[pizza]))


class Order:
    """Hold order information."""

    def __init__(self):
        """Default values for order."""
        self.is_delivery = False
        self.name = ''
        self.address = None
        self.phone = None
        self.pizzas = {}
        self.cost = 0.00

    def fetch_input(self, prompt, regex, error_message):
        while True:
            try:
                # Get input and strip trailing whitespaces
                user_input = input('\n' + prompt + ': ').lower().strip()

                if user_input == '':
                    print(ERROR.format('Required field.'))
                elif user_input == '<exit>':
                    sys.exit()
                elif user_input == '<cancel>':
                    confirm_order(False)
                elif re.match(regex, user_input):
                    break  # to return input
                else:
                    raise ValueError

            except ValueError:
                print(ERROR.format(error_message))

            return user_input

    def set_is_delivery(self):
        order = self.fetch_input('Enter order type.\n'
                                 'Enter "D" for delivery, or enter "P" for pick-up',
                                 ORDER_TYPE_REGEX,
                                 'Invalid order type.')

        self.is_delivery = True if order == 'd' else False

    def set_name(self):
        name = self.fetch_input('Enter customer name',
                                NAME_REGEX,
                                'Invalid character in name.\n'
                                "Valid characters: A-Z ' - [space]").title()

        self.name = name

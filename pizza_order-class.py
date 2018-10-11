"""Dream Pizzas ordering console for phone operators."""

import re
import sys
from textwrap import dedent
from collections import namedtuple

# Order specifications
DELIVERY_CHARGE = 3.00
MAX_ORDER_SIZE = 5

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
Pizza = namedtuple('Pizza', ['name', 'price'])
PIZZA_LIST = [Pizza('BBQ Italian Sausage', 8.5),
              Pizza('BBQ Pork and Onion', 8.5),
              Pizza('Beef and Onion', 8.5),
              Pizza('Ham and Cheese', 8.5),
              Pizza('Hawaiian', 8.5),
              Pizza('Pepperoni', 8.5),
              Pizza('Simply Cheese', 8.5),
              Pizza('Cheesy Chicken Chorizo and Bacon', 13.5),
              Pizza('Chicken and Camembert', 13.5),
              Pizza('Chicken Supreme', 13.5),
              Pizza('Loaded Supreme', 13.5),
              Pizza('Mega Meatlovers', 13.5)]
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
        print('{:>2}. {:<32}{:>21}{:>6.2f}'.format(
            index, pizza.name, '$', pizza.price))


class Order:
    """Hold order information."""

    def __init__(self):
        self.is_delivery = None
        self.customer_name = None
        if self.is_delivery:
            self.address = None
            self.phone = None
        self.pizzas_ordered = None
        self.total = 0.00

    def fetch_input(self, prompt, regex, error_message):
        """Get and evaluate user input."""
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

    @property
    def is_delivery(self):
        """bool: Whether order is a delivery."""
        return self._is_delivery

    @is_delivery.setter
    def is_delivery(self, _):
        value = self.fetch_input('Enter order type.\n'
                                 'Enter "D" for delivery, or enter "P" for pick-up',
                                 ORDER_TYPE_REGEX,
                                 'Invalid order type.')
        self._is_delivery = True if value == 'd' else False

    @property
    def customer_name(self):
        """str: Customer name"""
        return self._customer_name

    @customer_name.setter
    def customer_name(self, _):
        value = self.fetch_input('Enter customer name',
                                 NAME_REGEX,
                                 'Invalid character in name.\n'
                                 "Valid characters: A-Z ' - [space]").title()
        self._customer_name = value

    @property
    def address(self):
        """Address (namedtuple): Order delivery address."""
        return self._address

    @address.setter
    def address(self, _):
        street = self.fetch_input('Enter delivery address.\n'
                                  'Street address',
                                  STREET_REGEX,
                                  'Invalid street address.\n'
                                  'Must contain at least one digit and character.' +
                                  EXAMPLES.format('26 Elwyn Cresent',
                                                  '434 George Street',
                                                  '6A Hanover Street',
                                                  '459 Princes Street')).title()
        suburb = self.fetch_input('Suburb',
                                  SUBURB_TOWN_CITY_REGEX,
                                  'Invalid suburb.\n'
                                  'Must contain at least a character.' +
                                  EXAMPLES.format('Green Island',
                                                  'Brockville',
                                                  'Kenmure',
                                                  'Concord')).title()
        town = self.fetch_input('Town/city',
                                SUBURB_TOWN_CITY_REGEX,
                                'Invalid town/city.\n'
                                'Must contain at least a character.' +
                                EXAMPLES.format('Dunedin',
                                                'Ashburton',
                                                'Christchurch',
                                                'Auckland')).title()
        postcode = self.fetch_input('Postcode',
                                    POSTCODE_REGEX,
                                    'Invalid postcode.\n'
                                    'Postcode must be a four digit value.' +
                                    EXAMPLES.format('9018',
                                                    '9011',
                                                    '8013',
                                                    '1010'))

        Address = namedtuple(
            'Address', ['street', 'suburb', 'town', 'postcode'])
        self._address = Address(street, suburb, town, postcode)

    @property
    def phone(self):
        """str: Customer phone number."""
        return self._phone

    @phone.setter
    def phone(self, _):
        value = self.fetch_input('Phone number',
                                 NUMBER_REGEX,
                                 'Invalid phone number.' +
                                 EXAMPLES.format('+64 7 123 1234',
                                                 '07-123-1234',
                                                 '021 123 1234',
                                                 '(Spaces and hyphen optional.)'))
        self._phone = value

    @property
    def pizzas_ordered(self):
        """dict: Customer order.
        key: Pizza number
        value: Amount of pizza
        """
        return self._pizzas_ordered

    @pizzas_ordered.setter
    def pizzas_ordered(self, _):
        prompt = ('{} of {}\n'
                  'Enter a number from 1 to {} to select a pizza.\n'
                  'Or enter "<finish>" to complete order')
        pizzas_ordered = {}
        ordered_amount = 1

        print('\nSelect a pizza from the menu below.\n'
              'An order may contain up to {} pizzas.\n'.format(MAX_ORDER_SIZE))
        # Keep asking till limit is reached
        while ordered_amount < MAX_ORDER_SIZE + 1:
            print_menu(PIZZA_LIST)
            try:
                option_number = int(self.fetch_input(prompt.format(ordered_amount,
                                                                   MAX_ORDER_SIZE,
                                                                   MENU_SIZE),
                                                     PIZZA_MENU_REGEX,
                                                     'Invalid pizza number.'))
                print(LINE + '\n')

                # Check if given option number is valid
                if option_number in range(1, MENU_SIZE + 1):
                    # Decrement number by one to access index of PIZZA_LIST
                    option_number -= 1
                    ordered_amount += 1
                    try:
                        # Increment the amount ordered
                        pizzas_ordered[PIZZA_LIST[option_number]] += 1
                    except KeyError:
                        # Or, create new key with order number
                        pizzas_ordered[PIZZA_LIST[option_number]] = 1
                else:
                    raise IndexError('Invalid range.')

            except IndexError as e:
                print(ERROR.format(e))

            # Order is finished (cancel before reaching MAX_ORDER_SIZE)
            # Will fail to parse as base 10, so it must be "<finish>"
            except ValueError:
                if ordered_amount == 1:
                    print(ERROR.format('You must select at least one pizza.\n'
                                       'Or enter "<cancel>" to cancel order.'))
                else:
                    break

        self._pizzas_ordered = pizzas_ordered

    @property
    def total(self):
        """float: Total order total."""
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    def __str__(self):
        order_type = 'Pick-up'
        customer_details = '''\
        CUSTOMER NAME:       {0.customer_name}
        ORDER TYPE:          {1}'''
        if self.is_delivery:
            order_type = 'Delivery'
            customer_details += '''
        CONTACT NUMBER:      {0.phone}
        DELIVERY ADDRESS:    {0.address.street}
                             {0.address.suburb}
                             {0.address.town} {0.address.postcode}'''

        customer_details = dedent(customer_details.format(self, order_type))

        order_details = ''

        for pizza, amount in self.pizzas_ordered.items():
            item_subtotal = pizza.price * amount
            amount = '(x{})'.format(amount) if amount > 1 else ''
            self.total += item_subtotal

            order_details += '{:<32}{:>17}{:>8}{:>6.2f}\n'.format(
                pizza.name, amount, '$', item_subtotal)

        total_fields = '{:<32}{:>25}{:>6.2f}'

        if self.is_delivery:
            order_details += total_fields.format('Subtotal', '$', self.total)
            order_details += total_fields.format(
                'Delivery surcharge', '$', DELIVERY_CHARGE)
            self.total += DELIVERY_CHARGE

        order_total = total_fields.format('TOTAL', '$', self.total)

        receipt = '\n'.join(['ORDER CONFIRMATION',
                             DOUBLE_LINE,
                             customer_details,
                             DOUBLE_LINE + '\n',
                             'ORDER SUMMARY',
                             LINE,
                             order_details,
                             LINE,
                             order_total,
                             DOUBLE_LINE
                             ])

        return receipt

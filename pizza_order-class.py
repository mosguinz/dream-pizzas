"""Dream Pizzas ordering console for phone operators."""

import re
import sys
from collections import namedtuple

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
        """bool: Whether order is a delivery"""
        return self._is_delivery

    @is_delivery.setter
    def is_delivery(self):
        order = self.fetch_input('Enter order type.\n'
                                 'Enter "D" for delivery, or enter "P" for pick-up',
                                 ORDER_TYPE_REGEX,
                                 'Invalid order type.')

        self._is_delivery = True if order == 'd' else False

    @property
    def customer_name(self):
        """str: Customer name"""
        return self._customer_name

    @customer_name.setter
    def customer_name(self):
        name = self.fetch_input('Enter customer name',
                                NAME_REGEX,
                                'Invalid character in name.\n'
                                "Valid characters: A-Z ' - [space]").title()

        self._customer_name = name

    @property
    def address(self):
        """Address (namedtuple): Order delivery address."""
        return self._address

    @address.setter
    def address(self):
        Address = namedtuple(
            'Address', ['street', 'suburb', 'town', 'postcode'])
        suburb_town_error = 'Must contain at least a character.'

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
                                  'Invalid suburb.\n' + suburb_town_error +
                                  EXAMPLES.format('Green Island',
                                                  'Brockville',
                                                  'Kenmure',
                                                  'Concord')).title()
        town = self.fetch_input('Town/city',
                                SUBURB_TOWN_CITY_REGEX,
                                'Invalid town/city.\n' + suburb_town_error +
                                EXAMPLES.format('Dunedin',
                                                'Ashburton',
                                                'Christchurch',
                                                'Auckland')).title()
        postcode = self.fetch_input('Postcode',
                                    POSTCODE_REGEX,
                                    'Invalid postcode.\n'
                                    'Postcode must be 4 digit numbers.' +
                                    EXAMPLES.format('9018',
                                                    '9011',
                                                    '8013',
                                                    '1010'))

        self._address = Address(street, suburb, town, postcode)

    @property
    def phone(self):
        """str: Customer phone number."""
        return self._phone

    @phone.setter
    def phone(self):
        phone = self.fetch_input('Phone number',
                                 NUMBER_REGEX,
                                 'Invalid phone number.' +
                                 EXAMPLES.format('+64 7 123 1234',
                                                 '07-123-1234',
                                                 '021 123 1234',
                                                 '(Spaces and hyphen optional.)'))

        self._phone = phone

    @property
    def pizza_order(self):
        """dict: Customer order.

        key: Pizza number
        value: Amount of pizza
        """
        return self._pizza_order

    @pizza_order.setter
    def pizza_order(self):
        prompt = ('{} of {}\n'
                  'Enter a number from 1 to {} to select a pizza.\n'
                  'Or enter "<finish>" to complete order')
        pizza_order = {}
        ordered_amount = 1

        print('\nSelect a pizza from the menu below.\n'
              'An order may contain up to {} pizzas.\n'.format(MAX_PIZZA))

        # Keep asking till limit is reached
        while ordered_amount < MAX_PIZZA + 1:
            print_menu(PIZZA_LIST)
            try:
                pizza_num = int(self.fetch_input(prompt.format(ordered_amount,
                                                               MAX_PIZZA,
                                                               MENU_SIZE),
                                                 PIZZA_MENU_REGEX,
                                                 'Invalid pizza number.'))

                # Add pizza to order if selection is valid
                if pizza_num in range(1, MENU_SIZE + 1):
                    pizza_num -= 1
                    ordered_amount += 1
                    try:
                        pizza_order[PIZZA_LIST[pizza_num]] += 1
                    except KeyError:
                        pizza_order[PIZZA_LIST[pizza_num]] = 1
                else:
                    raise IndexError

            except IndexError:
                print(ERROR.format('Invalid range.'))

            # Must be "<finish>" because of regex
            except ValueError:
                if ordered_amount > 1:
                    break
                else:
                    print(ERROR.format('You must select at least one pizza.\n'
                                       'Or enter "<cancel>" to cancel order.'))

        self._pizza_order = pizza_order

    @property
    def total(self):
        """float: Total order total."""
        return self._total

    @total.setter
    def total(self):
        for pizza in self.pizzas_ordered:
            self._total += pizza.price * self.pizzas_ordered[pizza]

        if self.is_delivery:
            self._total += DELIVERY_CHARGE

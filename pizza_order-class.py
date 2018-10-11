"""Dream Pizzas ordering console for phone operators."""

import re
import sys
from textwrap import dedent
from collections import namedtuple

# Order specifications.
DELIVERY_CHARGE = 3.00
MAX_ORDER_SIZE = 5

# String templates.
LINE = '-' * 63
DOUBLE_LINE = '=' * 63
EXAMPLES = '\n\nExamples:\n' + ' {}\n' * 3 + ' {}'
ERROR = LINE + '\nERROR\n{}\n' + LINE

# Regex for input validation.
ORDER_TYPE_REGEX = r'[d|p]{1}$'
ORDER_CONFIRM_REGEX = r'[y|n]{1}$'
PIZZA_MENU_REGEX = r'^([\d]+)|(--f)$'
NAME_REGEX = r"[a-z\s\-']+$"
STREET_REGEX = r"^([a-z_\-']+\s)?\d+[a-z]?\s[\w\s_\-']+$"
SUBURB_TOWN_CITY_REGEX = r"([\w]+)?[a-z\s_\-']+([\w\s_\-']+)?$"
POSTCODE_REGEX = r'\d{4}$'
MOBILE_REGEX = r'^(0|(\+64(\s|-)?)){1}(\d){2}(\s|-)?\d{3}(\s|-)?\d{4}$'
LANDLINE_REGEX = r'^(0|(\+64(\s|-)?)){1}\d{1}(\s|-)?\d{3}(\s|-)?\d{4}$'
NUMBER_REGEX = '|'.join('(?:{0})'.format(regex)
                        for regex in (MOBILE_REGEX, LANDLINE_REGEX))

# Pizza is an instance of a namedtuple object.
# The attributes of the object are the properties of the pizza.
#
# Attributes
# ----------
#     name (str): Name of the pizza.
#     price (float): Price of the pizza.
Pizza = namedtuple('Pizza', ['name', 'price'])

# List of Pizza: Pizzas available for order; the menu.
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

# int: Number of pizzas available for order.
MENU_SIZE = len(PIZZA_LIST)


def print_splash():
    """Print a beautifully made splash screen :)."""
    print(DOUBLE_LINE)
    print('''
                         ____
    DREAM PIZZAS        / . .\\
     PHONE OPERATOR     \  ---<
     ORDERING CONSOLE    \  /
   ______________________/ /
-=:_______________________/

Enter "--c" at anytime to cancel the current order.
Enter "--e" at anytime to kill this console.
Review order details at the end before submitting orders.

Press Enter key to continue.
''')
    print(DOUBLE_LINE)
    input()


def print_menu(menu):
    """Print menu."""
    for index, pizza in enumerate(menu, 1):
        print('{:>2}. {:<52}${:>6.2f}'.format(index, pizza.name, pizza.price))


class Order:
    """Hold order information."""

    def __init__(self):
        """Class does not take arguements upon instantiation to set attributes.

        Instead, they are assigned to None to invoke the respective property
        setters.
        """
        self.is_delivery = None
        self.customer_name = None
        if self.is_delivery:
            self.address = None
            self.phone = None
        self.pizzas_ordered = None
        self.item_subtotal = self.pizzas_ordered

    def fetch_input(self, prompt, regex, error_message):
        """Get and evaluate user input.

        Takes user input and check against given regex. Prints given error
        message when input does not satisfy regex.

        Also trims input to fit be 37 characters or less so it doesn't break
        text wrapping.

        Args
        ----
            prompt (str): Message to display to prompt user input.
            regex (str): Regular expression for the function to check against
                the provided user input.
            error_message (str): Message to display when user input does not
                matches the given regex.

        Returns
        -------
            user_input (str): A string that satisfies given regex.

        Raises
        ------
            ValueError: If the given input is blank or does not matches regex.
                Handled within the function to print the given error message
                and ask user for input again.
            SystemExit: If the given input matches the special command "--e".
                Simply exits the console.

        """
        while True:
            try:
                # Get input and strip trailing whitespaces.
                user_input = input('\n' + prompt + ': ').lower().strip()

                if user_input == '':
                    raise ValueError('Required field.')
                elif user_input == '--e':
                    sys.exit()
                elif user_input == '--c':
                    self.confirm(False)
                elif re.match(regex, user_input):
                    break  # to return input.
                else:
                    raise ValueError(error_message)

            except ValueError as e:
                print(ERROR.format(e))

        # Replace last 3 characters with elipsis if input is too long.
        if len(user_input) > 37:
            user_input = user_input[:34] + '...'

        return user_input

    def confirm(self, submit=None):
        """Confirm the order.

        Prompts for an input if a (bool) value is not provided for submit.
        Informs user whether order has been submitted or cancelled,
        corresponding to the given value of submit or input.

        Args
        ----
            submit (bool, optional): True if order is confirmed, False
                otherwise. Defaults to None.

        Returns
        -------
            None.

        Raises
        ------
            KeyboardInterrupt: Raises regardless to escape loop.

        """
        if submit is None:
            submit = self.fetch_input('Submit order? (Y/N)',
                                      ORDER_CONFIRM_REGEX,
                                      'Invalid input.\n'
                                      'Enter "Y" to submit order, or "N" to cancel order.')
            submit = True if submit == 'y' else False

        print('\n\n' + DOUBLE_LINE + '\n')
        print('ORDER SUBMITTED') if submit else print('ORDER CANCELLED')
        print('Press Enter key to continue.')
        input('\n' + DOUBLE_LINE + '\n\n')
        raise KeyboardInterrupt('Restarting console...')

    @property
    def is_delivery(self):
        """bool: True if order is delivery, False otherwise."""
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
        """str: Customer name."""
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
        """Address (namedtuple): Order delivery address.

        The attribute address is an instance of a namedtuple object, Address.
        The attributes of the object are the properties of the address.

        Attributes
        ----------
            street (str): Street address.
            suburb (str): Suburb.
            town (str): Town.
            postcode (str): Postcode.

        """
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

        Address = namedtuple('Address', ['street', 'suburb', 'town', 'postcode'])
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

        key (Pizza): instance of Pizza (namedtuple).
        value: Amount of pizza(s) ordered.

        """
        return self._pizzas_ordered

    @pizzas_ordered.setter
    def pizzas_ordered(self, _):
        pizzas_ordered = {}
        ordered_amount = 1

        while ordered_amount < MAX_ORDER_SIZE + 1:
            # Display menu.
            print()
            print_menu(PIZZA_LIST)

            try:
                print(dedent("""
                             Select a pizza from the menu above.
                             An order may contain up to {} pizzas.
                             Enter a number from 1 to {} to select a pizza.
                             Or enter "--f" to complete order."""
                             .format(MAX_ORDER_SIZE, MENU_SIZE)))

                # Get input
                option_number = int(self.fetch_input(
                    'Pizza {} of {}'.format(ordered_amount, MAX_ORDER_SIZE),
                    PIZZA_MENU_REGEX, 'Invalid pizza number.'))

                # Check if given option number is valid.
                if option_number in range(1, MENU_SIZE + 1):
                    # Decrement number by one to access index of PIZZA_LIST.
                    option_number -= 1
                    ordered_amount += 1
                    selected_pizza = PIZZA_LIST[option_number]

                    # Inform user of selected option.
                    print('Selected {0.name} - ${0.price:.2f}.'.format(selected_pizza))

                    try:
                        # Increment the amount ordered.
                        pizzas_ordered[selected_pizza] += 1
                    except KeyError:
                        # Or, create new key with order number.
                        pizzas_ordered[selected_pizza] = 1
                else:
                    raise IndexError('Invalid range.')

            except IndexError as e:
                print(ERROR.format(e))

            # Order is finished (cancel before reaching MAX_ORDER_SIZE).
            # Will fail to parse as base 10, so it must be "--f".
            except ValueError:
                if ordered_amount == 1:
                    print(ERROR.format('You must select at least one pizza.\n'
                                       'Or enter "--c" to cancel order.'))
                else:
                    break

        self._pizzas_ordered = pizzas_ordered

    @property
    def item_subtotal(self):
        """dict: Subtotal amount for each pizza.

        key (str): Name of pizza.
        value (tuple): Amount of pizza and the subtotal cost.

        """
        return self._item_subtotal

    @item_subtotal.setter
    def item_subtotal(self, value):
        item_subtotal = {}
        self.total = DELIVERY_CHARGE if self.is_delivery else 0

        for pizza, amount in value.items():
            subtotal = pizza.price * amount
            item_subtotal[pizza.name] = (amount, subtotal)
            self.total += subtotal

        self._item_subtotal = item_subtotal

    @property
    def total(self):
        """float: Total order cost."""
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    def __str__(self):
        """Return the order into a readable 'receipt-like' format."""
        # Customer details.
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

        # Order details.
        order_details = []

        for pizza, value in self.item_subtotal.items():
            # Unpack tuple.
            amount, subtotal = value
            # Show multiplier if amount > 1.
            amount = '(x{})'.format(amount) if amount > 1 else ''
            order_details.append('{0:<45}'
                                 '{1:<11}'
                                 '${2:>6.2f}'.format(pizza,
                                                     amount,
                                                     subtotal))
        order_details = '\n'.join(order_details) + '\n'

        # Order subtotal.
        total_fields = '{:<56}${:>6.2f}'
        order_subtotal = []

        # Set subtotal to amount before delivery surcharge.
        subtotal = self.total - DELIVERY_CHARGE if self.is_delivery else self.total
        order_subtotal.append(total_fields.format('Subtotal', subtotal))
        if self.is_delivery:
            order_subtotal.append(total_fields.format(
                'Delivery surcharge', DELIVERY_CHARGE))
        order_subtotal = '\n'.join(order_subtotal)

        # Order total.
        order_total = total_fields.format('Total', self.total)

        receipt = '\n'.join(['\nORDER CONFIRMATION',
                             DOUBLE_LINE,
                             customer_details,
                             DOUBLE_LINE + '\n',
                             'ORDER SUMMARY',
                             LINE,
                             order_details,
                             order_subtotal,
                             LINE,
                             order_total,
                             DOUBLE_LINE])

        return receipt


while True:
    print_splash()
    try:
        order = Order()
        print(order)
        order.confirm()
    except KeyboardInterrupt as e:
        print(e)

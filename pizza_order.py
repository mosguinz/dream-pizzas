"""Dream Pizzas ordering console for phone operators."""
# Write pizza as Class object?

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


def print_splash():
    """Self-explanatory."""
    print(DOUBLE_LINE)
    print('''
                         ____
    DREAM PIZZAS        / . .\\
     PHONE OPERATOR     \  ---<
     ORDERING CONSOLE    \  /
   ______________________/ /
-=:_______________________/

Enter "<cancel>" at anytime to cancel the current order.
Enter "<exit>" at anytime to kill this console.
Review order details at the end before submitting orders.

Press Enter key to continue.
''')
    print(DOUBLE_LINE)
    input()


def confirm_order(confirm):
    """Print end-of-order confirmation box."""
    print('\n\n' + DOUBLE_LINE + '\n')
    if confirm is True:
        print('ORDER SUBMITTED')
    else:
        print('ORDER CANCELLED')
    print('Press Enter key to continue.')
    print('\n' + DOUBLE_LINE + '\n')
    input()
    raise KeyboardInterrupt


def fetch_input(prompt, regex, error_message):
    """Evaluate and validate user input using the provided regex.

    prompt (str): prompt message
    regex (str): regex for input validation
    error_message (str): error message

    Return value that match regex.

    [THIS FUNCTION IS SLIGHTLY UGLY.]
    """
    # Keep asking user for input. Break and return when input is valid.
    while True:
        try:
            # Get input and strip trailing whitespaces
            user_input = input('\n' + prompt).lower().strip()

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


def print_menu(options):
    """Self-explanatory.

    options (OrderedDict): the menu and price
    """
    for index, option in enumerate(options, 1):
        print('{}.\t{:<32}{:>21}{:>6.2f}'.format(
            index, option, '$', options[option]))


def get_order_type():
    """Self-explanatory."""
    order = fetch_input('Enter order type.\n'
                        'Enter "D" for delivery, or enter "P" for pick-up: ',
                        ORDER_TYPE_REGEX,
                        'Invalid order type.')

    return True if order == 'd' else False


def get_name():
    """Self-explanatory."""
    name = fetch_input('Enter customer name: ',
                       NAME_REGEX,
                       'Invalid character in name.\n'
                       "Valid characters: A-Z ' - [space]").title()

    return name


def get_address():
    """Self-explanatory."""
    suburb_town_error = 'Must contain at least a character.'

    street = fetch_input('Enter delivery address.\n'
                         'Street address: ',
                         STREET_REGEX,
                         'Invalid street address.\n'
                         'Must contain at least one digit and character.' +
                         EXAMPLES.format('26 Elwyn Cresent',
                                         '434 George Street',
                                         '6A Hanover Street',
                                         '459 Princes Street')).title()
    suburb = fetch_input('Suburb: ',
                         SUBURB_TOWN_CITY_REGEX,
                         'Invalid suburb.\n' + suburb_town_error +
                         EXAMPLES.format('Green Island',
                                         'Brockville',
                                         'Kenmure',
                                         'Concord')
                         ).title()
    town = fetch_input('Town/city: ',
                       SUBURB_TOWN_CITY_REGEX,
                       'Invalid town/city.\n' + suburb_town_error +
                       EXAMPLES.format('Dunedin',
                                       'Ashburton',
                                       'Christchurch',
                                       'Auckland')).title()
    postcode = fetch_input('Postcode: ',
                           POSTCODE_REGEX,
                           'Invalid postcode.\n'
                           'Postcode must be 4 digit numbers.' +
                           EXAMPLES.format('9018',
                                           '9011',
                                           '8013',
                                           '1010'))

    return street, suburb, ' '.join((town, str(postcode)))


def get_phone():
    """Self-explanatory."""
    phone = fetch_input('Phone number: ',
                        NUMBER_REGEX,
                        'Invalid phone number.' +
                        EXAMPLES.format('+64 7 123 1234',
                                        '07-123-1234',
                                        '021 123 1234',
                                        '(Spaces and hyphen optional.)'))

    return phone


def get_pizza():
    """Self-explanatory."""
    prompt = ('{} of {}\nEnter a number from 1 to {} to select a pizza.\n'
              'Or enter "<finish>" to complete order: ')
    pizzas_ordered = {}
    ordered_amount = 1

    print('\nSelect a pizza from the menu below.\n'
          'An order may contain up to {} pizzas.\n'.format(MAX_PIZZA))

    # Keep asking till limit is reached
    while ordered_amount < MAX_PIZZA + 1:
        print_menu(PIZZA_LIST)
        try:
            pizza_num = int(fetch_input(prompt.format(ordered_amount,
                                                      MAX_PIZZA,
                                                      MENU_SIZE),
                                        PIZZA_MENU_REGEX,
                                        'Invalid pizza number.'))

            # Add pizza to order if selection is valid
            if pizza_num in range(1, MENU_SIZE + 1):
                pizza_num -= 1
                ordered_amount += 1
                try:
                    pizzas_ordered[pizza_num] += 1
                except KeyError:
                    pizzas_ordered[pizza_num] = 1
            else:
                raise IndexError

        # Must be "<finish>" because of regex
        except ValueError:
            if ordered_amount > 1:
                break
            else:
                print(ERROR.format('You must select at least one pizza.\n'
                                   'Or enter "<cancel>" to cancel order.'))
        except IndexError:
            print(ERROR.format('Invalid range.'))

    return pizzas_ordered


def print_receipt(name, pizzas_ordered, is_delivery, address, phone):
    """Self-explanatory."""
    total = 0
    total_fields = '{:<32}{:>25}{:>6.2f}'
    # List of tuples to reference pizza named
    pizza_ref = list(PIZZA_LIST.items())

    customer_details = OrderedDict({'CUSTOMER NAME:': name})
    if is_delivery:
        customer_details['ORDER TYPE:'] = 'Delivery'
        customer_details['CONTACT NUMBER:'] = phone
        customer_details['DELIVERY ADDRESS:'] = address[0]
        customer_details[' '] = address[1]
        customer_details['  '] = address[2]
    else:
        customer_details['ORDER TYPE:'] = 'Pick-up'

    # Print customer details
    print('\n\nORDER CONFIRMATION\n' + DOUBLE_LINE)
    for field in customer_details:
        print('{:<17}\t{:<43}'.format(field, customer_details[field]))
    print(DOUBLE_LINE + '\n')

    # Print order details and calculate cost
    print('ORDER SUMMARY\n' + LINE)
    for pizza in pizzas_ordered:
        pizza_name = pizza_ref[pizza][0]
        amount = pizzas_ordered[pizza]
        cost = amount * pizza_ref[pizza][1]
        total += cost
        amount = '(x{})'.format(amount) if amount > 1 else ''
        print('{:<32}{:>17}{:>8}{:>6.2f}'.format(
            pizza_name, amount, '$', cost))

    # Add delivery cost, if applicable
    if is_delivery:
        print()
        print(total_fields.format('Subtotal', '$', total))
        print(total_fields.format(
            'Delivery surcharge', '$', DELIVERY_CHARGE))
        total += DELIVERY_CHARGE

    # Print total cost
    print(LINE)
    print(total_fields.format('Total', '$', total))
    print(LINE)

    # Confirm order
    confirm = fetch_input('Submit order? (Y/N) ',
                          ORDER_CONFIRM_REGEX,
                          'Invalid input.\n'
                          'Enter "Y" to submit order, or "N" to cancel order.')
    if confirm == 'y':
        confirm_order(True)
    else:
        confirm_order(False)


def start_order():
    """Initialize order."""
    is_delivery = get_order_type()
    name = get_name()
    if is_delivery:
        address, phone = get_address(), get_phone()
    else:
        address, phone = None, None
    order_items = get_pizza()
    print_receipt(name, order_items, is_delivery, address, phone)


while True:
    print_splash()
    try:
        start_order()
    except KeyboardInterrupt:
        pass

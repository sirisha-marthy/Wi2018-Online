#!/usr/bin/env python3
# -----------------------------------------------------------
# mailroom.py
#  Script to automate writing thank you emails to donors.
# -----------------------------------------------------------

import time
from sys import exit


class Donors(object):

    def __init__(self):
        self.donorlist = []

    def add_donor(self, donor):
        self.donorlist.append(donor)

    def print_report(self):
        """
        Prints a formatted report on the donors with name, amount given, number of gifts, and average gift.
        :return: None
        """
        # Find longest name in donor list, or use name_min value
        name_max = max(*[len(donor.name) for donor in self.donorlist], 25)

        rpt_title = "Donor Name" + ' ' * (name_max - 9) + "| Total Given | Num Gifts | Average Gift"
        print(rpt_title)
        print("-" * len(rpt_title))
        for donor in self.donorlist:
            print(f"{donor.name:{name_max}}  ", end='')
            ddons = donor.donations
            print(f"$ {sum(ddons):>10.2f}   {len(ddons):>9}  ${sum(ddons)/len(ddons):>12.2f}")

    def send_letters_all(self):
        """
            Runs through donor data structure, generates a thank you letter for each and saves it to
            the current working directory with in a date+donorname.txt file
            :return: None
            """
        for donor in self.donorlist:
            print(f'Generating letter for {donor.name}')
            now = time.localtime()
            f_name = f"{now.tm_year}{now.tm_mon:02}{now.tm_mday:02}_"
            f_name += donor.name.replace(" ", "_") + ".txt"
            with open(f_name, 'w') as file_out:
                file_out.write(donor.generate_letter())
        return None

    @property
    def list_donors(self):
        return [donor.name for donor in self.donorlist]

    @property
    def count(self):
        return len(self.donorlist)

    def get_donor(self, dname):
        if dname == "":
            return None

        for donor in self.donorlist:
            if donor.name == dname:
                return donor

        newdonor = Donor(dname)
        self.add_donor(newdonor)
        return newdonor


class Donor(object):

    def __init__(self, name):
        if not name:
            raise ValueError("Donor name cannot be empty.")
        self.name = name
        self.donations = []

    @property
    def first(self):
        name_sp = self.name.split()
        if len(name_sp) == 1:
            return ''
        else:
            return name_sp[0]

    @property
    def last(self):
        name_sp = self.name.split()
        if len(name_sp) == 1:
            return self.name
        else:
            return ' '.join(name_sp[1:])

    def add_donation(self, amount):
        if float(amount) <= 0:
            raise ValueError('Donation amount must be a positive number.')
        else:
            self.donations.append(amount)

    @property
    def last_donation(self):
        if not self.donations:
            return None
        else:
            return self.donations[-1]

    def generate_letter(self):
        """
        Generates a Thank You letter to send to a donor. Uses the last value in their donations list to
        mention their last donation amount.
        :param donor: a donor dictionary entry
        :return: string containing the text of the Thank You letter.
        """
        format_string = """
Dear {first_name} {last_name},

   Thank you for your donation of ${last_donation:.2f}.

            Warmest Regards,
                Local Charity
"""
        return format_string.format(
            last_donation=float(self.last_donation),
            first_name=self.first,
            last_name=self.last
        )


def send_thank_you_menu(dlist):
    """
    Prompts for donor name, if not present, adds user to data. Prompts for donation
    and adds it to donor's data. Prints a 'Thank You' email populated with the donor's data.
    :return: None
    """

    while True:
        name = input("Enter a Full Name ('list' to show list of donors, 'q' to quit): ")
        if name == 'q':
            return
        elif name == 'list':
            print(("{}\n" * dlist.count).format(*dlist.list_donors))
            continue
        else:
            donor = dlist.get_donor(name)
            if not donor:
                print("Name cannot be empty.")
                continue
            else:
                break

    while True:
        try:
            amount = float(input(f"Enter a donation amount for {donor.name} : "))
            if amount <= 0:
                print('Amount donated must be a positive number.')
            else:
                break
        except ValueError:
            print('Please enter a numerical value.')

    donor.add_donation(amount)
    print(donor.generate_letter())


def menu(menu_data):
    """
    Prints the main user menu & retrieves user selection.
    :param: a menu list, consisting of tuples with three values:
        [0]: text to be presented to user
        [1]: function that should be called for the menu item
        [2]: parameter that should be used in the function call, None if no parameter call needed
    :return: two values:
        1) the function corresponding to the user's selection, or None on a bad selection
        raises ValueError if choice is non-numeric
        2) a parameter that should be used with the fn call, None if no parameter needed
    """
    print("\nPlease choose one of the following options:")

    for index, menu_item in enumerate(menu_data):   # Prints the menu user text
        print(f"{index + 1}) {menu_item[0]}")

    choice = int(input("> ")) - 1

    if choice in range(len(menu_data)):                     # Ensure that option chosen is within menu range, this
        return menu_data[choice][1], menu_data[choice][2]   # handles choosing 0, which would return menu_data[-1][1]

    return None


if __name__ == "__main__":

    # Global data structure
    donor_data = (
        ('Al Donor1', [10.00, 20.00, 30.00, 40.00, 50.00]),
        ('Bert Donor2' ,[10.00]),
        ('Connie Donor3', [10.00, 10.00, 10.01]),
        ('Dennis Donor4', [10.00, 20.00, 20.00]),
        ('Egbert Donor5', [10.39, 20.21, 10.59, 4000.40])
    )

    dl = Donors()
    for name, dons in donor_data:
        n = Donor(name)
        dl.add_donor(n)
        for d in dons:
            n.donations.append(d)

    dl.print_report()

    menu_functions = [
        ('Send a Thank You', send_thank_you_menu, dl),
        ('Print a report', dl.print_report, None),
        ('Send letters to everyone', dl.send_letters_all, None),
        ('Quit', exit, None),
    ]
    while True:
        try:
            fn, param = menu(menu_functions)
            if param:
                fn(param)
            else:
                fn()
        except TypeError:
            continue
        except ValueError:
            continue

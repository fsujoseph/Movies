# Coding Assessment for Walmart Labs
# Author: Joseph Caswell

import math
import pathlib


class Theater:
    def __init__(self, reservations, row, col):
        self.reservations = reservations            # Reservations stored in dict as {ID: # Seats}
        self.row = row                              # Number of rows
        self.col = col                              # Seats per row
        self.open = row * col                       # Total seats
        self.seating = self.init_seats()            # Initialize 2-D matrix of theater
        self.output = {}                            # Store output as {ID: seat #, seat #...}
        self.aisles = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}

    def init_seats(self):
        """
        Initializes movie theater layout as a 2-D matrix of # rows * # seats per row. Values are assigned to each seat
        to represent the desirability of the seat. This is used to optimize the best seating for the customer.
        The middle 1/3 are all given high desirability and decrement off as the seats approach the left and right aisle.
        An extra boost in value is given for all seats in the middle to back of theater.
        """
        seating = []
        for x in range(self.row):                           # Initialize matrix as list of 0's, row * col
            r = []
            for y in range(self.col):
                r.append(0)
            seating.append(r)

        # Sets middle to correctly distribute left and right depending on divisibility of 3
        if self.col % 3 == 2:
            middle = (self.col // 3, (self.col // 3) * 2 + 1)
        elif self.col % 3 == 1:
            middle = (self.col // 3, (self.col // 3) * 2)
        else:
            middle = (self.col // 3, (self.col // 3) * 2 - 1)
        left = (0, middle[0] - 1)
        right = (middle[1] + 1, self.col - 1)
        inc = 4 / left[1]                                   # Correct value to increment, modular for size of theater
        lval, rval = 4, 4                                   # Starting values of left and right

        for index, row in enumerate(seating):
            for col in range(left[1], left[0] - 1, -1):     # Decrementing value from middle to left
                if index > 3:
                    row[col] = math.ceil(lval) + 2          # This is where the middle to back values get a boost
                else:
                    row[col] = math.ceil(lval)
                lval = lval - inc
            for col in range(middle[0], middle[1] + 1):     # Middle is all given high value
                if index > 3:
                    row[col] = 7
                else:
                    row[col] = 5
            for col in range(right[0], right[1] + 1):       # Decrementing value from middle to right
                if index > 3:
                    row[col] = math.ceil(rval) + 2
                else:
                    row[col] = math.ceil(rval)
                rval = rval - inc
            lval, rval = 4, 4

        return seating

    def add_reservations(self):
        """
        This method acts as the driver for assigning the seats to the reservations by calling a few other methods to
        help. We iterate through the dictionary of reservations because in Python, dictionaries are now stored in the
        order they were created so it maintains the priority of the reservations. Reservations are first prioritized
        by seating the group together, and then by the best seats available. If the entire group cannot be fit, then
        the group is split up and given the best seats available. Output is saved to a new dictionary.
        """
        for id, seats in self.reservations.items():         # Iterate through dictionary
            if self.seats_available() < seats:              # If not enough seats available, go to next reservation
                self.output[id] = 'Maximum Capacity'
                continue
            not_assigned = seats
            while not_assigned > 0:                         # Loop until all seats requested are assigned
                max_val, best_slot = 0, None                # Keep track of best seating for given reservation
                for row in range(self.row - 1, - 1, - 1):
                    for col in range(self.col - seats + 1):
                        if self.is_valid(row, col, col + seats - 1):    # If valid, update max value and slot
                            value = self.get_value(row, col, col + seats)
                            if value > max_val:
                                max_val = value
                                best_slot = (row, col, col + seats)
                if best_slot:                               # Assign optimal seat(s) to reservation ID
                    self.assign(best_slot, id)
                    not_assigned = not_assigned - seats     # Seats have been assigned, so decrement
                    seats = not_assigned                    # Seats still needing to be assigned
                else:                                       # If no slots for requested group size, try smaller group
                    seats -= 1

            self.open = self.open - seats

    def is_valid(self, row, start, end):
        """
        Checks if proposed seating arrangement is valid based off of the current theater. Returns True or False.
        """
        buf1 = start - 3                                        # Check 3 seats to left and right for COVID protocol
        buf2 = end + 4
        if buf1 < 0:
            buf1 = 0
        if buf2 >= self.col:
            buf2 = self.col

        for col in range(buf1, buf2):
            if not isinstance(self.seating[row][col], int):     # If seat is not an integer, it's a reserved seat ID
                return False

        return True

    def get_value(self, row, start, end):
        """
        Returns the value of the proposed seating arrangement.
        """
        value = 0
        for col in range(start, end):
            value = value + self.seating[row][col]

        return value

    def assign(self, slot, id):
        """
        Assigns seating choices to reservation by inserting the ID number onto seat choices in 2-D matrix. Also
        saves the seat choices to a dictionary for later output.
        """
        row, start, end = slot                                              # Unpack set
        for col in range(start, end):
            self.seating[row][col] = id                                     # Assign ID to matrix spot
            if id in self.output:                                           # Add seat choice to output dictionary
                self.output[id].append(self.aisles[row + 1] + str(col + 1))
            else:
                self.output[id] = [self.aisles[row + 1] + str(col + 1)]

    def seats_available(self):
        """
        Returns the number of seats available in the theater, accounting for COVID rules. Iterates through each open
        seat and uses the is_valid method to check if seat is valid.
        """
        available = 0
        for row in range(self.row):
            for col in range(self.col):
                if not isinstance(self.seating[row][col], int):   # If seat already taken don't check
                    continue
                if self.is_valid(row, col, col):    # If seat is valid, increment available seats
                    available += 1

        return available

    def display_theater(self):
        """
        Prints row of theater to aid in visual debugging.
        """
        for row in self.seating:
            print(row)

    def output_to_file(self):
        """
        This method writes an output of the reservation number and the respective reserved seat(s) to a file called
        reservations.txt.
        """
        out = open('assignments.txt', 'w')      # Creates or overwrites output file
        for id, seats in self.output.items():   # For each line, displays ID and the seats appended
            line = id + ' '
            if seats == 'Maximum Capacity':     # If maximum capacity write here
                line = line + seats + '\n'
                out.write(line)
                continue
            for seat in seats:                  # Format each seat
                line = line + seat + ','
            line = line.rstrip(',') + '\n'      # Strip ending comma
            out.write(line)
        out.close()

        path = str(pathlib.Path(__file__).parent.absolute()) + '/assignments.txt'
        print('You can review the results at ' + path)


if __name__ == "__main__":
    file = input("Please enter the name of your input file: ")
    with open(file, 'r') as data:     # Opens input file
        res = {}                                    # Create dictionary with reservations
        for line in data:
            line = line.strip().split()
            res[line[0]] = int(line[1])
    data.close()

    movie = Theater(res, 10, 20)
    movie.display_theater()
    movie.add_reservations()
    print('________________________________________')
    movie.display_theater()
    movie.output_to_file()

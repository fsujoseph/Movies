import unittest
import movies
import random


class MyTestCase(unittest.TestCase):
    def test_random(self):
        """
        This test case generates reservations randomly and attempts to trigger errors in the program.
        """
        for run in range(1):
            row, col = 10, 20                       # Movie theater size is modular
            capacity = row * col
            total = 0                               # Initialize number of requested seats
            id_num = 1
            reservations = {}
            while total < capacity + 10:            # Keep adding reservations until we are past capacity
                if id_num < 10:                     # Format ID number
                    res_id = 'R00' + str(id_num)
                elif id_num < 100:
                    res_id = 'R0' + str(id_num)
                else:
                    res_id = 'R' + str(id_num)
                seats = random.randint(1, 8)        # Generate random number of seats, can change if desired
                reservations[res_id] = seats        # Store ID and seats requested to use for input
                id_num += 1
                total = total + seats

            theater = movies.Theater(reservations, row, col)    # Creates theater object
            theater.display_theater()               # Option to print theater to console
            theater.add_reservations()              # Adds reservations
            print('____________')
            theater.display_theater()               # Option to print theater to console
            theater.output_to_file()                # Output to file


if __name__ == '__main__':
    unittest.main()

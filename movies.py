# Coding Assessment for Walmart Labs
# Author: Joseph Caswell

import math


class Theatre:
    def __init__(self, reservations, row, col):
        self.reservations = reservations
        self.row = row
        self.col = col
        self.open = row * col
        self.seating = self.init_seats()
        self.output = {}
        self.aisles = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J'}

    def init_seats(self):
        seating = []
        for x in range(self.row):
            r = []
            for y in range(self.col):
                r.append(0)
            seating.append(r)

        if self.col % 3 == 2:
            middle = (self.col // 3, (self.col // 3) * 2 + 1)
        elif self.col % 3 == 1:
            middle = (self.col // 3, (self.col // 3) * 2)
        else:
            middle = (self.col // 3, (self.col // 3) * 2 - 1)
        left = (0, middle[0] - 1)
        right = (middle[1] + 1, self.col - 1)
        inc = 4 / left[1]
        lval, rval = 4, 4

        for index, row in enumerate(seating):
            for col in range(left[1], left[0] - 1, -1):
                if index > 3:
                    row[col] = math.ceil(lval) + 1
                else:
                    row[col] = math.ceil(lval)
                lval = lval - inc
            for col in range(middle[0], middle[1] + 1):
                if index > 3:
                    row[col] = 6
                else:
                    row[col] = 5
            for col in range(right[0], right[1] + 1):
                if index > 3:
                    row[col] = math.ceil(rval) + 1
                else:
                    row[col] = math.ceil(rval)
                rval = rval - inc
            lval, rval = 4, 4

        return seating

    def add_reservations(self):
        for id, seats in self.reservations.items():
            if seats > self.open:
                print('Maximum Capacity')
                continue
            not_assigned = seats
            while not_assigned > 0:
                max_val, best_slot = 0, None
                for row in range(self.row - 1, - 1, - 1):
                    for col in range(self.col - seats + 1):
                        if self.is_valid(row, col, col + seats - 1):
                            value = self.get_value(row, col, col + seats - 1)
                            if value > max_val:
                                max_val = value
                                best_slot = (row, col, col + seats)
                if best_slot:
                    self.assign(best_slot, id)
                    not_assigned = not_assigned - seats
                    seats = not_assigned
                else:
                    seats -= 1

            self.open = self.open - seats

    def is_valid(self, row, start, end):
        buf1 = start - 3
        buf2 = end + 3
        if buf1 < 0:
            buf1 = 0
        if buf2 >= self.col:
            buf2 = self.col - 1

        for col in range(buf1, buf2 + 1):
            if not isinstance(self.seating[row][col], int):
                return False

        return True

    def get_value(self, row, start, end):
        value = 0
        for col in range(start, end):
            value = value + self.seating[row][col]

        return value

    def assign(self, slot, id):
        row, start, end = slot
        for col in range(start, end):
            self.seating[row][col] = id
            if id in self.output:
                self.output[id].append(self.aisles[row] + str(col + 1))
            else:
                self.output[id] = [self.aisles[row] + str(col + 1)]

    def get_output(self):
        return self.output

    def display_theatre(self):
        for row in self.seating:
            print(row)


if __name__ == "__main__":
    with open('reservations.txt', 'r') as data:
        res = {}
        for line in data:
            line = line.strip().split()
            res[line[0]] = int(line[1])
    data.close()

    movie = Theatre(res, 10, 20)
    movie.display_theatre()
    movie.add_reservations()
    print('_________________________________')
    movie.display_theatre()

    out = open('assignments.txt', 'w')
    for id, seats in movie.get_output().items():
        out.write(id + ' ')
        for seat in seats:
            out.write(seat + ' ')
        out.write('\n')
    out.close()



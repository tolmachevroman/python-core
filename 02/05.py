from pprint import pprint as pp


class Flight:
    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError(f"No airline code in '{number}'")
        self._number = number
        self._aircraft = aircraft
        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + \
            [{letter: None for letter in seats} for _ in rows]

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def __str__(self):
        return f"Airline: {self.airline()}, Number: {self.number()}, Aircraft: {self._aircraft.model()}"

    def allocate_seat(self, seat, passenger):
        """Allocate a seat to a passenger
        Args:
            seat: A seat designator such as '12C' or '21F'
            passenger: The passenger name
        Raises:
            ValueError: If the seat is unavailable
        """
        row, letter = self.parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} already occupied")
        self._seating[row][letter] = passenger

    def parse_seat(self, seat):
        """Parse a seat designator into a valid row and letter
        Args:
            seat: A seat designator such as 12F
        Returns:
            A tuple containing an integer and a string for row and seat
        """
        rows, seat_letters = self._aircraft.seating_plan()
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"Invalid seat letter {letter}")
        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError(f"Invalid seat row {row_text}")
        if row not in rows:
            raise ValueError(f"Invalid row number {row}")
        return row, letter

    def relocate_passenger(self, from_seat, to_seat):
        """Relocate a passenger to a different seat
        Args:
            from_seat: The existing seat designator for the passenger to be moved
            to_seat: The new seat designator
        """
        from_row, from_letter = self.parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"No passenger to relocate in seat {from_seat}")

        to_row, to_letter = self.parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f"Seat {to_seat} already occupied")

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                   for row in self._seating
                   if row is not None)

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(),
                         self._aircraft.model())

    def _passenger_seats(self):
        """An iterable series of passenger seating locations"""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, f"{row}{letter}")


class Aircraft:
    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)


class AirbusA319(Aircraft):

    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 23), "ABCDEF"


class Boeing777(Aircraft):

    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1, 56), "ABCDEFGHJK"


def console_card_printer(passenger, seat, flight_number, aircraft):
    output = f"| Name: {passenger}" \
             f"  Flight: {flight_number}" \
             f"  Seat: {seat}" \
             f"  Aircraft: {aircraft}" \
             " |"
    banner = '+' + '-' * (len(output) - 2) + '+'
    border = '|' + ' ' * (len(output) - 2) + '|'
    lines = [banner, border, output, border, banner]
    card = '\n'.join(lines)
    print(card)
    print()


if __name__ == '__main__':
    airbus319 = AirbusA319('G-EZBT')
    print(airbus319.num_seats())

    flight = Flight('SN060', airbus319)
    print(flight)
    flight.allocate_seat('12A', 'Guido van Rossum')
    flight.allocate_seat('15F', 'Bjarne Stroustrup')
    flight.allocate_seat('15E', 'Anders Hejlsberg')
    flight.allocate_seat('1C', 'John McCarthy')
    flight.allocate_seat('1D', 'Rich Hickey')
    flight.relocate_passenger('12A', '15D')
    # pp(flight._seating)
    # print(f'Available seats: {flight.num_available_seats()}')
    # passenger = 'Eric Idle'
    # seat = '12B'
    # flight_bumber = 'SN060'
    # aircraft_model = 'Airbus A319'
    # console_card_printer(passenger, seat, flight_bumber, aircraft_model)
    flight.make_boarding_cards(console_card_printer)

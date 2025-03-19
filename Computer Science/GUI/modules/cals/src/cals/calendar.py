import numpy as np
import calendar
import pandas as pd



class Month:
    def __init__(self, year, month_name, binary_array, date_array, zero_array):
        """
        Represents a month with different calendar views.
        :param year: The year of the month.
        :param month_name: The name of the month.
        :param binary_array: NumPy array with 1s and 0s.
        :param date_array: NumPy array with actual date values.
        :param zero_array: NumPy array with only 0s.
        """
        self.year = year
        self.month_name = month_name
        self.binary_array = binary_array
        self.date_array = date_array
        self.zero_array = zero_array

    def set_value(self, date_str, array_type, value):
        """
        Sets a specific value in the specified array type.
        :param date_str: Date in 'YYYY-MM-DD' format.
        :param array_type: Type of array ('binary', 'dates', 'zeros').
        :param value: Value to set (should be 1 for binary).
        """
        d = pd.to_datetime(date_str)
        if d.year != self.year or d.strftime("%B") != self.month_name:
            return  # Ignore if the date is not in the correct month

        row, col = self._get_weekday_position(d)
        if row is not None:
            if array_type == "binary":
                self.binary_array[row, col] = value
            elif array_type == "dates":
                self.date_array[row, col] = value
            elif array_type == "zeros":
                self.zero_array[row, col] = value

    def get_value(self, date_str, array_type):
        """
        Retrieves the value from the specified array type.
        :param date_str: Date in 'YYYY-MM-DD' format.
        :param array_type: Type of array ('binary', 'dates', 'zeros').
        :return: Value from the array.
        """
        d = pd.to_datetime(date_str)
        if d.year != self.year or d.strftime("%B") != self.month_name:
            return None  # Ignore if the date is not in the correct month

        row, col = self._get_weekday_position(d)
        if row is not None:
            if array_type == "binary":
                return self.binary_array[row, col]
            elif array_type == "dates":
                return self.date_array[row, col]
            elif array_type == "zeros":
                return self.zero_array[row, col]
        return None

    def _get_weekday_position(self, date_obj):
        """
        Returns the row and column position of a given date in the month grid.
        """
        first_weekday, _ = calendar.monthrange(self.year, list(calendar.month_name).index(self.month_name))
        first_weekday = (first_weekday - 0) % 7  # Convert to Monday-based index

        day = date_obj.day
        row = (first_weekday + day - 1) // 7
        col = (first_weekday + day - 1) % 7

        return row, col

    def __repr__(self):
        return f"Month({self.month_name} {self.year})"


class CalendarFactory:
    def __init__(self):
        self.weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.month_names = list(calendar.month_name)[1:]  # Remove empty first entry

    def create_month(self, year, month_name):
        """
        Generates a Month object with all its data.
        :param year: Year of the month.
        :param month_name: Month name as a string.
        :return: Month object.
        """
        if month_name not in self.month_names:
            raise ValueError("Invalid month name.")

        month_index = self.month_names.index(month_name) + 1
        binary_array, date_array, zero_array = self._generate_month_arrays(year, month_index)

        return Month(year, month_name, binary_array, date_array, zero_array)

    def _generate_month_arrays(self, year, month):
        """
        Generates three NumPy arrays for a given month:
        - Binary array (1s and 0s)
        - Date array (actual dates and 0s)
        - Zero array (all 0s)
        """
        first_weekday, num_days = calendar.monthrange(year, month)
        first_weekday = (first_weekday - 0) % 7  # Convert to Monday-based

        num_weeks = (first_weekday + num_days + 6) // 7  # Calculate required weeks

        # Initialize arrays
        binary_array = np.zeros((num_weeks, 7), dtype=int)
        date_array = np.zeros((num_weeks, 7), dtype=int)
        zero_array = np.zeros((num_weeks, 7), dtype=int)

        # Populate the arrays
        day = 1
        for row in range(num_weeks):
            for col in range(7):
                if row == 0 and col < first_weekday:
                    continue
                if day > num_days:
                    break

                binary_array[row, col] = 1
                date_array[row, col] = day
                day += 1

        return binary_array, date_array, zero_array

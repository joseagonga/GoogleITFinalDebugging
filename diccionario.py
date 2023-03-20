
import csv
import datetime
import requests


FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)


def get_toListData(data):
    reader = csv.reader(data[1:])
    employees = []
    for row in reader:
        row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d')
        row_name = "{} {}".format(row[0], row[1])
        employees.append((row_date,row_name))

    employees.sort(key=lambda tup: tup[0])

    return employees

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

def get_same_or_newer(start_date,employeesToList):

    min_date_employees = []

    for date,name in employeesToList:
        if date == start_date:
            min_date_employees.append(name)
    
    min_date = start_date

    return min_date, min_date_employees


def list_newer(start_date,employessToList):
    while start_date < datetime.datetime.today():
        start_date, employees = get_same_or_newer(start_date,employessToList)
        if len(employees) != 0:
            print("Started on {}: {}".format(start_date.strftime("%b %d, %Y"), employees))

        # Now move the date to the next one
        start_date = start_date + datetime.timedelta(days=1)


def main():
    start_date = get_start_date()
    data = get_file_lines(FILE_URL)
    employeesToList = get_toListData(data)
    list_newer(start_date,employeesToList)


if __name__ == "__main__":
    main()
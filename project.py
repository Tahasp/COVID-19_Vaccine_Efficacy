"""The Effects of Vaccination Efficacy on COVID-19 Cases
=================================================================================

The purpose of this file is to calculate the total number of cases among vaccinated individuals.
"""
import datetime
from dataclasses import dataclass

POPULATION = {'Ontario': 14570000, 'Nova Scotia': 971395}
ONTARIO_INFO = {'population': 14570000, 'august_8_cases': 552479}
NOVA_SCOTIA_INFO = {'population': 971395, 'august_8_cases': 5900}
VACCINATION_EFFICACY = {'Pfizer': 0.95, 'Moderna': 0.941, 'AstraZeneca': 0.62}
VACCINE_ADMINISTERED = {'Pfizer': 0.77, 'Moderna': 0.22, 'AstraZeneca': 0.01}

TOTAL_CASES_AUGUST8 = {'Ontario': 552479, 'Nova Scotia': 5900}


@dataclass
class VaccinatedCases:
    """
    Instance Attributes:
        - date: The date in the format (year, month, date)
        - total_vaccinated_people: The total population vaccinated until the current date
        - total_cases: The total Covid-19 cases until the current date

    Representation Invariants:
        - 0 < date.month <= 12
        - 0 < date.day <= 31
        - date.year >= 2019
        - total_vaccinated_people >= 0
        - total_cases >= 0

    Sample Usage:
    >>> case = VaccinatedCases(date=datetime.datetime(2021, 8, 9), \
        total_vaccinated_people=5000000, total_cases=100000, location='Ontario')
    """
    date: datetime.date
    total_vaccinated_people: int
    total_cases: int
    location: str


def new_cases(data: list[VaccinatedCases], case: VaccinatedCases) -> int:
    """
    Return daily new cases given the total cases from the previous date and current date.
    >>> val = [VaccinatedCases(datetime.datetime(2021, 8, 9, 0, 0), 9343260,552804)]
    >>> new_cases(val, VaccinatedCases(datetime.datetime(2021, 8, 9, 0, 0), 9343260,552804))
    325

    >>> val2 = [VaccinatedCases(datetime.datetime(2021, 8, 9, 0, 0), 9343260,552804), \
    VaccinatedCases(datetime.datetime(2021, 8, 10, 0, 0), 1000000, 600000)]
    >>> new_cases(val2, VaccinatedCases(datetime.datetime(2021, 8, 10, 0, 0), 1000000, 600000))
    47196
    """
    change_in_cases = 0

    for row in range(len(data)):
        if data[row].location == 'Ontario':
            if data[row] == case and data[row].date == datetime.datetime(2021, 8, 9, 0, 0):
                change_in_cases = data[row].total_cases - TOTAL_CASES_AUGUST8[0]
            elif data[row] == case:
                change_in_cases = data[row].total_cases - data[row - 1].total_cases
        else:
            if data[row] == case and data[row].date == datetime.datetime(2021, 8, 9, 0, 0):
                change_in_cases = data[row].total_cases - TOTAL_CASES_AUGUST8[0]
            elif data[row] == case:
                change_in_cases = data[row].total_cases - data[row - 1].total_cases

    return change_in_cases


def calculate_cases_in_fully_vaxx(data: list[VaccinatedCases]) -> dict[datetime.date, int]:
    """
    Calculate the cases in fully vaccinated individuals using the vaccination efficacy
    formula,
    Efficacy rate = ((cases among unvaccinated people / number of people not vaccinated) -
    (cases among vaccinated people / number of people vaccinated)) /
    (cases among unvaccinated people / number of people not vaccinated)

    >>> val = [VaccinatedCases(datetime.datetime(2021, 8, 9, 0, 0), 9343260,552804)]
    >>> calculate_cases_in_fully_vaxx(val)
    {datetime.datetime(2021, 8, 9, 0, 0): 19}

    >>> val2 = [VaccinatedCases(datetime.datetime(2021, 8, 9, 0, 0), 9343260,552804), \
    VaccinatedCases(datetime.datetime(2021, 8, 10, 0, 0), 1000000, 600000)]
    >>> calculate_cases_in_fully_vaxx(val2)
    {datetime.datetime(2021, 8, 9, 0, 0): 19, datetime.datetime(2021, 8, 10, 0, 0): 186}
    """
    fully_vaxx_cases = {}

    for row in data:
        vaccinated_cases = 0
        new_case = new_cases(data, row)

        for efficacy in VACCINATION_EFFICACY:
            num = row.total_vaccinated_people * VACCINE_ADMINISTERED[efficacy] * \
                  new_case * (VACCINATION_EFFICACY[efficacy] - 1)
            denom = (row.total_vaccinated_people * VACCINE_ADMINISTERED[efficacy]
                     * VACCINATION_EFFICACY[efficacy]) - POPULATION

            vaccinated_cases += (num / denom)

        fully_vaxx_cases[row.date] = int(vaccinated_cases)

    return fully_vaxx_cases


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['dataclasses', 'datetime', 'python_ta.contracts'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

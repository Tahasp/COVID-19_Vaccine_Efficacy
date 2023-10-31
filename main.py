from computations import VaccinatedCases
from computations import calculate_cases_in_fully_vaxx
import matplotlib.pyplot as plt
import csv
import datetime


def load_cases_data(cases_data: str) -> list[VaccinatedCases]:
    """Return a list of VaccinatedCases objects based on the data in cases_data."""
    cases_so_far = []

    with open(cases_data, newline='') as file:
        r = csv.reader(file)

        next(r)
        for row in r:
            d = str.split(row[0], '-')
            date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
            total_vaccinated_people = int(row[2])
            total_cases = int(row[3])

            cases_so_far.append(VaccinatedCases(date, total_vaccinated_people, total_cases))

    return cases_so_far


def load_real_data(cases_data: str) -> dict[datetime, int]:
    """Return a dictionary, mapping the date to the number of cases in the fully vaccinated
    population based on the data in cases_data.
    """
    cases_in_fully_vaxx = {}

    with open(cases_data, newline='') as file:
        r = csv.reader(file)

        next(r)
        for row in r:
            d = str.split(row[0], '-')
            date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))
            real_data_for_cases_in_fully_vaxx = int(row[1])

            cases_in_fully_vaxx[date] = real_data_for_cases_in_fully_vaxx

    return cases_in_fully_vaxx


def run_computations_ontario() -> dict[datetime, int]:
    """Return a dictionary, mapping the date to the estimated number of cases in the fully
    vaccinated population based on the vaccine efficacy formula."""
    file = load_cases_data('proj_data_ONTARIO.csv')
    return calculate_cases_in_fully_vaxx(file, 'Ontario')


def run_computations_nova_scotia() -> dict[datetime, int]:
    """Return a dictionary, mapping the date to the estimated number of cases in the fully
    vaccinated population based on the vaccine efficacy formula."""
    file = load_cases_data('proj_data_NOVA_SCOTIA.csv')
    return calculate_cases_in_fully_vaxx(file, 'Nova Scotia')


def run_ontario_graph() -> None:
    """Plot Graph Estimation VS Actual Data of COVID-19 Cases in Fully Vaccinated Individuals,
    showing the difference between the actual daily cases in the fully vaccinated population versus
    the the estimated daily cases in the fully vaccinated population"""

    # Coordinates based off the Vaccine Efficacy Formula
    coords = run_computations_ontario()

    x_values = coords.keys()  # dates
    y_values = coords.values()  # estimated cases in fully vaxx people

    plt.plot(x_values, y_values, color='navy', label='estimation')
    plt.scatter(x_values, y_values, color='navy')
    plt.fill_between(x_values, y_values, alpha=0.50, color='navy')

    # Coordinates based off of real life data
    real_coords = load_real_data('proj_data_ONTARIO.csv')
    real_x_values = real_coords.keys()  # dates
    real_y_values = real_coords.values()  # actual cases in fully vaxx people

    plt.plot(real_x_values, real_y_values, color='orange', label='real data')
    plt.scatter(real_x_values, real_y_values, color='orange')
    plt.fill_between(real_x_values, real_y_values, alpha=0.30, color='orange')

    # Graph Design
    fig = plt.gcf()
    fig.canvas.manager.set_window_title('Estimation VS Actual Data of COVID-19 Cases in Fully '
                                        'Vaccinated Individuals')
    fig.set_size_inches(19, 9)

    # Graph Info
    plt.title('Estimation VS Actual Data of COVID-19 Cases in Fully Vaccinated Individuals in '
              'Ontario')
    plt.xlabel('Date')
    plt.ylabel('COVID-19 Cases in Fully Vaccinated Individuals')
    plt.legend(loc='upper left')
    plt.show()


def run_nova_scotia_graph() -> None:
    """Plot Graph Estimation VS Actual Data of COVID-19 Cases in Fully Vaccinated Individuals,
    showing the difference between the actual daily cases in the fully vaccinated population versus
    the the estimated daily cases in the fully vaccinated population"""

    # Coordinates based off the Vaccine Efficacy Formula
    coords = run_computations_nova_scotia()

    x_values = coords.keys()  # dates
    y_values = coords.values()  # estimated cases in fully vaxx people

    plt.plot(x_values, y_values, color='orange', label='estimation')
    plt.scatter(x_values, y_values, color='orange')
    plt.fill_between(x_values, y_values, alpha=0.70, color='orange')

    # Coordinates based off of real life data
    real_coords = load_real_data('proj_data_NOVA_SCOTIA.csv')
    real_x_values = real_coords.keys()  # dates
    real_y_values = real_coords.values()  # actual cases in fully vaxx people

    plt.plot(real_x_values, real_y_values, color='purple', label='real data')
    plt.scatter(real_x_values, real_y_values, color='purple')
    plt.fill_between(real_x_values, real_y_values, alpha=0.30, color='purple')

    # Graph Design
    fig = plt.gcf()
    fig.canvas.manager.set_window_title('Estimation VS Actual Data of COVID-19 Cases in Fully '
                                        'Vaccinated Individuals')
    fig.set_size_inches(19, 9)

    # Graph Info
    plt.title('Estimation VS Actual Data of COVID-19 Cases in Fully Vaccinated Individuals in Nova '
              'Scotia')
    plt.xlabel('Date')
    plt.ylabel('COVID-19 Cases in Fully Vaccinated Individuals')
    plt.legend(loc='upper left')
    plt.show()

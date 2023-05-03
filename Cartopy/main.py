import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib import pyplot as plt


class FlightsMap:
    def __init__(self, precovid_flights, flights23, airports):
        """
        Initializes the FlightsMap class with CSV file paths for pre-Covid flights, flights in 2023, and airports data.
        """
        self.ax = None
        self.pre_covid_flights = pd.read_csv(precovid_flights, sep=";")
        self.flights_23 = pd.read_csv(flights23, sep=";")
        self.airports_data = pd.read_csv(airports, sep=",")

    def merge_flight_data(self):
        """
        Merges flight data with airport data and saves the merged datasets as new CSV files.
        """
        # Merge pre-Covid flight data with airport data using the IATA code as a common key
        pre_covid_merged = pd.merge(self.pre_covid_flights, self.airports_data, on='IATA')
        flights_23_merged = pd.merge(self.flights_23, self.airports_data, on='IATA')

        # Save the merged pre-Covid flight and 2023 flight data to a new CSV file
        pre_covid_merged.to_csv("pre_covid_flights.csv", index=False)
        flights_23_merged.to_csv("flights_23.csv", index=False)

    def create_map(self):
        """
        Creates the map with Lambert Cylindrical projection and adds coastlines and borders.
        """
        # Lambert Cylindrical projection
        proj = ccrs.LambertCylindrical()

        # map with the specified projection
        self.ax = plt.axes(projection=proj)

        # Set extent of the map
        self.ax.set_extent([-20, 45, 25, 70])

        # Add earth background image to the map
        self.ax.stock_img()

        # Add coastlines to the map
        self.ax.add_feature(cf.COASTLINE, lw=2)

        # country borders to the map
        self.ax.add_feature(cf.BORDERS)

        # Set figure size
        plt.gcf().set_size_inches(20, 10)

    @staticmethod
    def plot_flight_route(row, origin_longitude, origin_latitude, line_color, marker_color, marker, label=None,
                          line_style='-', alpha=1):
        """
        Plots a single flight route on the map using the provided parameters.
        """
        # Plot the flight route line between the origin and destination
        line, = plt.plot([origin_longitude, row['Longitude']], [origin_latitude, row['Latitude']], color=line_color,
                         marker=marker, linestyle=line_style, alpha=alpha,
                         transform=ccrs.Geodetic(), linewidth=2, markersize=10, label=label)

        # Add a scatter plot for the destination point
        plt.scatter(row['Longitude'], row['Latitude'], color=marker_color, marker=marker, transform=ccrs.Geodetic(),
                    s=30)

        # Add the IATA code as a text label next to the destination point
        plt.text(row['Longitude'], row['Latitude'], row['IATA'], transform=ccrs.Geodetic(), fontsize=12,
                 fontweight='bold')

        # Return the line object (useful for a legend)
        return line

    def display_map(self):
        """
        Creates the map, plots the pre-Covid and 2023 flights, adds a title and legend, saves the map as a PNG file,
        and displays the map.
        """
        # Create the map
        self.create_map()

        # Merge the pre-Covid and 2023 flights with airport coordinates
        pre_covid_coordinates = pd.merge(self.pre_covid_flights, self.airports_data[['Longitude', 'Latitude', 'IATA']],
                                         on='IATA')
        flight23_coordinates = pd.merge(self.flights_23, self.airports_data[['Longitude', 'Latitude', 'IATA']],
                                        on='IATA')

        # Define the coordinates for Tallinn (origin)
        tallinn_latitude = 59.4162
        tallinn_longitude = 24.8004

        # Plot the pre-Covid and 2023 flights on the map
        line1, line2 = self.plot_flight(flight23_coordinates, pre_covid_coordinates, tallinn_latitude,
                                        tallinn_longitude)

        # Add title and legend to the map
        self.title_and_legend(line1, line2)

        # Save the map as a PNG file
        plt.savefig("lennud.png")

        # Display the map
        plt.show()

    def title_and_legend(self, line1, line2):
        """
        Adds a title and legend to the map using the provided line objects.
        """
        # Define the title, subtitle, and author
        title = "Direct Flights from Tallinn\n"
        subtitle = "Yellow: 2020 (Pre-Covid) | Blue: 2023\n"
        author = "Glen Kink\n"

        # Add the title to the map
        plt.title(title + subtitle + author, fontsize=20)

        # Add the legend to the map
        plt.legend(handles=[line1, line2], loc='upper left', fontsize=12)

    def plot_flight(self, flight23_coordinates, pre_covid_coordinates, tallinn_latitude, tallinn_longitude):
        """
        Plots pre-Covid and 2023 flights on the map, and returns line objects for the legend.
        """
        # Plot pre-Covid flights on the map
        for index, row in pre_covid_coordinates.iterrows():
            self.plot_flight_route(row, tallinn_longitude, tallinn_latitude, line_color='yellow', marker_color='blue',
                                   marker='*', line_style='-', alpha=0.7)

        # Plot 2023 flights on the map
        for index, row in flight23_coordinates.iterrows():
            self.plot_flight_route(row, tallinn_longitude, tallinn_latitude, line_color='blue', marker_color='red',
                                   marker='*', line_style='--', alpha=0.7)

        # Create line objects for the legend
        line1 = plt.Line2D([], [], color='yellow', marker='*', linestyle='-', linewidth=5, markersize=10,
                           label='Pre-Covid (2020)')
        line2 = plt.Line2D([], [], color='blue', marker='*', linestyle='--', linewidth=2, markersize=10, label='2023')

        # Return line objects for the legend
        return line1, line2


flights_map = FlightsMap("otselennud20.csv", "otselennud23.csv", "airports.dat")

# Merge the datasets and save them to new CSV files
flights_map.merge_flight_data()

# Display and save the flights maps
flights_map.display_map()

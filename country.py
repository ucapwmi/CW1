from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from plotting_utilities import plot_country, plot_path

import math 

import numpy as np

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.figure import Figure

import warnings
def custom_warning_format(message, category, filename, lineno, line=None):
    return f"{message}\n"
warnings.formatwarning = custom_warning_format

def travel_time(
    distance,
    different_regions,
    locations_in_dest_region,
    speed = 4.75
):
    return 1/3600 * distance / speed * (1 + different_regions * locations_in_dest_region / 10)


class Location:
    def __init__(self, name:str, region:str, r, theta, depot) -> None:
        if not isinstance(name, str) or not isinstance(region, str):
            raise ValueError("name and region should be strings")
        # check whether the name and region should have each word in them capitalised, and remaining characters in each word should be lowercase. 
        formatted_name = name.title()
        formatted_region = region.title()


        if name != formatted_name:
            warnings.warn(f"The provided name '{name}' did not follow the required format and was reformatted to '{formatted_name}'.", UserWarning)
        if region != formatted_region:
            warnings.warn(f"The provided region '{region}' did not follow the required format and was reformatted to '{formatted_region}'.", UserWarning)


        if not isinstance(r, (int, float)) or r < 0:
            raise ValueError("r should be non-negative")
        
        if not isinstance(theta, (int, float)) or not -math.pi <= theta <= math.pi:
            raise ValueError("theta should between -π and π")
        
        if not isinstance(depot, bool):
            raise ValueError("depot should be boolean")
        
        self.name = formatted_name
        self.region = formatted_region
        self.r = float(r) #polar radius
        self.theta = float(theta) #polar angle, radius
        self.depot = depot
        
    @property
    def settlement(self) -> bool:
        return not self.depot
    def __repr__(self):
        """
        Do not edit this function.
        You are NOT required to document or test this function.

        Not all methods of printing variable values delegate to the
        __str__ method. This implementation ensures that they do,
        so you don't have to worry about Locations not being formatted
        correctly due to these internal Python caveats.
        """
        return self.__str__()

    def __str__(self):

        theta_over_pi = round(self.theta / math.pi, 2)
        
        if self.depot == True:
            return f"{self.name} [depot] in {self.region} @ ({round(self.r, 2)}m, {theta_over_pi}pi)"
        else:
            return f"{self.name} [settlement] in {self.region} @ ({round(self.r, 2)}m, {theta_over_pi}pi)"

    def distance_to(self, other):
        raise NotImplementedError


class Country:

    def travel_time(self, start_location, end_location):
        raise NotImplementedError

    def fastest_trip_from(
        self,
        current_location,
        potential_locations,
    ):
        raise NotImplementedError

    def nn_tour(self, starting_depot):
        raise NotImplementedError

    def best_depot_site(self, display):
        raise NotImplementedError

    def plot_country(
        self,
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """

        Plots the locations that make up the Country instance on a
        scale diagram, either displaying or saving the figure that is
        generated.

        Use the optional arguments to change the way the plot displays
        the information.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        distinguish_regions : bool, default: True
            If True, locations in different regions will use different
            marker colours.
        distinguish_depots bool, default: True
            If True, depot locations will be marked with crosses
            rather than circles.  Their labels will also be in
            CAPITALS, and underneath their markers, if not toggled
            off.
        location_names : bool, default: True
            If True, all locations will be annotated with their names.
        polar_projection : bool, default: True
            If True, the plot will display as a polar
            projection. Disable this if you would prefer the plot to
            be displayed in Cartesian (x,y) space.
        save_to : Path, str
            Providing a file name or path will result in the diagram
            being saved to that location. NOTE: This will suppress the
            display of the figure via matplotlib.
        """
        return plot_country(
            self,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )

    def plot_path(
        self,
        path: List[Location],
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """
        Plots the path provided on top of a diagram of the country,
        in order to visualise the path.

        Use the optional arguments to change the way the plot displays
        the information. Refer to the plot_country method for an
        explanation of the optional arguments.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        path : list
            A list of Locations in the country, where consecutive
            pairs are taken to mean journeys from the earlier location to
            the following one.
        distinguish_regions : bool, default: True,
        distinguish_depots : bool, default: True,
        location_names : bool, default: True,
        polar_projection : bool, default: True,
        save_to : Path, str

        See Also
        --------
        self.plot_path for a detailed description of the parameters
        """
        return plot_path(
            self,
            path,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )

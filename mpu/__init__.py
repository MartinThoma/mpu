"""mpu: Martins Python Utilities."""


# Core Library
import logging
import math as math_stl
import random
import traceback
from typing import Any, Callable, List, Tuple, Union

# First party
from mpu import io, shell, string, units  # noqa
from mpu._version import __version__  # noqa


def parallel_for(
    loop_function: Callable[[Any], Any],
    parameters: List[Tuple[Any, ...]],
    nb_threads: int = 100,
) -> List[Any]:
    """
    Execute the loop body in parallel.

    .. note:: Race-Conditions
          Executing code in parallel can cause an error class called
          "race-condition".

    Parameters
    ----------
    loop_function : Callable
        Python function which takes a tuple as input
    parameters : List[Tuple]
        Each element here should be executed in parallel.

    Returns
    -------
    return_values : list of return values
    """
    import multiprocessing.pool
    from contextlib import closing

    with closing(multiprocessing.pool.ThreadPool(nb_threads)) as pool:
        return pool.map(loop_function, parameters)


def clip(
    number: Union[int, float],
    lowest: Union[None, int, float] = None,
    highest: Union[None, int, float] = None,
) -> Union[int, float]:
    """
    Clip a number to a given lowest / highest value.

    Parameters
    ----------
    number : number
    lowest : number, optional
    highest : number, optional

    Returns
    -------
    clipped_number : number

    Examples
    --------
    >>> clip(42, lowest=0, highest=10)
    10
    """
    if lowest is not None:
        number = max(number, lowest)
    if highest is not None:
        number = min(number, highest)
    return number


def consistent_shuffle(*lists: List[List[Any]]) -> Tuple[List[Any], ...]:
    """
    Shuffle lists consistently.

    Parameters
    ----------
    *lists
        Variable length number of lists

    Returns
    -------
    shuffled_lists : tuple of lists
        All of the lists are shuffled consistently

    Examples
    --------
    >>> import mpu, random; random.seed(8)
    >>> mpu.consistent_shuffle([1,2,3], ['a', 'b', 'c'], ['A', 'B', 'C'])
    ([3, 2, 1], ['c', 'b', 'a'], ['C', 'B', 'A'])
    """
    perm = list(range(len(lists[0])))
    random.shuffle(perm)
    lists = tuple([sublist[index] for index in perm] for sublist in lists)
    return lists


class Location:
    """
    Define a single point.

    Parameters
    ----------
    latitude : float
        in [-90, 90] - from North to South
    longitude : float
        in [-180, 180] - from West to East
    """

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    @property
    def latitude(self) -> float:
        """Getter for latiutde."""
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        """Setter for latiutde."""
        if not (-90 <= latitude <= 90):
            raise ValueError(
                "latitude was {}, but has to be in [-90, 90]".format(latitude)
            )
        self._latitude = latitude

    @property
    def longitude(self) -> float:
        """Getter for longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        """Setter for longitude."""
        if not (-180 <= longitude <= 180):
            raise ValueError(
                "longitude was {}, but has to be in [-180, 180]".format(longitude)
            )
        self._longitude = longitude

    def get_google_maps_link(self):
        """Get a Google Maps link to this location."""
        return "https://www.google.com/maps/place/{},{}".format(
            self.latitude, self.longitude
        )

    def distance(self, there: "Location") -> float:
        """
        Calculate the distance from this location to there.

        Parameters
        ----------
        there : Location

        Returns
        -------
        distance_in_m : float
        """
        return haversine_distance(
            (self.latitude, self.longitude), (there.latitude, there.longitude)
        )

    def __repr__(self):
        """Get an unambiguous representation."""
        return "Location({}, {})".format(self.latitude, self.longitude)

    __str__ = __repr__


def haversine_distance(
    origin: Tuple[float, float], destination: Tuple[float, float]
) -> float:
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : Tuple[float, float]
        (lat, long)
    destination : Tuple[float, float]
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> munich = (48.1372, 11.5756)
    >>> berlin = (52.5186, 13.4083)
    >>> round(haversine_distance(munich, berlin), 1)
    504.2

    >>> new_york_city = (40.712777777778, -74.005833333333)  # NYC
    >>> round(haversine_distance(berlin, new_york_city), 1)
    6385.3
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    if not (-90.0 <= lat1 <= 90):
        raise ValueError("lat1={:2.2f}, but must be in [-90,+90]".format(lat1))
    if not (-90.0 <= lat2 <= 90):
        raise ValueError("lat2={:2.2f}, but must be in [-90,+90]".format(lat2))
    if not (-180.0 <= lon1 <= 180):
        raise ValueError("lon1={:2.2f}, but must be in [-180,+180]".format(lat1))
    if not (-180.0 <= lon2 <= 180):
        raise ValueError("lon1={:2.2f}, but must be in [-180,+180]".format(lat1))
    radius = 6371  # km

    dlat = math_stl.radians(lat2 - lat1)
    dlon = math_stl.radians(lon2 - lon1)
    a = math_stl.sin(dlat / 2) * math_stl.sin(dlat / 2) + math_stl.cos(
        math_stl.radians(lat1)
    ) * math_stl.cos(math_stl.radians(lat2)) * math_stl.sin(dlon / 2) * math_stl.sin(
        dlon / 2
    )
    c = 2 * math_stl.atan2(math_stl.sqrt(a), math_stl.sqrt(1 - a))
    d = radius * c

    return d


def is_in_intervall(value, min_value, max_value, name="variable"):
    """
    Raise an exception if value is not in an interval.

    Parameters
    ----------
    value : orderable
    min_value : orderable
    max_value : orderable
    name : str
        Name of the variable to print in exception.
    """
    if not (min_value <= value <= max_value):
        raise ValueError(
            "{}={} is not in [{}, {}]".format(name, value, min_value, max_value)
        )


def exception_logging(exctype, value, tb):
    """
    Log exception by using the root logger.

    Use it as `sys.excepthook = exception_logging`.

    Parameters
    ----------
    exctype : type
    value : NameError
    tb : traceback
    """
    write_val = {
        "exception_type": str(exctype),
        "message": str(traceback.format_tb(tb, 10)),
    }
    logging.exception(str(write_val))

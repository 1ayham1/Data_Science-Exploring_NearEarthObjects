"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, and handles missing names and unknown diameters.

"""
import math

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether
    it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        one implementation can be by defining default keys/values
        default =
        {"pdes":None,"name":None,"diameter":float("nan"),"pha":False}
        another can by by overriding __missing__ :D

        :param info:
            dictionary of excess keyword arguments supplied to the construct
        """

        self.designation = info.get("pdes")
        self.name = info.get("name")
        self.diameter = info.get("diameter", float('nan'))
        self.hazardous = info.get("pha", False)

        # Also set default values in case of return empty string
        self.name = self.name if self.name else None
        self.diameter = float(self.diameter) if self.diameter else float('nan')
        self.hazardous = False if self.hazardous in ['N', ''] else True

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        f_name = (
            f"{self.designation} :{self.name}"
            if self.name else self.designation
        )

        return f_name

    def __str__(self):
        """Return str(self),human-readable str representation of this obj."""

        hazard = "not" if not self.hazardous else ""
        diam_km = (
            f"has a diameter of {self.diameter:.3f} km "
            if not math.isnan(self.diameter)
            else "")

        msg = f"""A NearEarthObject.. {self.fullname} {diam_km} and is
         {hazard} potentially hazardous"""

        return msg

    def __repr__(self):
        """Return `repr(self)`,
            a computer-readable string representation of this object."""

        return (
            f"NearEarthObject(designation={self.designation!r}, "
            f"name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def __iter__(self):
        """helper to iterate and save objects"""

        serialized_obj = {"designation": self.designation, "name": self.name,
                          "diameter_km": self.diameter,
                          "potentially_hazardous": self.hazardous}

        # Handle edge cases:
        serialized_obj['name'] = (
            serialized_obj['name']
            if serialized_obj['name'] is not None
            else ''
        )

        serialized_obj["potentially_hazardous"] = bool(
            serialized_obj["potentially_hazardous"])

        if math.isnan(serialized_obj["diameter_km"]):
            serialized_obj["diameter_km"] = float('nan')

        serialized_obj = [serialized_obj]

        return iter(serialized_obj)


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative approach
    velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info:
            dictionary of excess keyword arguments supplied to the construct.
        """

        self._designation = info.get('des')
        self.time = cd_to_datetime(info.get('cd'))
        self.distance = info.get('dist', float("nan"))
        self.velocity = info.get('v_rel', float("nan"))

        # Also set default values in case of return empty string
        self.time = self.time if self.time else None
        self.distance = float(self.distance) if self.distance else float("nan")
        self.velocity = float(self.velocity) if self.velocity else float("nan")

        # Create an attribute for the referenced NEO, originally None.
        self.neo = info.get("neo", None)

    @property
    def get_designation(self):
        """getter to private attribute _designation"""

        return self._designation

    @property
    def time_str(self):
        """Return a formatted repr. of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default repr.
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """

        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`,
        a human-readable string representation of this object"""

        msg = f"""A CloseApproach: At {self.time_str},
         '{self.neo.fullname}' approaches Earth at a distance of
          {self.distance:.2f} au and a velocity of
           {self.velocity:.2f} km/s."""

        return msg

    def __repr__(self):
        """Return `repr(self)`,
        a computer-readable string representation of this object."""

        return (
            f"CloseApproach(time={self.time_str!r}, "
            f"distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def __iter__(self):
        """helper to iterate and save objects

        returns list of two dictionaries that compress fields of interest
        to be saved to either .json or .csv files
        """

        # approach dictionary that includes neo object
        extended_approach = [
            {
                "datetime_utc": datetime_to_str(self.time),
                "distance_au": self.distance,
                "velocity_km_s": self.velocity
            }]

        # encoded list of dictionary to fields of interest from neo object
        neo_dict = list(iter(self.neo))

        extended_approach.extend(neo_dict)

        return iter(extended_approach)

"""Provide filters for querying close approaches & limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of
interest from the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

"""
import operator
from itertools import islice


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach, or its attached NEO to a reference value. It
    essentially functions as a callable predicate for whether a
    `CloseApproach` object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter` from a binary predicate and
        a reference value.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        - <=, ==, or >= - available as operator.le, operator.eq, and
        operator.ge; i.e, operator.ge(a, b) is the same as a >= b.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against. It is supplied
         by the user
        at the command line and fed to create_filters by the main module.
        """

        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke self(approach)

        The __call__ method makes instance objects of this type behave as
        callables. With an instance of a subclass of AttributeFilter named f,
        then the code f(approach) evaluates f.__call__(approach). Specifically,
        "calling" the AttributeFilter with a CloseApproach object will get
        the attribute of interest (self.get(approach)) and compare
        it (via self.op) to the reference value (self.value), returning either
        True or False, representing whether that close approach satisfiesthe
        criterion.
        """

        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return:
            The value of an attribute of interest, comparable to
            `self.value` via `self.op`.
        """
        # one option is to make it also abstract
        raise UnsupportedCriterionError  # subclass of NotImplementedError

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(op=operator.{self.op.__name__},"
            f" value={self.value})"
        )


class DesignationFilter(AttributeFilter):
    """build an AttributeFilter that filtered on the designation attribute

     of the NearEarthObject attached to a CloseApproach,
     define a new subclass of AttributeFilter
     (This is only an example & not needed because primary
     designations are unique and we already have
     NEODatabase.get_neo_by_designation).

    """
    @classmethod
    def get(cls, approach):
        return approach.neo.designation


class DateFilters(AttributeFilter):
    """build an AttributeFilter that filtered on the Date attribute"""

    @classmethod
    def get(cls, approach):
        """
        for an input time (date, start_date, end_date), return the
        corrosponding approach.time and convert to date_time_obj
        """

        return approach.time.date()


class DistanceFilters(AttributeFilter):
    """build an AttributeFilter that filtered on Distance attribute"""

    @classmethod
    def get(cls, approach):
        """
        for an input distance (min,max), return the
        corrosponding approach.distance
        """
        return approach.distance


class VelocityFilters(AttributeFilter):
    """build an AttributeFilter that filtered on the velocity attribute"""

    @classmethod
    def get(cls, approach):
        """
        for an input Velocity (min,max), return the
        corrosponding approach.velocity
        """
        return approach.velocity


class DiameterFilters(AttributeFilter):
    """build an AttributeFilter that filtered on diameter attribute"""

    @classmethod
    def get(cls, approach):
        """
        for an input diameter (min,max), return the
        corrosponding approach.neo.diameter
        """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """build an AttributeFilter that filtered on hazardous attribute"""

    @classmethod
    def get(cls, approach):
        """
        for an input hazardous, return the
        corrosponding approach.neo.hazardous only if hazardous is not None
        """

        return approach.neo.hazardous


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value
    from the user's options at the command line. Each one corresponds to
    a different type of filter. For example, the `--date` option corresponds
    to the `date` argument, and represents a filter that selects close
    approaches that occured on exactly that given date. Similarly,
    the `--min-distance` option corresponds to the `distance_min` argument,
    and represents a filter that selects close approaches whose nominal
    approach distance is at least that far away from Earth. Each option
    is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results
    in `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of
    `NEODatabase` because the main module directly passes this result
    to that method. For now, this can be thought of as a collection of
    `AttributeFilter`s.

    :param date (datetime objects):
        A `date` on which a matching `CloseApproach` occurs.
    :param start_date:
        A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date:
        A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min (float):
        A min nominal approach distance for a matching `CloseApproach`.
    :param distance_max (float):
        A max nominal approach distance for a matching `CloseApproach`.
    :param velocity_min (float):
        A min relative approach velocity for a matching `CloseApproach`
    :param velocity_max (float):
        A max relative approach velocity for a matching `CloseApproach`
    :param diameter_min (float):
        A min diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max (float):
        A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous (bool):
        if the NEO of a matching `CloseApproach` is potentially hazardous.
    :return:
        A collection of filters for use with `query`.
    """

    filters_list = []

    if date:
        filters_list.append(DateFilters(operator.eq, date))

    if start_date:
        filters_list.append(DateFilters(operator.ge, start_date))

    if end_date:
        filters_list.append(DateFilters(operator.le, end_date))

    if distance_min:
        filters_list.append(DistanceFilters(operator.ge, distance_min))

    if distance_max:
        filters_list.append(DistanceFilters(operator.le, distance_max))

    if velocity_min:
        filters_list.append(VelocityFilters(operator.ge, velocity_min))

    if velocity_max:
        filters_list.append(VelocityFilters(operator.le, velocity_max))

    if diameter_min:
        filters_list.append(DiameterFilters(operator.ge, diameter_min))

    if diameter_max:
        filters_list.append(DiameterFilters(operator.le, diameter_max))

    if hazardous is not None:
        filters_list.append(HazardousFilter(operator.eq, hazardous))

    return filters_list


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """

    # don't limit the iterator at all
    if n == 0 or n is None:
        return iterator

    # else return first n elements from iterator:
    # https://stackoverflow.com/questions/26864008/simplest-way-to-get-the-first-n-elements-of-an-iterator

    return list(islice(iterator, n))

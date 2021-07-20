# PROG_Pyth-Exploring_NearEarthObjects

Python code that implements a command-line tool to inspect and query a dataset of Near Earth Objects (NEOs) and their close approaches to Earth. 

Input data is read from both a CSV file and a JSON file before it is converted into structured Python objects. Data is then fitlterd, analyzed and the results are written backto a file in a structured format, such as CSV or JSON.

Users are able to inspect the properties of the near-Earth objects in the data set and query the data set using any combination of the following filters:

* _**Object Temporal Queries**_:
  * Occurs on a given date.
  * Occurs on or after a given start date.
  * Occurs on or before a given end date.

* _**Object Spatial Queries**_:
  * Approaches Earth at a distance of at least (or at most) X astrononical units.
  * Approaches Earth at a relative velocity of at least (or at most) Y kilometers per second.
  * Has a diameter that is at least as large as (or at least as small as) Z kilometers.

* _**Object Type**_
  * Is marked by NASA as potentially hazardous (or not).

## Data Set

One dataset 'neos.csv' contains information about semantic, physical, orbital, and model parameters for certain small bodies (asteroids and comets, mostly) in our solar system. The other dataset (cad.json) contains information about NEO close approaches - moments in time when the orbit of an astronomical body brings it close to Earth. NASA helpfully provides a glossary to define any unfamiliar terms you might encounter.

Importantly, these datasets come directly from NASA - we haven't dressed them up for you at all.

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

The following [glossary](https://cneos.jpl.nasa.gov/glossary/) by NASA's Center for Near-Earth Object Studies (CNEOS)define the terms. Data is also from there. 

### `neos.csv` 
contains information about semantic, physical, orbital, and model parameters for certain small bodies (asteroids and comets, mostly) in our solar system.
 
 * NASA's Jet Propulsion Laboratory (JPL) provides a [web interface](https://ssd.jpl.nasa.gov/sbdb_query.cgi) to their database of "small bodies" - _mostly asteroids and comets_ - in the solar system. A subset of these small bodies are **near-Earth objects (NEOs)**: "comets and asteroids that have been nudged by the gravitational attraction of nearby planets into orbits that allow them to enter the Earth's neighborhood."[REF](https://cneos.jpl.nasa.gov/about/basics.html)
 
 * The data set comes directly from a query in which every output group is selected where "Object Group == NEOs". Result is: (__75 columns__). Following is an explanation for some:
   * _**pdes**_ - the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
   * _**name**_ - the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
   * _**pha**_ - whether NASA has marked the NEO as a "Potentially Hazardous Asteroid," roughly meaning that it's large and can come quite close to Earth.
   * _**diameter**_ - the NEO's diameter (from an equivalent sphere) in kilometers. 
 
 * From this dataset, one can answer questions such as:
   * what is the diameter of the Halley's Comet? or 
   * is the near-Earth object named 'Eros' potentially hazardous?

### `cad.json`
 A close approach occurs when a NEO's orbit path brings it near Earth -measured with the astronomical unit (au): the mean distance between the Earth and the sun. The data is JSON-formatted, downloaded it from NASA's public API. A description of the API, as well as details about the query parameters and the scheme of the returned data, can be found [here](https://ssd-api.jpl.nasa.gov/doc/cad.html). The query result in a data set contains all currently known close approaches that have happened or will happen in the 20th and 21st centuries! Additionally, NASA provides the data is in chronological order.

 * From this dataset, one can answer questions such as:
   * On which date(s) does Halley's Comet pass near to Earth? or 
   * How fast does Eros pass by Earth, on average?

Below is an initial look at the data in `cad.json`.

```
{
  "signature":{
    "source":"NASA/JPL SBDB Close Approach Data API",
    "version":"1.1"
  },
  "count":"406785",
  "fields":["des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf", "t_sigma_f", "h"],
  "data":[
    [
       "170903",
       "105",
       "2415020.507669610",
       "1900-Jan-01 00:11",
       "0.0921795123769547",
       "0.0912006569517418",
       "0.0931589328621254",
       "16.7523040362574",
       "16.7505784933163",
       "01:00",
       "18.1"
    ],
    [
       "2005 OE3",
       "52",
       "2415020.606013490",
       "1900-Jan-01 02:33",
       "0.414975519685102",
       "0.414968315685577",
       "0.414982724454678",
       "17.918395877175",
       "17.9180375373357",
       "< 00:01",
       "20.3"
    ],
    ...
  ]
}
```











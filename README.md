# Explore Close Approaches of Near-Earth Objects

## Overview

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

The following [glossary](https://cneos.jpl.nasa.gov/glossary/) by NASA's Center for Near-Earth Object Studies (CNEOS)define the terms. Data is also from there and is accessible in the Project Workspace lesson, under the `data/ folder`.

### Visual Exploration

NASA has [a tutorial video](https://www.youtube.com/watch?v=UA6voCyCW1g) on how to effectively navigate the CNEOS website, and an [interactive close approach data table](https://cneos.jpl.nasa.gov/ca/) that one can investigate. Data is updated frequently.

### `neos.csv` 
contains information about semantic, physical, orbital, and model parameters for certain small bodies (asteroids and comets, mostly) in our solar system.
 
* NASA's Jet Propulsion Laboratory (JPL) provides a [web interface](https://ssd.jpl.nasa.gov/sbdb_query.cgi) to their database of "small bodies" - _mostly asteroids and comets_ - in the solar system. A subset of these small bodies are **near-Earth objects (NEOs)**: "comets and asteroids that have been nudged by the gravitational attraction of nearby planets into orbits that allow them to enter the Earth's neighborhood."[REF](https://cneos.jpl.nasa.gov/about/basics.html)
 
* The data set comes directly from a query in which every output group is selected where "Object Group == NEOs". Result is: (__75 columns__). Following is an explanation for some:
   * _**pdes**_ - the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
   * _**name**_ - the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
   * _**pha**_ - whether NASA has marked the NEO as a "Potentially Hazardous Asteroid," roughly meaning that it's large and can come quite close to Earth.
   * _**diameter**_ - the NEO's diameter (from an equivalent sphere) in kilometers. 

 an initial look at the first three rows of `neos.csv`:

```
id,spkid,full_name,pdes,name,prefix,neo,pha,H,G,M1,M2,K1,K2,PC,diameter,extent,albedo,rot_per,GM,BV,UB,IR,spec_B,spec_T,H_sigma,diameter_sigma,orbit_id,epoch,epoch_mjd,epoch_cal,equinox,e,a,q,i,om,w,ma,ad,n,tp,tp_cal,per,per_y,moid,moid_ld,moid_jup,t_jup,sigma_e,sigma_a,sigma_q,sigma_i,sigma_om,sigma_w,sigma_ma,sigma_ad,sigma_n,sigma_tp,sigma_per,class,producer,data_arc,first_obs,last_obs,n_obs_used,n_del_obs_used,n_dop_obs_used,condition_code,rms,two_body,A1,A2,A3,DT
a0000433,2000433,"   433 Eros (A898 PA)",433,Eros,,Y,N,10.4,0.46,,,,,,16.84,34.4x11.2x11.2,0.25,5.270,4.463e-04,0.921,0.531,,S,S,,0.06,"JPL 658",2459000.5,59000,20200531.0000000,J2000,.2229512647434284,1.458045729081037,1.132972589728666,10.83054121829922,304.2993259000444,178.8822959227224,271.0717325705167,1.783118868433408,.5598186418120109,2459159.351922368362,20201105.8519224,643.0654021001488,1.76061711731731,.148623,57.83961291,3.2865,4.582,9.6497E-9,2.1374E-10,1.4063E-8,1.1645E-6,3.8525E-6,4.088E-6,1.4389E-6,2.6139E-10,1.231E-10,2.5792E-6,1.414E-7,AMO,Giorgini,46330,1893-10-29,2020-09-03,8767,4,2,0,.28397,,,,,
a0000719,2000719,"   719 Albert (A911 TB)",719,Albert,,Y,N,15.5,,,,,,,,,,5.801,,,,,S,,,,"JPL 214",2459000.5,59000,20200531.0000000,J2000,.5465584653041263,2.63860206439375,1.196451769530403,11.56748478123323,183.8669499802364,156.17633771,140.2734217745985,4.080752359257098,.2299551959241748,2458390.496728663387,20180928.9967287,1565.522355575327,4.28616661348481,.203482,79.18908994,1.41794,3.140,2.1784E-8,2.5313E-9,5.8116E-8,2.9108E-6,1.6575E-5,1.6827E-5,2.5213E-6,3.9148E-9,3.309E-10,1.0306E-5,2.2528E-6,AMO,"Otto Matic",39593,1911-10-04,2020-02-27,1874,,,0,.39148,,,,,
```
 * From this dataset, one can answer questions such as:
   * what is the diameter of the Halley's Comet? or 
   * is the near-Earth object named 'Eros' potentially hazardous?


### `cad.json`
 A close approach occurs when a NEO's orbit path brings it near Earth -measured with the astronomical unit (au): the mean distance between the Earth and the sun. The data is JSON-formatted, downloaded it from NASA's public API. A description of the API, as well as details about the query parameters and the scheme of the returned data, can be found [here](https://ssd-api.jpl.nasa.gov/doc/cad.html). The query result in a data set contains all currently known close approaches that have happened or will happen in the 20th and 21st centuries! Additionally, NASA provides the data is in chronological order.

Below is an initial look at the data in `cad.json`. The "signature" field shows where this data came from. The "count" field tells us how many entries to expect in the "data" section. The "fields" key maps to a list of strings describing how we should interpret the entries in the "data" section. Lastly, the "data" section itself maps to a list of lists - each element is a list of data for a single close approach, corresponding (by order) with the "fields" key.

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
[NASA's API documentation](https://ssd-api.jpl.nasa.gov/doc/cad.html) describes each field:

> * des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
> * orbit_id - orbit ID
> * jd - time of close-approach (JD Ephemeris Time)
> * cd - time of close-approach (formatted calendar date/time, in UTC)
> * dist - nominal approach distance (au)
> * dist_min - minimum (3-sigma) approach distance (au)
> * dist_max - maximum (3-sigma) approach distance (au)
> * v_rel - velocity relative to the approach body at close approach (km/s)
> * v_inf - velocity relative to a massless body (km/s)
> * t_sigma_f - 3-sigma uncertainty in the time of close-approach (formatted in days, hours, and minutes; days are not included if zero; example "13:02" is 13 hours 2 minutes; example "2_09:08" is 2 days 9 hours 8 minutes)
> * h - absolute magnitude H (mag)

Analysis will concentrate on _**des**_, _**cd**_, _**dist**_, and _**v_rel**_ measurements.

From this dataset, one can answer questions such as:
 * On which date(s) does Halley's Comet pass near to Earth? or 
 * How fast does Eros pass by Earth, on average?

## Project Interface

This project is driven by the `main.py` script. run `python3 main.py ... ... ...` at the command line to invoke the program that will the code. Run `python3 main.py --help` for an explanation of how to invoke the script.

```
usage: main.py [-h] [--neofile NEOFILE] [--cadfile CADFILE] {inspect,query,interactive} ...

Explore past and future close approaches of near-Earth objects.

positional arguments:
  {inspect,query,interactive}

optional arguments:
  -h, --help            show this help message and exit
  --neofile NEOFILE     Path to CSV file of near-Earth objects.
  --cadfile CADFILE     Path to JSON file of close approach data.
```
The three subcommands: `inspect`, `query`, and `interactive`, are explained below:












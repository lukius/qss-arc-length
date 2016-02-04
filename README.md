## Arc length for QSS numerical integrators 

### Description

This is a proof of concept of arc length computation for the [QSS3 numerical integrator](https://en.wikipedia.org/wiki/Quantized_state_systems_method).

### Usage

* The class `QSS3ArcLength` can be used to calculate the arc length of a QSS3 curve given two collections of tuples that represent the polynomial sections of both `q_x` and `q_y`. These tuples are of the form `(q_i, t0_i, t1_i)`, where `q_i` contains the coefficients of the polynomial that approximates `x` (or `y`) between `t0_i` and `t1_i`.
* The class `QSS3ArcLengthFromLogFile` receives a log file (format to be described soon) and the indices of `q_x` and `q_y` and parses the content of the log in order to build the aforementioned collections of tuples.
* Since the arc length of every polynomial section has to be calculated, a class hierarchy that handles polynomial arc length calculations is also provided.

### Limitations 

* Only two-dimensional parametric curves are supported, but the code can be easily adapted to deal with higher dimensions.
* QSS3 is the only member of the QSS family currently supported. 

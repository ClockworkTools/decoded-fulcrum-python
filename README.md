# decoded-fulcrum-python

A library for working with [Fulcrum API](http://fulcrumapp.com/developers/api/).

This modifies the behaviour of the core [Fulcrum](https://github.com/fulcrumapp/fulcrum-python) class by producing and
consuming Json where the form field's "keys" have been replaced with their respective "data_names".

Further, a new "schemas" end point is provided which serves Python Schema Objects with utilities for conveniently
retrieving  information regarding the content and structure of Application forms

## Installation

    python setup.py install


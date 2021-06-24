# codeastro-group6

This project allows a user to input a celestial object name and receive a postage stamp image of the target, pulled from one of the HIPS surveys using the CDS's hips2fits utility.

Currently, there is a single method that can be used by the user.

Example: from pyhips import get_image

get_image(id, frame, survey)

id - the SIMBAD resolvable ID of the target

frame - the coordinate frame desired

survey - the HIPS survey to pull images from. Currently forced to be DSS


There's some issue with my local codeastro conda environment where the QT backend for matplotlib isn't working correctly. Needs more external testing.
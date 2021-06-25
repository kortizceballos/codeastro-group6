# codeastro-group6

This project allows a user to input a celestial object name and receive a postage stamp image of the target, pulled from one of the HIPS surveys using the CDS's hips2fits utility.

Required packages: numpy, matplotlib, astropy, astroquery

We recommend that users preinstall these, especially astropy and astroquery, as pip may struggle with their release models.

Currently, there is a single method that can be used by the user.

Example: from pyhips import get_image

get_image(id, frame, survey, cmap, fov)

id - the SIMBAD resolvable ID of the target

frame - the coordinate frame desired. default "ICRS"

survey - the HIPS survey to pull images from. default "DSS"

cmap - the matplotlib colormap to use for plotting. default "gray"

fov - the field of view of the desired image in degrees. default 1.0

There's some issue with my local codeastro conda environment where the QT backend for matplotlib isn't working correctly. The plots save correctly, but don't show in my x server. Needs more external testing.
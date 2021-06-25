"""Simple Python interface to the hips2fits service provided by the Centre de Données astronomiques de Strasbourg"""

import sys
from astroquery.simbad import Simbad
from astropy.io import fits
import astropy.units as u

import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord

from urllib.parse import quote
from urllib.parse import urlencode
import numpy as np


class Target(object):
    """
        Object to store information about the desired imaging target.

        Args:
            id (string): SIMBAD resolvable identifier
            frame (string): coordinate frame to use (default ICRS)
            survey (string): HiPS survey to grab data from (default DSS)
    """
    def __init__(self, id, frame="ICRS", survey=None):
        self.id = id
        self.main_id = None
        self.frame = frame
        self.otype = None
        self.sptype = None
        self.coords = None
        self.survey = survey

        # custom simbad object to handle query - modified votable fields
        self.simbad = Simbad()
        self.simbad.remove_votable_fields("coordinates")
        self.simbad.add_votable_fields("otype", "sp")
    def resolve_name(self):
        """
        Function to resolve target name in SIMBAD, and populate the instance variables with their relevant values.

        Return:
            int: status code 0 for successful operation, 1 for error. If an error is returned, it will likely have been printed to stdout
        """
        try:
            self.coords = SkyCoord.from_name(self.id, frame=self.frame.lower())
            results = self.simbad.query_object(self.id)
            self.otype = results["OTYPE"][0]
            self.sptype = results["SP_TYPE"][0]
            self.main_id = results["MAIN_ID"][0]
            return 0
        except Exception as e:
            print(e)
            return(1)


# testing query functionality. try this in your codeastro environment
def get_image(id, frame="ICRS", survey="DSS", cmap="gray", fov=1.0):
    """
        Function to query hips2fits for an image. Plots, saves the image as a JPEG (fig.jpg).

        Args:
            id (string): SIMBAD resolvable identifier
            frame (string): coordinate frame to use (default ICRS)
            survey (string): HiPS survey to grab data from (default DSS)
            cmap (string): matplotlib colormap to use when plotting (default "gray")
            fov (float): field of view of image (in degrees, default 1.0)

        Return:
            int: status code 0 for successful operation, 1 for error. If an error is returned, it will likely have been printed to stdout
    """

    id = id
    frame = frame
    survey = survey
    cmap = cmap

    # instantiate target object
    tgt = Target(id=id, frame=frame, survey=survey)

    # resolve target name, if this fails, quit execution and return the error code
    code = tgt.resolve_name()
    if code != 0:
        return(1)
    
    # make hips2fits query to be placed in url
    query_params = {
        'hips': tgt.survey,
        'object': tgt.id,
        'ra': tgt.coords.ra.value,
        'dec': tgt.coords.dec.value,
        'fov': (fov * u.deg).to(u.deg).value,
        'width': 500,
        'height': 500,
    }

    url = f'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?{urlencode(query_params)}'
    try:
        # try grabbing the fits file and plotting it.
        hdu = fits.open(url)

        im = hdu[0].data

        fig = plt.figure()
        ax=plt.gca()
        ax.imshow(im, origin='lower', cmap=cmap)
        plt.title(f"{tgt.main_id}: {tgt.survey}")
        fig.savefig("fig.jpg", dpi=200)
        return(0)
    except Exception as e:
        # if the above failed, print the error and quit
        print(e)
        return(1)

# TODO: grid_builder() - given a list of surveys, plot all of them together as subplots

# TODO: followup_plotter() - takes a single survey, sets up figure and axes, reloads desired FITS file, plots the data as above
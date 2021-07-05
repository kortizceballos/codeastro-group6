"""Simple Python interface to the hips2fits service provided by the Centre de Données astronomiques de Strasbourg"""

import sys
import argparse
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

# grid_builder() - given a list of surveys, plot all of them together as subplots for a particular object
def grid_builder(id, frame="ICRS", survey_list = ['DSS', 'DSS2/red', 'CDS/P/AKARI/FIS/N160', 'PanSTARRS/DR1/z', '2MASS/J', 'AllWISE/W3'], cmap="gray", fov=1.0):
    """
        Function to build grid of get_image images. Plots the grid, saves the image as a JPEG (fig.jpg).

        Args:
            id (string): SIMBAD resolvable identifier
            frame (string): coordinate frame to use (default ICRS)
            survey_list (list): HiPS surveys to grab data from (default DSS, DSS2/red, CDS/P/AKARI/FIS/N160, PanSTARRS/DR1/z, 2MASS/J and AllWISE/W3)
            cmap (string): matplotlib colormap to use when plotting (default "gray")
            fov (float): field of view of images (in degrees, default 1.0)

        Return:
            int: status code 0 for successful operation, 1 for error. If an error is returned, it will likely have been printed to stdout
    """

    # instantiate target object
    tgt = Target(id=id, frame=frame, survey='DSS')

    # resolve target name, if this fails, quit execution and return the error code
    code = tgt.resolve_name()
    if code != 0:
        return(1)

    # make the figure for the grid
    fig, axs = plt.subplots(1, len(survey_list), figsize=(4 * len(survey_list), 3), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace = .2, wspace=.001)

    axs = axs.ravel()
    i=0
    for survey in survey_list:

        # make hips2fits query to be placed in url
        query_params = {
            'hips': survey,
            'object': tgt.id,
            'ra': tgt.coords.ra.value,
            'dec': tgt.coords.dec.value,
            'fov': (fov * u.deg).to(u.deg).value,
            'width': 500,
            'height': 500,
        }

        url = f'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?{urlencode(query_params)}'

        axs[i].set_title('{} - {}'.format(tgt.main_id, survey))
    
        hdu = fits.open(url)
        im = hdu[0].data
        axs[i].imshow(im, origin='lower', cmap=cmap)
        
        i += 1
    fig.tight_layout()
    fig.savefig(f"{tgt.main_id}" + "_grid.jpg", dpi=200)
    return(0)

    # TODO: need to add error exception

# removed follow-up plotter since get_image makes it redundant

# Creating the parser
my_parser = argparse.ArgumentParser(prog = 'PyHiPS', description='Show a target in the sky as seen by a HiPS survey.')

# Adding the arguments
my_parser.add_argument('Target',
                       metavar='Target Name',
                       type=str,
                       help='The target name to be resolved')

my_parser.add_argument('--frame',
                       action='store',
                       metavar='Frame Name',
                       type=str,
                       default='ICRS',
                       help='The name of the frame')

my_parser.add_argument('--survey', '--surveys',
                       action='store',
                       metavar='Survey Name(s)',
                       type=list,
                       default=['DSS'],
                       help='The name of the desired survey (or several names if using --grid)')

my_parser.add_argument('--cmap',
                       action='store',
                       metavar='Colormap',
                       type=str,
                       default='gray',
                       help='The name of the colormap')

my_parser.add_argument('--fov',
                       action='store',
                       metavar='Field of View',
                       type=float,
                       default=1.0,
                       help='The field of view')

my_parser.add_argument('-g', '--grid',
                       action='store_true',
                       metavar='Save multi-survey grid',
                       help='Used to save a grid with several surveys instead of a single image')

# Execute parse_args()
args = my_parser.parse_args()

# Define main() process for running from command line
def main():
    if args.grid:
        grid_builder(args.Target, frame=args.frame, survey_list=args.survey, cmap=args.cmap, fov=args.fov)
    else:
        get_image(args.Target, frame=args.frame, survey=args.survey[0], cmap=args.cmap, fov=args.fov)

#  Run main if program is run from the command line
if __name__ == '__main__':
    main()


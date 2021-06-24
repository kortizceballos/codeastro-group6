"""Simple Python interface to the hips2fits service provided by the Centre de Données astronomiques de Strasbourg"""

import sys
from astroquery.simbad import Simbad
from astropy.io import fits
import astropy.units as u

import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
#from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)
from urllib.parse import quote
from urllib.parse import urlencode
import numpy as np
#from astropy.visualization import (MinMaxInterval, SqrtStretch, AsinhStretch, ImageNormalize)

class Target(object):
    """
        Object to store information about the desired imaging target.

        Args:
            id (string): SIMBAD resolvable identifier
            frame (string): coordinate frame to use (default ICRS)
    """
    def __init__(self, id, frame="ICRS", survey=None):
        self.id = id
        self.main_id = None
        self.frame = frame
        self.coords = SkyCoord.from_name(self.id, frame=self.frame.lower())
        self.otype = None
        self.sptype = None

        self.survey = None

        # custom simbad object to handle query - modified votable fields
        self.simbad = Simbad()
        self.simbad.remove_votable_fields("coordinates")
        self.simbad.add_votable_fields("otype", "sp")

    def resolve_name(self):
        results = self.simbad.query_object(self.id)
        self.otype = results["OTYPE"][0]
        self.sptype = results["SP_TYPE"][0]
        self.main_id = results["MAIN_ID"][0]

# testing query functionality. try this in your codeastro environment
def get_image(id, frame="ICRS", survey=None):
    id = id
    frame = frame
    survey = survey

    # instantiate target object
    tgt = Target(id=id, frame=frame, survey=survey)
    tgt.resolve_name()

    # make hips2fits query
    query_params = {
        'hips': 'DSS',
        'object': tgt.id,
        'ra': tgt.coords.ra.value,
        'dec': tgt.coords.dec.value,
        'fov': (2 * u.arcmin).to(u.deg).value,
        'width': 500,
        'height': 500,
    }

    url = f'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?{urlencode(query_params)}'
    print(url)
    hdu = fits.open(url)
    print(hdu[0])

    im = hdu[0].data
    #norm = ImageNormalize(im, interval=MinMaxInterval(), stretch=AsinhStretch())
    print(im)
    fig = plt.figure()
    ax=plt.gca()
    ax.imshow(im, cmap='viridis', origin='lower')

def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("Usage: %s [options]" % sys.argv[0])
        print("\toptions:")
        print("\t--help (-h)\t\t\tprint options")
        print("\t-id [string]\t\t\trequired, target identifier")
        print("\t-frame [string]\t\t\toptional, coordinate frame. default \"ICRS\"")
        print()
        sys.exit(1)

    if "-id" in sys.argv:
        ind = sys.argv.index("-id")
        id = sys.argv[ind+1]
    else:
        print("Target ID Required.")
        sys.exit(1)

    if "-frame" in sys.argv:
        ind = sys.argv.index("-frame")
        frame = sys.argv[ind+1]

    if "-survey" in sys.argv:
        ind = sys.argv.index("-survey")
        survey = sys.argv[ind+1]

    get_image(id, frame, survey)


if __name__ == "__main__":
    main()
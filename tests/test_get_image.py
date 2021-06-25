from matplotlib.pyplot import get
import pyhips
from pyhips import get_image


def test_get_image():
    """
    Tests the get_image() function to make sure no errors are thrown.
    """

    assert get_image("Vega", frame="ICRS", survey="DSS", cmap="plasma") == 0
    assert get_image("notanid", frame="ICRS", survey="DSS", cmap="plasma") == 1
    assert get_image("Vega", frame="notaframe", survey="DSS", cmap="plasma") == 1
    assert get_image("Vega", frame="ICRS", survey="notasurvey", cmap="plasma") == 1
    assert get_image("Vega", frame="ICRS", survey="DSS", cmap="notacolormap") == 1
    
if __name__ == "__main__":
    test_get_image()
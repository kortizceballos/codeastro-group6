import numpy as np
import matplotlib.pyplot as plt




earth = {
	"name": "earth",
	"r_star": 6.957E5, # km # solar
	"r_planet": 6.3710E3, # km 
	"pl_dist": 1.4959826E8, # km # AU, a(1-e^2)/(1+ecos(theta))	
}

moon = {
	"name": "moon",
	"r_star": 6.957E5, # meters # solar
	"r_planet": 1.7374E3, # meters 
	"pl_dist": 1.4959826E8, # meters # AU, a(1-e^2)/(1+ecos(theta))	
}

jupiter = {
	"name": "jupiter",
	"r_star": 6.957E5, # meters # solar
	"r_planet": 6.9911E4, # meters 
	"pl_dist": 7.7834082E8, # meters # AU, a(1-e^2)/(1+ecos(theta))	
}

ganymede = {
	"name": "ganymede",
	"r_star": 6.957E5, # meters # solar
	"r_planet": 2.684E3, # meters 
	"pl_dist": 7.7834082E8, # meters # AU, a(1-e^2)/(1+ecos(theta))	
}

# get orbit data from JPL horizons, calculate angles over all phases of the planetary orbits
# maybe use astropy to convert between coordinate systems
# figure out how to get to moons from horizons


def calc_TZ(planet):
	r_star = planet["r_star"]
	r_planet = planet["r_planet"]
	pl_dist = planet["pl_dist"]

	transit_angle = 2*(np.arctan(r_star/pl_dist) - np.arcsin(r_planet/(np.sqrt((pl_dist*pl_dist) + (r_star*r_star)))))

	grazing_angle = 2*np.arctan((r_planet+r_star)/pl_dist)

	depth = ((r_planet**2 / r_star**2)) * 100

	print("{}: {} deg, {} deg, {:.4f} ppm transit depth".format(planet["name"], np.rad2deg(transit_angle), np.rad2deg(grazing_angle), depth*1e4))


calc_TZ(earth)
calc_TZ(moon)
calc_TZ(jupiter)
calc_TZ(ganymede)
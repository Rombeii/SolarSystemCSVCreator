from skyfield.api import load
from skyfield.framelib import itrs
from datetime import date, timedelta
import csv


def get_planets_row(t):
    planets = load('de440s.bsp')
    earth = planets['earth']
    barycentric_earth = earth.at(t)

    return [get_planet_row(planets['sun'], barycentric_earth),
            get_planet_row(planets['mercury'], barycentric_earth),
            get_planet_row(planets['venus'], barycentric_earth),
            get_planet_row(planets['moon'], barycentric_earth),
            get_planet_row(planets['mars barycenter'], barycentric_earth),
            get_planet_row(planets['jupiter barycenter'], barycentric_earth),
            get_planet_row(planets['saturn barycenter'], barycentric_earth),
            get_planet_row(planets['uranus barycenter'], barycentric_earth),
            get_planet_row(planets['neptune barycenter'], barycentric_earth),
            get_planet_row(planets['pluto barycenter'], barycentric_earth)]


def get_planet_row(planet, barycentric_earth):
    astrometric = barycentric_earth.observe(planet)
    apparent = astrometric.apparent()
    rotated_position = apparent.frame_xyz(itrs)

    return str(rotated_position.km[0] / SCALE) + ' / ' + str(rotated_position.km[2] / SCALE) + ' / ' + str(
        rotated_position.km[1] / SCALE)


def daterange(from_date, until_date):
    for n in range(int((until_date - from_date).days)):
        yield from_date + timedelta(n)


if __name__ == '__main__':
    start_date = date(2020, 1, 1)
    end_date = date(2030, 12, 31)
    observations_at = [0, 8, 16]
    observatory_angles = ["10", "10", "10", "10", "10", "10", "10", "10"]
    object_diameters = ["1.39139998", "0.0048794", "0.0121036", "0.0034748", "0.006779",
                        "0.139822006", "0.116463996", "0.050724", "0.049244002", "0.0023766"]
    object_importance = ["1", "1", "1", "1", "1",
                         "1", "1", "1", "1", "1"]
    SCALE = 1000000
    ts = load.timescale()

    with open('planetPositions.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(observatory_angles)
        writer.writerow(object_diameters)
        writer.writerow(object_importance)
        for single_date in daterange(start_date, end_date):
            observation_dates = ts.utc(int(single_date.year), int(single_date.month), int(single_date.day),
                                       observations_at)
            for t in observation_dates:
                writer.writerow(get_planets_row(t))

"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import terrain


class CommonTerrainUtils:
    """ Utilities for manipulating the Terrain. """

    @staticmethod
    def get_water_depth_at(x: float, z: float, surface_level: int=0) -> float:
        """get_water_depth_at(x, z, surface_level=0)

        Determine the water depth at the specified coordinates.

        :param x: The X coordinate.
        :type x: float
        :param z: The Z coordinate.
        :type z: float
        :param surface_level: The surface level. Default is 0.
        :type surface_level: int, optional
        :return: The depth of the water at the specified coordinates.
        :rtype: float
        """
        return terrain.get_water_depth(x, z, level=surface_level)

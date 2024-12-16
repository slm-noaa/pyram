# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 18:49:56 2023

@author: caplinje-noaa

Input data organization schema

Modified by slm-noaa
Thurs Dec 5 24
"""

# import numpy as np
# from dataclasses import dataclass, field


class sourceInputs:
    """grid inputs
    defaults are initialized from test case supplied with RAM
    """

    freq: float = 25.0  # frequency in Hz
    zs: float = 40.0  # source depth
    zr: float = 30.0  # reciever depth


class gridInputs:
    """grid inputs
    defaults are initialized from example ram.in
    """

    rmax: float = 4000.0  # Maximum range
    dr: float = 5.0  # range step
    ndr: int = 1  # range output step

    zmax: float = 1000.0  # Maximum depth
    dz: float = 1.0  # depth step
    ndz: int = 2  # depth output step


class ramInputs:
    """other more general inputs
    defaults are initialized from example ram.in
    """

    c0: float = 1500.0  # reference sound speed (m/s)
    npd: int = 8  # number of pade steps
    ns: int = 1  # stability constraint
    rs: float = 0.0  # radius of stability
    irot: int = -1  # stability option, (0 or 1) *only for rams
    theta: int = -1  # stability option, (0 to 90 degrees) *only for rams
    zmplt: float = 1000.0  # max depth for output
    ramver: str = field(
        default_factory=list
    )  # internally used to select version of RAM
    # 'geo', '15p', '15', 'geop','rams'


class bathData:
    """bathymetry
    defaults are initialized from example ramgeo.in
    """

    z: list = field(default_factory=list)  # depth array (m)
    r: list = field(default_factory=list)  # range array (m)


class soundSpeedProfile:
    """sound speed profiles for water and bottom
    defaults are initialized from example ramgeo.in
    """

    w: list = field(default_factory=list)  # sound speed in water (m/s)
    zw: list = field(default_factory=list)  # depth at water ss point
    b: list = field(default_factory=list)  # sound speed in seabed (m/s)
    bs: list = field(default_factory=list)  # sound speed in seabed (m/s)
    zb: list = field(default_factory=list)  # depth at seabed ss point
    zbs: list = field(default_factory=list)  # depth at seabed ss point
    r: float = 0.0


class seabedProperties:
    """sound speed profiles for water and bottom
    defaults are initialized from example ramgeo.in
    """

    rhob: list = field(default_factory=list)  # density of seabed layers
    attn: list = field(default_factory=list)  # attenuation of seabed layers
    attns: list = field(
        default_factory=list
    )  # shear wave attenuation of seabed layers
    z_rhob: list = field(default_factory=list)  # depth of layers
    z_attn: list = field(default_factory=list)  # depth of layers
    z_attns: list = field(default_factory=list)  # depth of layers
    r: float = 0.0  # range point for definitions


class inputContainer:
    source: sourceInputs = sourceInputs()
    ram: ramInputs = ramInputs()
    grid: gridInputs = gridInputs()
    bath: bathData = bathData()
    soundSpeeds: [soundSpeedProfile] = field(default_factory=list)
    seabeds: [seabedProperties] = field(default_factory=list)

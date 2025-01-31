# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 18:49:56 2023

@author: caplinje-noaa

Input data organization schema

Modified by slm-noaa
Thurs Dec 5 24
"""

# from dataclasses import dataclass, field
# use dataclass later maybe to neaten this up and add some checks.
from dataclasses import field


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


class physicalProperties:
    """Refactor this a little bit... group physical properties then
    we can define "water", "seabed", whatever with said properties.
    We can even pre-define default materials.
    """

    r: float = 0.0  # range for this description (or ranges)
    z: list = field(default_factory=list)  # depth grid for this material (m)
    c: list = field(default_factory=list)  # (compressional) sound speed (m/s)
    cs: list = field(default_factory=list)  # (shear) sound speed (m/s)
    rho: list = field(default_factory=list)  # density (g/cc)
    attn: list = field(
        default_factory=list
    )  # (compressional) attenuation (dB/wavelength)
    attns: list = field(
        default_factory=list
    )  # (shear) attenuation (dB/wavelength)


class inputContainer:
    source: sourceInputs = sourceInputs()
    ram: ramInputs = ramInputs()
    grid: gridInputs = gridInputs()
    bath: bathData = bathData()
    watercol: physicalProperties = physicalProperties()
    seabed: physicalProperties = physicalProperties()

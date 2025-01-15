# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:21:38 2022

@author: jim
"""
import logging
import yaml
from importlib import resources as impresources
from . import Tests
from operator import itemgetter

# from dataclasses import dataclass, field
from pyram.RAMinput import inputContainer

logger = logging.getLogger("bluRAM.readRAM")

# get relative path and find input data
# ramver='org'
inFolder = impresources.files(Tests)

hasFields = {
    "geo": False,
    "15p": True,
    "15": False,
    "geop": True,
    "rams": True,
}
geoGrid = {
    "geo": True,
    "15p": False,
    "15": False,
    "geop": False,
    "rams": False,
}
isGeo = {"geo": True, "15p": False, "15": False, "geop": True, "rams": False}
shearWaves = {
    "geo": False,
    "15p": False,
    "15": False,
    "geop": False,
    "rams": True,
}
inputfn = {
    "geo": "ramgeo.in",
    "15p": "ram.in",
    "15": "ram.in",
    "geop": "ramgeo.in",
    "rams": "rams.in",
    "test": "ramOriginal.yaml",
}

"""
class dataContainer:
    rVector: list = field(default_factory=list)
    zVector: list = field(default_factory=list)
    TLgrid: list = field(default_factory=list)
    TLline: list = field(default_factory=list)
    bath: bathData = bathData()
    seabed: seabedProperties = seabedProperties()
    outpath: Path
"""


def read(ramver: str = "test"):
    logging.debug("Reading RAM data.")

    inputPath = inFolder / inputfn[ramver]
    inData = inputContainer()

    # Read input deck
    with inputPath.open() as f:
        raminput = yaml.load(f, Loader=yaml.SafeLoader)

    scenario_txt = raminput.get("description")
    print("unpacking input data for ", scenario_txt)

    modeldata = raminput.get("model")
    sourcedata = raminput.get("source")
    griddata = raminput.get("grid")
    envdata = raminput.get("environment")

    (inData.source.freq, inData.source.zs, inData.source.zr) = itemgetter(
        "freq", "zs", "zr"
    )(sourcedata)

    rangedata, depthdata = itemgetter("range", "depth")(griddata)
    inData.grid.rmax, inData.grid.dr, inData.grid.ndr = itemgetter(
        "rmax", "dr", "ndr"
    )(rangedata)
    inData.grid.zmax, inData.grid.dz, inData.grid.ndz = itemgetter(
        "zmax", "dz", "ndz"
    )(depthdata)

    (
        inData.ram.c0,
        inData.ram.npd,
        inData.ram.zmplt,
        inData.ram.ns,
        inData.ram.rs,
    ) = itemgetter("c0", "np", "zmplt", "ns", "rs")(modeldata)

    inData.bath.r, inData.bath.z, r_ssp = itemgetter("rb", "zb", "r_ssp")(
        envdata
    )

    inData.watercol.r = r_ssp
    inData.seabed.r = r_ssp

    tempdata = itemgetter("env")(envdata)

    inData.watercol.z, inData.watercol.c = itemgetter("z_ssp", "cw_ssp")(
        tempdata
    )
    inData.watercol.cs = 0.0
    inData.watercol.rho = 1.024
    inData.watercol.attn = 0.0
    inData.watercol.attns = 0.0

    inData.seabed.z, inData.seabed.c = itemgetter("zb", "cb_ssp")(tempdata)
    inData.seabed.cs = 0.0
    inData.seabed.rho = itemgetter("rhob")(tempdata)
    inData.seabed.attn = itemgetter("attn")(tempdata)
    inData.seabed.attns = 0.0

    return inData

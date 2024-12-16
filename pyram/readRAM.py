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

# import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from pyram.RAMinput import bathData, seabedProperties, inputContainer

# from .ioTools.readOutputs import (
#    readTLgrid,
#    readTLgrid_geo,
#    readTLline,
#    readField,
# )

logger = logging.getLogger("bluRAM.readRAM")

# get relative path and find input data
# ramver='org'
inFolder = impresources.files(Tests)

# gridfn = r"tl.grid"
# linefn = r"tl.line"
# fieldfn = r"u.grid"

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


class dataContainer:
    rVector: list = field(default_factory=list)
    zVector: list = field(default_factory=list)
    TLgrid: list = field(default_factory=list)
    TLline: list = field(default_factory=list)
    bath: bathData = bathData()
    seabed: seabedProperties = seabedProperties()
    outpath: Path


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

    rb, zb = itemgetter("rb", "zb")(envdata)

    """
        # Read bathymetry inputs
        bathSection = True
        rbath = []
        zbath = []
        while bathSection == True:
            line = f.readline()
            split = line.split(" ")
            if float(split[0]) == -1:
                bathSection = False
                continue
            else:
                rbath.append(float(split[0]))  # range of bath data point
                zbath.append(float(split[1]))  # depth points
        # put bathymetry in data container
        data.bath.r = np.array(rbath)
        data.bath.z = np.array(zbath)
        data.bath.n = len(rbath)

        # read water sound speed profile
        cwSection = True
        zcw = []
        cw = []
        while cwSection == True:
            line = f.readline()
            split = line.split(" ")
            if float(split[0]) == -1:
                cwSection = False
                continue
            else:
                zcw.append(
                    float(split[0])
                )  # depth array for sound speed in water
                cw.append(float(split[1]))  # water sound speed array
        zcw = np.array(zcw)
        cw = np.array(cw)

        # read bottom sound speed profile
        cbSection = True
        zcb = []
        cb = []
        while cbSection == True:
            line = f.readline()
            split = line.split(" ")
            if float(split[0]) == -1:
                cbSection = False
                continue
            else:
                zcb.append(
                    float(split[0])
                )  # depth array for bottom sound speed
                cb.append(float(split[1]))  # bottom sound speed array
        zcb = np.array(zcb)
        cb = np.array(cb)

        # read bottom layer densities
        rhoSection = True
        zrhob = []
        rhob = []
        while rhoSection == True:
            line = f.readline()
            split = line.split(" ")
            if float(split[0]) == -1:
                rhoSection = False
                continue
            else:
                zrhob.append(
                    float(split[0])
                )  # depth array for bottom sound speed
                rhob.append(float(split[1]))  # bottom sound speed array
        zrhob = np.array(zcb)
        rhob = np.array(cb)
        # put data in container
        data.seabed.z = np.array(zrhob)
        data.seabed.rhob = np.array(rhob)
        data.seabed.n = len(zrhob)

        # read bottom layer attenuation
        attnSection = True
        zattn = []
        attn = []
        while attnSection == True:
            line = f.readline()
            split = line.split(" ")
            if float(split[0]) == -1:
                attnSection = False
                continue
            else:
                zattn.append(
                    float(split[0])
                )  # depth array for bottom sound speed
                attn.append(float(split[1]))  # bottom sound speed array
        # put data in container
        data.seabed.z = np.array(zattn)
        data.seabed.attn = np.array(attn)
        data.seabed.n = len(zattn)
    """
    # # Read field file
    # if hasFields[ramver]:
    #     data.field = readField(fieldPath)
    #     logger.debug(f"read field of shape {data.field.shape}")
    # # Read tl.line and tl.grid file
    # if geoGrid[ramver]:
    #     data.TLgrid = readTLgrid_geo(gridPath)
    # else:
    #     data.lz, data.grid, data.general, data.TLgrid = readTLgrid(
    #         gridPath, rams=shearWaves[ramver]
    #     )

    # # r vector taken from line file, no issues there
    # data.rVector, data.TLline = readTLline(linePath)
    # # calculate implied r length
    # n_r = int(rmax / (dr * ndr))
    # if ndr > 1:
    #     data.rVector_line = data.rVector
    #     data.rVector = np.linspace(dr, rmax, num=data.TLgrid.shape[1])

    # if isGeo[ramver] or shearWaves[ramver]:
    #     # as defined in the fortran code, number of z points (before applying ndz stepping) to depth zmplt
    #     nzplt = int(zmplt / dz - 0.5)
    #     # expected number of z points in read grid
    #     # added minus 1 to make rams work, probably needs additional vetting
    #     n_z = int((zmplt / dz - 0.5) / ndz) - 1
    # else:
    #     # some earlier versions of ram do not output the last depth, so a modified version of nzplt is below
    #     nzplt = int(zmplt / dz)
    #     n_z = int((zmplt / dz) / ndz)

    # logger.debug(f"Read TLgrid data with shape = {data.TLgrid.shape}.")
    # if not data.TLgrid.shape == ((n_z, n_r)):
    #     msg = f"Output grid shape ({data.TLgrid.shape}) does not match input ({(n_z,n_r)}!"
    #     logger.critical(msg)
    # raise Warning(f'Output grid shape ({data.TLgrid.shape}) does not match input ({(n_z,n_r)}!')

    ## still not sure about this grid definition
    # it appears the fortran code starts at dr and ends at rmax,
    # though error relative to georam example is improved when starting at zero
    # z grid definition is likely correct, based on z=0 relating to i=1 in fortran
    # and the fact that this statement (below) mirrors the print statement in fortran
    # further testing should include
    # measure source depth from output and correlate
    # match line output at reciever depth and correlate
    # the issues are amplified by the fact that some version of ram don't print the last depth
    # if shearWaves[ramver]:
    #     data.zVector = (
    #         np.array(range(int(ndz), int(nzplt), int(ndz))) - 1
    #     ) * dz
    # else:
    #     data.zVector = (
    #         np.array(range(int(ndz), int(nzplt + 1), int(ndz))) - 1
    #     ) * dz

    # return data

"""TestPyRAM class definition"""

import unittest
import numpy
from pyram.PyRAM import PyRAM
import pyram.readRAM as reader
from scipy.linalg import lu_factor, lu_solve
from pyram.RAMinput import (
    inputContainer,
    bathData,
    soundSpeedProfile,
    seabedProperties,
    sourceInputs,
    gridInputs,
    ramInputs,
)

ramver = "test"


class TestPyRAM(unittest.TestCase):
    """
    Test PyRAM using the test case supplied with RAM.
    """

    def setUp(self):
        reader.read()
        self.inputs = inputContainer()

        # source inputs
        self.inputs.sourceInputs.freq = 50.0
        self.inputs.sourceInputs.zs = 50.0
        self.inputs.sourceInputs.zr = 50.0

        # grid inputs
        self.inputs.gridInputs.rmax = 50000.0
        self.inputs.gridInputs.dr = 500.0
        self.inputs.gridInputs.ndr = 1
        self.inputs.gridInputs.dz = 2.0

        # ramInputs
        self.inputs.ramInputs.c0 = 1600.0
        # self.inputs.npd =
        self.inputs.ramInputs.zmplt = 500.0
        self.inputs.ramInputs.ramver = ramver

        # bathData
        self.inputs.bath.z = numpy.array([0])
        self.inputs.bath.r = numpy.array([0])

        # soundSpeedProfile
        self.inputs.soundSpeeds.w = numpy.array(
            [[1480, 1530], [1520, 1530], [1530, 1530]]
        )
        self.inputs.soundSpeeds.zw = numpy.array([0, 100, 400])
        # self.inputs.soundSpeeds.b =

        """ z_ss=numpy.array([0, 100, 400]),
            rp_ss=numpy.array([0, 25000]),
            cw=numpy.array([[1480, 1530], [1520, 1530], [1530, 1530]]),
            z_sb=numpy.array([0]),
            rp_sb=numpy.array([0]),
            cb=numpy.array([[1700]]),
            rhob=numpy.array([[1.5]]),
            attn=numpy.array([[0.5]]),

            rbzb=numpy.array([[0, 200], [40000, 400]]),
        )"""

        ref_tl_file = "tl_ref.line"
        dat = numpy.fromfile(ref_tl_file, sep="\t").reshape([100, 2])
        self.ref_r, self.ref_tl = dat[:, 0], dat[:, 1]

        self.tl_tol = (
            1e-3  # Tolerable mean difference in TL (dB) with reference result
        )
        self.LU_tol = 1e-10  # Tolerable l2 error in linear algebra solver

    def tearDown(self):
        pass

    def test_PyRAM(self):

        pyram = PyRAM(
            self.inputs["freq"],
            self.inputs["zs"],
            self.inputs["zr"],
            self.inputs["z_ss"],
            self.inputs["rp_ss"],
            self.inputs["cw"],
            self.inputs["z_sb"],
            self.inputs["rp_sb"],
            self.inputs["cb"],
            self.inputs["rhob"],
            self.inputs["attn"],
            self.inputs["rbzb"],
            rmax=self.inputs["rmax"],
            dr=self.inputs["dr"],
            dz=self.inputs["dz"],
            zmplt=self.inputs["zmplt"],
            c0=self.inputs["c0"],
        )
        pyram.run()

        with open("tl.line", "w") as fid:
            for ran in range(len(pyram.vr)):
                fid.write(
                    str(pyram.vr[ran]) + "\t" + str(pyram.tll[ran]) + "\n"
                )

        self.assertTrue(
            numpy.array_equal(self.ref_r, pyram.vr), "Ranges are not equal"
        )

        mean_diff = numpy.mean(numpy.abs(pyram.tll - self.ref_tl))
        self.assertTrue(
            mean_diff <= self.tl_tol,
            "Mean TL difference with reference result not within tolerance",
        )


if __name__ == "__main__":
    unittest.main()

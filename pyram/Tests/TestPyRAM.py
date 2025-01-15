"""TestPyRAM class definition"""

import unittest
import numpy
from pyram.PyRAM import PyRAM
import pyram.readRAM as reader
from scipy.linalg import lu_factor, lu_solve
from pyram.RAMinput import (
    inputContainer,
)

ramver = "test"


class TestPyRAM(unittest.TestCase):
    """
    Test PyRAM using the test case supplied with RAM.
    """

    def setUp(self):
        self.inputs = reader.read()
        self.inputs.ram.ramver = ramver

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
            self.inputs,
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

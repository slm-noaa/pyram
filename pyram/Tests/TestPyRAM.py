"""TestPyRAM class definition"""

import unittest
import numpy
from pyram.PyRAM import PyRAM
from scipy.linalg import lu_factor, lu_solve


class TestPyRAM(unittest.TestCase):
    """
    Test PyRAM using the test case supplied with RAM.
    """

    def setUp(self):

        self.inputs = dict(
            freq=50,
            zs=50,
            zr=50,
            z_ss=numpy.array([0, 100, 400]),
            rp_ss=numpy.array([0, 25000]),
            cw=numpy.array([[1480, 1530], [1520, 1530], [1530, 1530]]),
            z_sb=numpy.array([0]),
            rp_sb=numpy.array([0]),
            cb=numpy.array([[1700]]),
            rhob=numpy.array([[1.5]]),
            attn=numpy.array([[0.5]]),
            rmax=50000,
            dr=500,
            dz=2,
            zmplt=500,
            c0=1600,
            rbzb=numpy.array([[0, 200], [40000, 400]]),
        )

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

    def test_PyRAM_replacesolver(self):
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
            use_splinalg=False,
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

    def test_gauss_elim(self):
        n = 4  # Test n x n matrix
        A = numpy.array(
            [
                [2.0, 1.0, -2.0, 0.0],
                [3.0, 0.0, 1.0, 0.0],
                [1.0, 1.0, -1.0, 0.0],
                numpy.zeros((1, n))[0],
            ]
        )
        x = numpy.array([1.0, -1.0, 2.0])
        Aslice = A[: n - 1, : n - 1]
        b = numpy.dot(Aslice, x)
        LU, piv = lu_factor(Aslice)
        x1 = lu_solve((LU, piv), b)
        dum, x2 = PyRAM.gauss(3, A, b, PyRAM.pivot)
        err = numpy.sqrt(numpy.dot(x1 - x2, x1 - x2))
        self.assertTrue(
            err <= self.LU_tol, "Gauss elim not matching LU factorization"
        )


if __name__ == "__main__":
    unittest.main()

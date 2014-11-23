# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 17:20:30 2014

@author: Andreea
"""
import numpy as np
import math
from globalfnc import *

#TODO Add XE
FFdefault = np.array([[lambda y: 0]*2]*2)
FFSigmaPPJ = {(19, 9): np.array([[lambda y: 0.90278 - 2.37144 * y + 2.3531 * y**2 - 1.04517 * y**3 + 0.175359 * y**4, \
                        lambda y: -0.0165506 + 0.050948 * y - 0.0510308 * y**2 + 0.0199287 * y**3 - 0.00236734 * y*4], \
                        [lambda y: -0.0165506 + 0.050948 * y - 0.0510308 * y**2 + 0.0199287 * y**3 - 0.00236734 * y**4, \
                        lambda y: 0.000303421 - 0.00107102 * y + 0.00114207 * y**2 - 0.000347594 * y**3 + 0.000031959 * y**4]]),
            (23, 11): np.array([[lambda y: 0.136361 - 0.266817 * y + 0.457598 * y**2 - 0.112141 * y**3 + 0.00828489 * y**4, \
                        lambda y: 0.0109688 - 0.029996 * y + 0.0217192 * y**2 - 0.00897498 * y**3 + 0.000591796 * y**4], \
                        [lambda y: 0.0109688 - 0.029996 * y + 0.0217192 * y**2 - 0.00897498 * y**3 + 0.000591796 * y**4, \
                        lambda y: 0.000882318 - 0.00309927 * y + 0.00398861 * y**2 - 0.00203246 * y**3 + 0.00040932 * y**4]]),
            (73, 32): np.array([[lambda y: 0.000102041 - 0.00096119 * y + 0.00335189 * y**2 - 0.00364089 * y**3 + 0.0019991 * y**4 - 0.000462685 * y**5 + 0.000040244 * y**6 - 3.45152*10**-7 * y**7 + 1.2863*10**-9 * y**8, \
                        lambda y: 0.00612884 - 0.0386733 * y + 0.0575045 * y**2 - 0.0535467 * y**3 + 0.0257882 * y**4 - 0.0065118 * y**5 + 0.000816404 * y**6 - 0.0000402374 * y**7 + 7.36917*10**-7 * y**8], \
                        [lambda y: 0.00612884 - 0.0386733 * y + 0.0575045 * y**2 - 0.0535467 * y**3 + 0.0257882 * y**4 - 0.0065118 * y**5 + 0.000816404 * y**6 - 0.0000402374 * y**7 + 7.36917*10**-7 * y**8, \
                        lambda y: 0.368112 - 1.17814 * y + 2.27237 * y**2 - 1.98163 * y**3 + 1.01909 * y**4 - 0.296483 * y**5 + 0.056608 * y**6 - 0.00599025 * y**7 + 0.000951084 * y**8]]),
            (127, 53): np.array([[lambda y: 0.130131 - 0.488539 * y + 1.83369 * y**2 - 2.79561 * y**3 + 2.70421 * y**4 - 1.58275 * y**5 + 0.528399 * y**6 - 0.0920503 * y**7 + 0.00666861 * y**8 - 6.28403*10**-12 * y**9 + 1.3501*10**-20 * y**10, \
                        lambda y: 0.0322868 - 0.125179 * y + 0.26445 * y**2 - 0.296832 * y**3 + 0.214155 * y**4 - 0.0982407 * y**5 + 0.0271252 * y**6 - 0.00422686 * y**7 + 0.000330271 * y**8 - 9.72551*10**-6 * y**9 + 1.02434*10**-14 * y**10], \
                        [lambda y: 0.0322868 - 0.125179 * y + 0.26445 * y**2 - 0.296832 * y**3 + 0.214155 * y**4 - 0.0982407 * y**5 + 0.0271252 * y**6 - 0.00422686 * y**7 + 0.000330271 * y**8 - 9.72551*10**-6 * y**9 + 1.02434*10**-14 * y**10, \
                        lambda y: 0.00801063 - 0.0320427 * y + 0.0534333 * y**2 - 0.0461654 * y**3 + 0.0247382 * y**4 - 0.00858068 * y**5 + 0.00190294 * y**6 - 0.000262031 * y**7 + 0.0000213702 * y**8 - 9.3627*10**-7 * y**9 + 1.68751*10**-8 * y**10]]),
            (129, 54): np.array([[lambda y: 0.000210575 - 0.00150295 * y + 0.00431238 * y**2 - 0.00630033 * y**3 + 0.00491101 * y**4 - 0.00199528 * y**5 + 0.00041825 * y**6 - 0.0000422967 * y**7 + 1.6268*10**-6 * y**8 + 3.31573*10**-14 * y**9 + 1.68953*10**-22 * y**10, \
                        lambda y: 0.00720992 - 0.0380102 * y + 0.0824299 * y**2 - 0.0971526 * y**3 + 0.067932 * y**4 - 0.0271548 * y**5 + 0.00613825 * y**6 - 0.000734195 * y**7 + 0.0000354172 * y**8 - 7.27679*10**-8 * y**9 - 7.41579*10**-16 * y**10], \
                        [lambda y: 0.00720992 - 0.0380102 * y + 0.0824299 * y**2 - 0.0971526 * y**3 + 0.067932 * y**4 - 0.0271548 * y**5 + 0.00613825 * y**6 - 0.000734195 * y**7 + 0.0000354172 * y**8 - 7.27679*10**-8 * y**9 - 7.41579*10**-16 * y**10, \
                        lambda y: 0.246862 - 0.840937 * y + 1.4482 * y**2 - 1.46722 * y**3 + 0.944902 * y**4 - 0.37255 * y**5 + 0.0890997 * y**6 - 0.0120716 * y**7 + 0.000755735 * y**8 - 3.08386*10**-6 * y**9 + 3.255*10**-9 * y**10]]),
            (131, 54): np.array([[lambda y: 0.0000578995 - 0.000032744 * y + 0.000127388 * y**2 - 0.000624606 * y**3 + 0.000875357 * y**4 - 0.000528633 * y**5 + 0.000151948 * y**6 - 0.0000197785 * y**7 + 9.38122*10**-7 * y**8 - 1.04681*10**-13 * y**9 + 5.94262*10**-21 * y**10, \
                        lambda y: 0.00225524 + 0.00315534 * y - 0.0106065 * y**2 - 0.000772228 * y**3 + 0.0192839 * y**4 - 0.0176928 * y**5 + 0.00663425 * y**6 - 0.00112357 * y**7 + 0.0000683327 * y**8 - 3.76191*10**-8 * y**9 + 3.59162*10**-15 * y**10], \
                        [lambda y: 0.00225524 + 0.00315534 * y - 0.0106065 * y**2 - 0.000772228 * y**3 + 0.0192839 * y**4 - 0.0176928 * y**5 + 0.00663425 * y**6 - 0.00112357 * y**7 + 0.0000683327 * y**8 - 3.76191*10**-8 * y**9 + 3.59162*10**-15 * y**10, \
                        lambda y: 0.0878436 + 0.295485 * y - 0.232083 * y**2 - 0.4651 * y**3 + 1.24324 * y**4 - 1.07229 * y**5 + 0.438103 * y**6 - 0.085951 * y**7 + 0.006652 * y**8 - 7.67519*10**-6 * y**9 + 2.24565*10**-9 * y**10]]),
}

def FFElementQ(Z):
    #check = [math.trunc(z) in np.array([9, 11, 32, 53, 54]) for z in Z]
    #return np.array([1 if c else 0 for c in check])
    return np.array([1] * Z.size)

def FF66normlalized(ER, A, Z, mT, N1, N2):
    bsq = 41.467/(45. * A**(-1./3) - 25. * A**(-2./3)) * fermiGeV**2
    y = 2.e-6 * mT * ER * bsq / 4.
    FFdef = np.array([[lambda y: 0]*2]*2)
    l =  map(lambda a, z, i: FFSigmaPPJ.get((np.trunc(a), np.trunc(z)), FFdef)[N1, N2](i), A, Z, y)
    return np.array(l) * np.exp(-2. * y)





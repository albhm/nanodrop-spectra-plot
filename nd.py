#!/usr/bin/python

#  most of the code is from a lecture of a member of the Straw lab at IMP :
#  http://py4science.strawlab.org/_static/py4science-vbc-2012-03-09.pdf
#  github.com/strawlab/py4science-vbc/

#  I just adapted it to actually work with the .tsv files exported by a Nanodrop 2000c

#  Please adjust the wavelength boundaries (FREQ_FROM, FREQ_TO) according to your nanodrop settings

import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


STATE_SKIP, _, _, STATE_SPEC_NAME, STATE_SPEC_DATE, _, STATE_DATA = range(7)
FREQ_FROM, FREQ_TO = 220, 350


spectrum_names = [] 
def func():
	state = STATE_SPEC_NAME
	for line in open(sys.argv[1],"r"):
		if state == STATE_SPEC_NAME: 
			spectrum_names.append(line.strip())
		elif state == STATE_DATA:
			wavelength, absorbance = line.strip().split() 
			yield absorbance
			if int(wavelength) == (FREQ_TO - 1):
				state = STATE_SKIP 
			continue
		state += 1
data = np.fromiter(func(), float)

wavelengths = np.arange(FREQ_FROM, FREQ_TO)
spectra = data.reshape(len(spectrum_names), FREQ_TO - FREQ_FROM).transpose()


ax = plt.axes(xlim=(FREQ_FROM, FREQ_TO))
ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.minorticks_on
ax.grid(True, which='both')

plt.ylabel("Absorption")
plt.xlabel("Wavelength [nm]")

plt.plot(wavelengths, spectra)
plt.legend(spectrum_names, loc=1)

plt.show()

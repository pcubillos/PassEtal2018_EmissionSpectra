import sys
import os
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d as gaussf
import matplotlib
import matplotlib.pyplot as plt
import ConfigParser as cp
plt.ioff()

sys.path.append("pyratbay")
import pyratbay.starspec   as ps
import pyratbay.constants  as pc
import pyratbay.atmosphere as pa


# Extract files:
allfiles = sorted(os.listdir("./run02/"))
flag = np.zeros(len(allfiles), bool)
for i in np.arange(len(allfiles)):
  if allfiles[i].endswith("_radeq.atm"):
    flag[i] = True
files = np.array(allfiles)[flag]
# Remove extension:
for i in np.arange(len(files)):
  files[i] = files[i].replace("_radeq.atm", "")

# Reshape into [Nplanet,Nmodel]:
nfiles = len(files)
nmodels = 6
nplanets = nfiles//nmodels
files = files.reshape((nplanets,nmodels))

# Planet names:
planet = np.zeros(nplanets, "|S50")
for i in np.arange(nplanets):
  planet[i] = files[i,0].split("_")[0]


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Plot temperature profiles:
dash = ["",    "",     "",
        (7,2), (7,2), (7,2)]
col = ["navy", "r", "limegreen",
       "navy", "r", "limegreen"]

# Planet index:
for j in np.arange(nplanets):
  plt.figure(0)
  plt.clf()
  ax = plt.subplot(111)
  for i in np.arange(nmodels):
    metal = "{:g}".format(float(files[j,i].split("_")[2][0:4]))
    albedo = files[j,i].split("_")[1]
    spec, press, temp, q = pa.readatm("run02/"+files[j,i]+"_radeq.atm")
    plt.plot(temp, press, label="{}x  {}".format(metal, albedo),
             color=col[i], dashes=dash[i])
  plt.yscale("log")
  plt.ylim(100, 1e-8)
  plt.xlim(300, 3000.0)
  plt.text(0.98, 0.95, planet[j], transform=ax.transAxes, ha="right")
  plt.legend(loc="lower left", fontsize=9)
  plt.xlabel("Temperature (K)")
  plt.ylabel("Pressure (bar)")
  plt.savefig("./plots/{}_thermo-rad-equil_temperature.png".format(planet[j]))


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Plot spectra:
wn, dummy = ps.readpyrat("run02/"+files[0,0]+"_radeq.dat")

sigma = 1.5  # Smoothing
col2 = ["navy", "r",      "g",
        "b",    "orange", "limegreen", ]

for j in np.arange(nplanets):
  config = cp.SafeConfigParser()
  config.read(["run02/"+files[j,0]+".cfg"])
  # Stellar model as a blackbody:
  starflux = ps.bbflux(wn, config.getfloat("pyrat", "tstar"))
  rprs = ( float(config.get("pyrat","rplanet").split()[0]) * pc.rjup /
          (float(config.get("pyrat","rstar"  ).split()[0]) * pc.rsun))
  plt.figure(1)
  plt.clf()
  plt.subplots_adjust(0.15, 0.1, 0.95, 0.95)
  ax = plt.subplot(111)
  for i in np.arange(nmodels):
    metal = "{:g}".format(float(files[j,i].split("_")[2][0:4]))
    albedo = files[j,i].split("_")[1]
    wl, spectrum = ps.readpyrat("run02/"+files[j,i]+"_radeq.dat", False)
    plt.plot(wl, gaussf(spectrum/starflux, sigma)*rprs**2, lw= 1.0, 
             label="{:04.1f}x  {}".format(float(metal), albedo), color=col2[i])
  plt.xscale("log")
  plt.gca().xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
  ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
  plt.xticks([0.5, 1, 2, 4, 10, 20])
  plt.text(0.98, 0.05, planet[j], transform=ax.transAxes, ha="right")
  plt.xlim(np.amin(wl), np.amax(wl))
  plt.legend(loc="upper left", fontsize=9)
  plt.xlabel("Wavelength (um)")
  plt.ylabel("Flux ratio")
  plt.savefig("./plots/{}_thermo-rad-equil_fluxratio.png".format(planet[j]))


#! /usr/bin/env python
import numpy as np

import astropy.table as at


def findreplace(name, size):
  """
  Find the digit characters in name, replace them with a zero-padded
  number of length size.

  Example
  -------
  >>> s = findreplace(name="WASP-43b", size=3)
  >>> print(s)
  WASP-043b
  """
  # Find digits in name:
  digits = filter(str.isdigit, name)
  # Zero-pad update:
  zerodigs = "{:0{}d}".format(int(digits), size)
  # Replace:
  return name.replace(digits, zerodigs)


# This script generates the Pyrat-Bay radeq configuration files by
# editing a template with the values taken from the CSV table.

# Get list of planets:
sample = at.Table.read("../inputs/exoplanet-parameters.csv", comment="#")
planets = sample["NAME" ].data
rstar   = sample["RSTAR"].data
mstar   = sample["MSTAR"].data
tstar   = sample["TEFF" ].data
rplanet = sample["R"    ].data
mplanet = sample["MASS" ].data
smaxis  = sample["A"    ].data

# Update planet name:
nplanets = len(planets)
for i in np.arange(nplanets):
  planets[i] = planets[i].replace(" ","")
  # Zero-pad to have consistent name:
  if planets[i].startswith("HAT"):
    planets[i] = findreplace(planets[i], size=2)
  if planets[i].startswith("Kepler"):
    planets[i] = findreplace(planets[i], size=3)
  if planets[i].startswith("WASP"):
    planets[i] = findreplace(planets[i], size=3)
  if planets[i].startswith("HD"):
    planets[i] = findreplace(planets[i], size=6)

# Read cfg template:
with open("radeq_template.cfg", "r") as f:
  template = f.readlines()
for i in np.arange(len(template)):
  if template[i].startswith("rstar"):
    irs = i
  if template[i].startswith("mstar"):
    ims = i
  if template[i].startswith("tstar"):
    its = i
  if template[i].startswith("rplanet"):
    irp = i
  if template[i].startswith("mplanet"):
    imp = i
  if template[i].startswith("smaxis"):
    isma = i
  if template[i].startswith("xsolar"):
    imetal = i
  if template[i].startswith("beta"):
    ibeta = i
  if template[i].startswith("atmfile"):
    iatm = i
  if template[i].startswith("logfile"):
    ilog = i
  if template[i].startswith("outspec"):
    ispec = i

albedo = [0.0, 0.3]
metal  = [0.1, 1.0, 10.0]

nalbedo  = len(albedo)
nmetal   = len(metal)
nplanets = len(planets)

print(iatm)
for i in np.arange(nplanets):
  for j in np.arange(nalbedo):
    for k in np.arange(nmetal):
      cfg = np.copy(template)
      ofile = ("{:s}_{:.1f}A_{:04.1f}xsolar".
               format(planets[i], albedo[j], metal[k]))
      # Replace values:
      cfg[imetal] = "xsolar = {:.1f}\n".format(metal[k])
      cfg[ibeta]  = "beta   = {:.1f}\n".format(1.0-albedo[j])
      cfg[its]    = "tstar    = {:4.0f}\n".format(tstar[i])
      cfg[irs]    = "rstar    = {:.3f} rsun\n".format(rstar[i])
      cfg[ims]    = "mstar    = {:.3f} msun\n".format(mstar[i])
      cfg[irp]    = "rplanet  = {:.3f} rjup\n".format(rplanet[i])
      cfg[imp]    = "mplanet  = {:.3f} mjup\n".format(mplanet[i])
      cfg[isma]   = "smaxis   = {:.4f} au\n".format(smaxis[i])
      cfg[iatm]   = "atmfile = {:s}_radeq.atm\n".format(ofile)
      cfg[ilog]   = "logfile = {:s}_radeq.log\n".format(ofile)
      cfg[ispec]  = "outspec = {:s}_radeq.dat\n".format(ofile)
      with open("../run02/{:s}.cfg".format(ofile), "w") as f:
        f.writelines(cfg)



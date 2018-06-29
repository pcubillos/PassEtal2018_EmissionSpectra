# Define topdir (in your top working directory) to make your life easier:
topdir=`pwd`

# Clone (download) the necessary code:
git clone --recursive https://github.com/pcubillos/pyratbay
cd $topdir/pyratbay
git checkout bb64088
make

cd $topdir
git clone https://github.com/pcubillos/repack
cd $topdir/repack
git checkout 65132bd
make

# Download CH4/NH3/HCN ExoMol data:
cd $topdir/inputs
wget -i wget_exomol_NH3.txt
wget -i wget_exomol_CH4.txt
wget -i wget_exomol_HCN.txt

# Download H2O/CO2 HITEMP data:
cd $topdir/inputs
wget --user=HITRAN --password=getdata -N -i wget_hitemp_H2O_CO2.txt
unzip '*.zip'
rm -f *.zip

# Download CO data:
cd $topdir/inputs
wget http://iopscience.iop.org/0067-0049/216/1/15/suppdata/apjs504015_data.tar.gz
tar -xvzf apjs504015_data.tar.gz
rm -f apjs504015_data.tar.gz ReadMe Table_S1.txt Table_S2.txt \
      Table_S3.txt Table_S6.par

# Download TiO data:
#cd $topdir/inputs
#wget http://kurucz.harvard.edu/molecules/tio/tioschwenke.bin
#wget http://kurucz.harvard.edu/molecules/tio/tiopart.dat


# Generate partition-function files for H2O and NH3:
cd $topdir/run01
python $topdir/code/pf_tips_H2O-NH3.py

# Generate partition-function files for HCN, CH4, and TiO:
cd $topdir/run01
python $topdir/pyratbay/scripts/PFformat_Exomol.py  \
       $topdir/inputs/1H-12C-14N__Harris.pf \
       $topdir/inputs/1H-13C-14N__Larner.pf
python $topdir/pyratbay/scripts/PFformat_Exomol.py \
       $topdir/inputs/12C-1H4__YT10to10.pf
#python $topdir/pyratbay/scripts/PFformat_Schwenke_TiO.py \
#       $topdir/inputs/tiopart.dat

# Compress LBL databases:
cd $topdir/run01
python $topdir/repack/repack.py repack_H2O.cfg
python $topdir/repack/repack.py repack_HCN.cfg
python $topdir/repack/repack.py repack_NH3.cfg
python $topdir/repack/repack.py repack_CH4.cfg
#python $topdir/repack/repack.py repack_TiO.cfg

# Make TLI files:
cd $topdir/run01
python $topdir/pyratbay/pbay.py -c tli_hitemp_CO2.cfg
python $topdir/pyratbay/pbay.py -c tli_hitemp_H2O.cfg
python $topdir/pyratbay/pbay.py -c tli_Li_CO.cfg
python $topdir/pyratbay/pbay.py -c tli_exomol_HCN.cfg
python $topdir/pyratbay/pbay.py -c tli_exomol_NH3.cfg
python $topdir/pyratbay/pbay.py -c tli_exomol_CH4.cfg
#python $topdir/pyratbay/pbay.py -c tli_Schwenke_TiO.cfg

# Make opacity file
cd $topdir/run01
python $topdir/pyratbay/pbay.py -c opacity_H2O-CH4-CO-CO2-HCN-NH3_300-3000K_0.3-33um.cfg

# Make atmospheric files
#cd $topdir/run01
#python $topdir/pyratbay/pbay.py -c atm_wasp63b_1000K_0.03x.cfg

# Radiative-equilibrium atmospheric models:
cd $topdir/run02
python $topdir/pyratbay/pbay.py -c radeq_wasp43b.cfg

# Posteriors plot:
#cd $topdir/run02_BKM/
#python $topdir/code/fig_posteriors.py

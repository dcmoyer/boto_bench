
#
# Straight from the DiPy website
#

from dipy.data import read_stanford_labels
from dipy.reconst.csdeconv import ConstrainedSphericalDeconvModel
from dipy.tracking import utils
from dipy.tracking.local import (ThresholdTissueClassifier, LocalTracking)

hardi_img, gtab, labels_img = read_stanford_labels()
data = hardi_img.get_data()
labels = labels_img.get_data()
affine = hardi_img.affine

seed_mask = labels == 2
white_matter = (labels == 1) | (labels == 2)
seeds = utils.seeds_from_mask(seed_mask, density=1, affine=affine)

csd_model = ConstrainedSphericalDeconvModel(gtab, None, sh_order=6)
csd_fit = csd_model.fit(data, mask=white_matter)

print("fitting model")

from dipy.reconst.shm import CsaOdfModel

csa_model = CsaOdfModel(gtab, sh_order=6)
gfa = csa_model.fit(data, mask=white_matter).gfa

import sys
print(sys.getsizeof(gfa))

import cloudpickle as cp

f = open("gfa_example.cloudpickle","wb")
cp.dump((csd_fit.shm_coeff, gfa, seeds, affine),f)
f.close()


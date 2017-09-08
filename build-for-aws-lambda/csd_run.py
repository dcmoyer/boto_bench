
import cloudpickle as cp

f = open("gfa_example.cloudpickle","rb")
shm_coeff, gfa, seeds, affine = cp.load(f)
f.close()

seeds = [seeds[0]]

print("tracking model")

from dipy.direction import ProbabilisticDirectionGetter
#from dipy.io.trackvis import save_trk

from dipy.data import default_sphere
from dipy.tracking.local import (ThresholdTissueClassifier, LocalTracking)

classifier = ThresholdTissueClassifier(gfa, .25)

prob_dg = ProbabilisticDirectionGetter.from_shcoeff(shm_coeff,
                                                    max_angle=30.,sphere=default_sphere)
streamlines = LocalTracking(prob_dg, classifier, seeds, affine, step_size=.5)






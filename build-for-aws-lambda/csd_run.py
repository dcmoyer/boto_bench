
def install_and_import(package):
  import importlib
  try:
    importlib.import_module(package)
  except ImportError:
    import pip
    pip.main(['install', package])
  finally:
    globals()[package] = importlib.import_module(package)

install_and_import('dipy')

#import joblib
import boto3
from dipy.direction import ProbabilisticDirectionGetter
#from dipy.io.trackvis import save_trk

from dipy.data import default_sphere
from dipy.tracking.local import (ThresholdTissueClassifier, LocalTracking)

def lambda_handler(event, context):

  #file logics
  try:
    event["local_debug"]
  except KeyError:
    event["local_debug"] = False
    pass

  if(event["local_debug"]):
    import cloudpickle as cp
    s3 = boto3.resource('s3')

    f = open("/outputs/gfa_example.cloudpickle","rb")
    shm_coeff, gfa, affine = cp.load(f)
    #shm_coeff, gfa, affine = joblib.load(f)
    f.close()

    f = open("/outputs/seeds.cloudpickle","rb")
    seeds = cp.load(f)
    #seeds = joblib.load(f)
    f.close()

    seeds = [seeds[0]]
  else:
    import pickle
    s3 = boto3.resource('s3')
    #shm_coeff, gfa, affine = cp.loads(\
    #  s3.Object(event["bucket_name"], event["gfa_key"]).get()["Body"].read()\
    #)
    local_file = '/tmp/temp_s3_obj.pkl'
    s3.Object(event["bucket_name"],\
      event["gfa_key"]).get_contents_to_filename( local_file )
    shm_coeff, gfa, affine = pickle.loads(\
      local_file
    )
    seeds = event["seeds"]
  
  print("tracking model")

  classifier = ThresholdTissueClassifier(gfa, .25)

  prob_dg = ProbabilisticDirectionGetter.from_shcoeff(shm_coeff, \
    max_angle=30.,sphere=default_sphere)
  streamlines = LocalTracking(prob_dg, classifier, seeds, affine, step_size=.5)

  #write and push
  if not event["local_debug"]:
    s3 = boto3.resource('s3')

    f = open("tmp/streamlines.pkl","wb")
    joblib.dump(streamlines,f,compress=True)
    f.close()
    f = open("tmp/streamlines.pkl","rb")
    s3.Object(event["output_bucket"], event["output_key"]).put(Body=f)
    f.close()
    pass


#
#
#
if __name__ == "__main__":
  lambda_handler(event = {"local_debug" : True}, context = None)





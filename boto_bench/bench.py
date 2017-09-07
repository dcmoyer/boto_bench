
import pickle
import cloudpickle
import boto3

from botocore.exceptions import ClientError

class Bench():

  def __init__(self, profile=None, verbose=False):
    import os

    # AWS Config Logic
    try:
      fname = os.environ["AWS_CONFIG_FILE"]
      if verbose:
        print("[Boto Bench]: Using override for AWS_CONFIG_FILE=%s" % fname)
    except KeyError:
      fname = os.path.expanduser('~') + "/.aws/credentials"

    if not os.path.isfile(fname):
      print("[Boto Bench]: AWS config key file not found. Aborting")
      exit(1)

    if profile:
      if verbose:
        print("[Boto Bench]: Using profile %s" % profile)

      #will error out if profile doesn't exist
      self.session = boto3.Session(profile_name=profile)
    else:
      self.session = boto3.Session()

    print(self.session.region_name)

    #there should be a cleaner way
    #credentials = None
    #with open(fname, "r") as config_file_reader:
    #  for line in config_file_reader:
    #    if line[0] == "[" and line[1:-2] == profile:
    #      aws_access_key = config_file_reader.readline().split(" = ")[1][:-1]
    #      aws_secret_key = config_file_reader.readline().split(" = ")[1][:-1]
    #      credentials = (aws_access_key, aws_secret_key)
    #    else:
    #      continue;

    #if not credentials:
    #  print("[Boto Bench]: Credentials not found")
    #  exit(1)

    #self.credentials = credentials

    #TODO: change this to a boto_bench config 
    self.bucket_name = "dcmoyer-boto-bench-workspace-1919"
    self.bb_config_dir = os.path.expanduser('~') + "/.boto_bench/"
    self.bucket_index_file = self.bb_config_dir + "bucket_index.p"

    if not os.path.isdir(self.bb_config_dir):
      if verbose:
        print("[Boto Bench]: Creating config dir at %s" % self.bb_config_dir)
      os.mkdir(self.bb_config_dir)

    self.s3 = self.session.resource('s3')

    if not os.path.isfile(self.bucket_index_file):
      self.bucket_index = {}
    else:
      self.bucket_index = pickle.load(open(self.bucket_index_file,"rb"))

    self._create_bucket()

  def _create_bucket(self):
    #TODO: switch to try except update
    #TODO: switch from lazy code always trying to create, to check then create 
    #if you're using this module and you don't want the same region as your default, you should just use boto
    try:
      self.s3.create_bucket(
        Bucket=self.bucket_name,
        CreateBucketConfiguration= {
          'LocationConstraint': self.session.region_name
        }
      )
    except ClientError as e:
      if e.response["Error"]["Code"] != "BucketAlreadyOwnedByYou":
        raise(e)
      print("[Boto Bench]: TODO: Collect Index from existing bucket.")
      #print("[Boto Bench]: BB bucket exists, updating index.")
      #self.Bucket = self.s3.Bucket(self.bucket_name)
      #self.index = self.Bucket.objects.all()
    return

  def __del__(self):
    #dump out index into pickle file
    pickle.dump(
      self.bucket_index,
      open(self.bucket_index_file,"wb")
    )

  def push(self,obj,name=""):
    pickled_obj = cloudpickle.dumps(object)
    pass

  def delete(self,key):
    pass

  def pull(self,key):
    pass






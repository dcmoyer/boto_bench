
import pickle

import cloudpickle
import boto3

from botocore.exceptions import ClientError

class Bench():

  def __init__(self, boto_bench_name=None, profile=None, verbose=False):

    import os

    if not boto_bench_name:
      print("You need a boto_bench_name. Aborting.")
      exit(1)

    self.boto_bench_name = boto_bench_name

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

    #self.credentials = credentials

    #TODO: change this to a boto_bench config 
    self.bucket_name = "%s-boto-bench-workspace-1919-nhw" % boto_bench_name
    #self.bb_config_dir = os.path.expanduser('~') + "/.boto_bench/"
    #self.bucket_index_file = self.bb_config_dir + "bucket_index.p"

    #init local directory
    #if not os.path.isdir(self.bb_config_dir):
    #  if verbose:
    #    print("[Boto Bench]: Creating config dir at %s" % self.bb_config_dir)
    #  os.mkdir(self.bb_config_dir)

    #init self resources
    self.s3 = self.session.resource('s3')
    print(self.session.get_available_services())
    self.lambda_service = self.session.client('lambda')

    #init in
    #if not os.path.isfile(self.bucket_index_file):
    #  self.bucket_index = {}
    #else:
    #  self.bucket_index = pickle.load(open(self.bucket_index_file,"rb"))

    self._create_bucket()
    self.Bucket = self.s3.Bucket(self.bucket_name)

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
      #
      #self.index = self.Bucket.objects.all()
    return

  #def __del__(self):
  #  #dump out index into pickle file
  #  pickle.dump( \
  #    self.bucket_index, \
  #    open(self.bucket_index_file,"wb") \
  #  )

  #
  # Pushes to AWS S3
  #   Pushing is FREE.99 (kinda)
  #
  def push(self,obj,name=None):
    pickled_obj = cloudpickle.dumps(obj)
    if not name:
      #TODO: default names?!??!
      #TODO: exceptions? sorry, c++ programmer
      print("every object needs a name silly, aborting")
      exit(1)
    self.s3.Object(self.bucket_name, name).put(Body=pickled_obj)
    pass

  #
  # Deletes from AWS S3
  #   Deleting is also FREE.99
  #
  def delete(self,target_key):
    #TODO:Direct??
    for key in self.Bucket.objects.all():
      if key.key == target_key:
        key.delete()
        return
    print("deleting key not found, aborting")
    exit(1)

  #
  # Pulling is not free. Sad.
  #
  #
  def pull(self,target_key):
    #TODO:Direct?
    for key in self.Bucket.objects.all():
      if key.key == target_key:
        return pickle.loads( key.get()["Body"].read() )

  def ls(self):
    print("[Boto Bench] ls")
    print("Bucket name: %s" % self.bucket_name)
    for key in self.Bucket.objects.all():
      print("\t%s" % key.key)
    pass

  def list(self):
    self.ls()

  #TODO: spin this out into not-just-the-bench
  def L_push_lambda(self):
    
    pass

  #TODO: spin this out into not-just-the-bench
  def L_list_lambdas(self):
    self.L_ls()
    pass

  def L_ls(self):
    print("[Boto Bench] (Lambda) ls")
    for func in self.lambda_service.list_functions()["Functions"]:
      print(func["FunctionName"])
    pass









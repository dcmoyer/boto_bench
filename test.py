from boto_bench import bench as bb

bench = bb.Bench(\
  boto_bench_name="dcmoyer",\
  profile="nhw", \
  verbose = True \
)

bench.ls()

test_list = [1,2,3]

bench.push(test_list, "test_list")

test_lambda = lambda x : 10 + 10
bench.push(test_lambda, "test_lambda_function")

bench.ls()

test_list_pulled = bench.pull("test_list")

bench.delete("test_list")

bench.delete("test_lambda_function")

bench.ls()

if test_list == test_list_pulled:
  print("yay!")  
else:
  print(list(test_list_pulled))

bench.L_ls()

import joblib

f = open("seeds.cloudpickle","rb")
seeds = joblib.load(f)
f.close()

bench.push_file("test.zip","test_function.zip")

def L_push_lambda(self):

bench.L_push_function( \
  "test_function.zip", \
  "csd_run.lambda_handler", \
  "csd_test_run",\
  function_is_bucket_key=True 
)


for x in range(len(seeds) // 1000):
  continue
  bench.L_invoke(
    "csd_test_run", \
    {\
      "seeds" : seeds[x*1000:(x+1)*1000], \
      "output_bucket" : "dcmoyer-boto-bench-workspace-1919-nhw", \
      "output_key" : "to%i" % x \
    }, \
    async=True,\
    dry_run = False\
  )







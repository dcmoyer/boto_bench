from boto_bench import bench as bb

bench = bb.Bench(verbose = True)

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



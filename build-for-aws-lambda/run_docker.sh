
echo ${1} > target.txt
chmod 744 target.txt
docker run --security-opt=seccomp:unconfined -v $(pwd):/outputs -it amazonlinux:2016.09 /bin/bash /outputs/build.sh
rm target.txt

docker run --security-opt=seccomp:unconfined -v $(pwd):/outputs -it amazonlinux:2016.09 /bin/bash /outputs/build.sh

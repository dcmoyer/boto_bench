#!/bin/bash
set -ex

yum update -y
yum install -y \
    atlas-devel \
    atlas-sse3-devel \
    blas-devel \
    bzip2-devel \
    gcc \
    gcc-c++ \
    lapack-devel \
    openssl \
    openssl-devel \
    python36-devel \
    python36-virtualenv \
    sqlite-devel \
    findutils \
    wget \
    xz \
    zlib-devel\
    zip

get_python(){
    wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
    tar -xf Python-3.6.2.tar.xz
    cd Python-3.6.2
    ./configure
    make
    make install
    cd /
}

do_pip () {
    pip3 install --upgrade pip wheel
    pip3 install --use-wheel --no-binary numpy==1.8.2
    pip3 install --use-wheel --no-binary scipy==0.19.0
    #pip install --use-wheel sklearn
    pip3 install --use-wheel  dipy
    #pip3 install --use-wheel  boto3
    #pip3 install --use-wheel  joblib 
    pip3 install --use-wheel  cloudpickle
    pip3 install --use-wheel  reprozip
    pip3 install --use-wheel  reprounzip
}

strip_virtualenv () {
    echo "venv original size $(du -sh $VIRTUAL_ENV | cut -f1)"
    find $VIRTUAL_ENV/lib/python3.6/site-packages/ -name "*.so" | xargs strip
    echo "venv stripped size $(du -sh $VIRTUAL_ENV | cut -f1)"

    pushd $VIRTUAL_ENV/lib/python3.6/site-packages/ && zip -r -9 -q /outputs/venv.zip * ; popd
    echo "site-packages compressed size $(du -sh /outputs/venv.zip | cut -f1)"

    pushd $VIRTUAL_ENV && zip -r -q /outputs/full-venv.zip * ; popd
    echo "venv compressed size $(du -sh /outputs/full-venv.zip | cut -f1)"
}

shared_libs () {
    libdir="$VIRTUAL_ENV/lib/python3.6/site-packages/lib/"
    mkdir -p $VIRTUAL_ENV/lib/python3.6/site-packages/lib || true
    cp /usr/lib64/atlas/* $libdir
    cp /usr/lib64/libquadmath.so.0 $libdir
    cp /usr/lib64/libgfortran.so.3 $libdir
}

main () {
    #/usr/bin/virtualenv \
    #    --python /usr/bin/python /sklearn_build \
    #    --always-copy \
    #    --no-site-packages
    #source /sklearn_build/bin/activate

    get_python

    #pip3 install virtualenv

    #/usr/local/bin/virtualenv \
    #    --python /usr/local/bin/python3 /build \
    #    --always-copy \
    #    --no-site-packages
    #source /build/bin/activate

    target=$(cat /outputs/target.txt)

    echo target=${target}
    if ! [ -a /outputs/${target} ];
    then
      echo "This function does not exist, and thus cannot be lambda prepped."
      exit 1
    fi

    do_pip

    #shared_libs

    #strip_virtualenv
    #
    #pushd /outputs/ && zip -r -q /outputs/venv.zip ${target} ; popd

    #do_pip

    #shared_libs

    #strip_virtualenv

    chmod 770 /outputs/${target}

    cd /outputs/

    reprozip trace --overwrite python3 /outputs/${target}

    rm -f ${target}.rpz
    reprozip pack ${target}.rpz

    cd ..
    rm -f /outputs/venv.zip
    pushd /outputs/ && zip -r -9 -q /outputs/venv.zip ${target}.rpz ; popd
    pushd /outputs/ && zip -r -q /outputs/venv.zip ${target} ; popd

   # zip -r -q /outputs/full-venv.zip /outputs/${target}.rpz /outputs/${target}
   # echo "venv compressed size $(du -sh /outputs/full-venv.zip | cut -f1)"

   # mv /outputs/full-venv.zip /outputs/${target}.zip
}
main

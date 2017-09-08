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
    pip3 install --use-wheel --no-binary numpy numpy
    pip3 install --use-wheel --no-binary scipy scipy
    #pip install --use-wheel sklearn
    pip3 install --use-wheel  dipy
    pip3 install --use-wheel  cloudpickle
    pip3 install --use-wheel  reprozip
    pip3 install --use-wheel  reprounzip
}

strip_virtualenv () {
    #echo "venv original size $(du -sh $VIRTUAL_ENV | cut -f1)"
    #find $VIRTUAL_ENV/lib64/python3.6/site-packages/ -name "*.so" | xargs strip
    #echo "venv stripped size $(du -sh $VIRTUAL_ENV | cut -f1)"

    #pushd $VIRTUAL_ENV/lib64/python3.6/site-packages/ && zip -r -9 -q /outputs/venv.zip * ; popd
    #echo "site-packages compressed size $(du -sh /outputs/venv.zip | cut -f1)"

    #pushd $VIRTUAL_ENV && zip -r -q /outputs/full-venv.zip * ; popd
    echo "venv compressed size $(du -sh /outputs/full-venv.zip | cut -f1)"
}

shared_libs () {
    libdir="$VIRTUAL_ENV/lib64/python3.6/site-packages/lib/"
    mkdir -p $VIRTUAL_ENV/lib64/python3.6/site-packages/lib || true
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

    do_pip

    #shared_libs

    #strip_virtualenv

    chmod 770 /outputs/csd_run.py

    cd /outputs/

    reprozip trace python3 /outputs/csd_run.py

    reprozip pack csd_tracking.rpz

    cd ..

    zip -r -q /outputs/full-venv.zip /outputs/csd_tracking.rpz
    echo "venv compressed size $(du -sh /outputs/full-venv.zip | cut -f1)"

    mv /outputs/full-venv.zip /outputs/csd_tracking.zip
}
main

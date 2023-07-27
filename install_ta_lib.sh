#!/bin/bash

# Download TA-Lib source tarball
curl -L -O http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

# Extract the tarball
tar -xvzf ta-lib-0.4.0-src.tar.gz

# Navigate to the ta-lib directory
cd ta-lib/

# Configure, make, and install TA-Lib
./configure --prefix=/usr
make
make install

# Export necessary environment variables
export TA_INCLUDE_PATH="/usr/include"
export TA_LIBRARY_PATH="/usr/lib"

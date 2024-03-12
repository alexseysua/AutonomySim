#!/bin/bash
#----------------------------------------------------------------------------------------
# Filename
#   setup.sh
# Description
#   BASH script to install and configure AutonomySim dependencies.
# Authors
#   Microsoft (original)
#   Adam Erickson (Nervosys)
# Date
#   2024-02-20
# Usage
#   `bash setup.sh --high-polycount-suv`
# Notes
# - Required: cmake, rpclib, eigen
# - Optional: high-poly count SUV asset for Unreal Engine
# - This script is a cleaned up version of the original AirSim script.
# TODO
# - Update: ensure script runs on recent Linux distributions, MacOS, Windows.
#----------------------------------------------------------------------------------------

set -x  # print shell commands before executing (for debugging)
set -e  # exit on error return code

###
### Functions
###

# Silence brew error if package is already installed.
function brew_install {
    brew list "$1" &>/dev/null || brew install "$1"
}

# Numeric comparator. A robust version checker.
# USAGE: if ( numeric_comparison '3.3' '<=' '3.4' ); then ...; else ...; fi
# WARNING: cannot handle version numbers.
# function numeric_comparison {
#     test "$(echo $1 $2 $3 | bc --mathlib)" = '1'
# }

# Check version compatability.
function version_less_than_equal_to {
    test "$(printf '%s\n' "$@" | sort -V | head -n 1)" = "$1"
}

# Get the absolute path on Linux and macOS.
# NOTE: We emulate `realpath`, as we cannot use it or GNU `coreutils:readlink` because macOS.
function abspath {
    if [ "$1" = '.' ]; then
        echo "$(cd $(dirname $1); pwd -P)"
    else
        echo "$(cd $(dirname $1); pwd -P)/$(basename $1)"
    fi
}

###
### Variables
###

# Directory paths. 
PROJECT_DIR="$(abspath $PWD)"
SCRIPT_DIR="$(dirname $(abspath ${BASH_SOURCE[0]}))"

CMAKE_VERSION='3.10.2'
CLANG_VERSION='12'  # requires ubuntu >= 20
EIGEN_VERSION='3.4.0'
RPCLIB_VERSION='2.3.0'
UNREAL_ASSET_VERSION='1.2.0'

# Ensure CMake supports CMAKE_APPLE_SILICON_PROCESSOR for MacOS.
if [ "$(uname)" = 'Darwin' ]; then
    CMAKE_VERSION_MIN='3.19.2'
else
    CMAKE_VERSION_MIN='3.10.0'
fi
CMAKE_VERSION_MIN_MAJ_MIN='3.10'

# download high-polycount SUV model.
HIGH_POLYCOUNT_SUV='false'
HIGH_POLYCOUNT_SUV_URL='https://github.com/microsoft/AirSim/releases/download/v1.2.0/car_assets.zip'

DEBUG="${DEBUG:-false}"

###
### Main
###

# Parse command-line interface (CLI) arguments.
while [ $# -gt 0 ]; do
    case "$1" in
    '--debug')
        DEBUG='true'
        ;;
    '--high-polycount-suv')
        HIGH_POLYCOUNT_SUV='true'
        shift
        ;;
    esac
done

# Ensure LLVM and Vulkan are installed.
if [ "$(uname)" = 'Darwin' ]; then
    echo 'Installing dependencies...'
    # Reinstall Homebrew
    # sudo rm -rf \
    #     /Users/runner/Library/Caches/Homebrew/ \
    #     /Users/runner/Library/Logs/Homebrew/ \
    #     /usr/local/Caskroom/ \
    #     /usr/local/Cellar/ \
    #     /usr/local/bin
    # NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    # (echo; echo 'eval "$(/usr/local/bin/brew shellenv)"') >> "${HOME}/.bash_profile"
    # eval "$(/usr/local/bin/brew shellenv)"
    brew update
    brew upgrade
    brew install curl
    export HOMEBREW_CURL_PATH='/usr/local/opt/curl/bin/curl'
    HOMEBREW_FORCE_BREWED_CURL=1 brew config
    export PATH="/usr/local/opt/curl/bin:${PATH}"
    echo 'Installing latest cURL version and configuring Homebrew to use it...'
    brew install python@3.11
    brew install coreutils
    brew install "llvm@${CLANG_VERSION}"
    # brew install azure-cli
else
    echo 'Installing dependencies...'
    sudo add-apt-repository -y ppa:graphics-drivers/ppa
    sudo apt-get update -y
    sudo apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        gnupg \
        software-properties-common \
        build-essential \
        unzip \
        coreutils \
        lsb-release \
        rsync \
        wget \
        libunwind-dev \
        zlib1g-dev \
        vulkan-tools \
        libvulkan1 \
        # vulkan vulkan-utils
    wget -qO- 'https://apt.llvm.org/llvm-snapshot.gpg.key' | sudo tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc
    sudo apt-get install -y \
        "clang-${CLANG_VERSION}" \
        "clang++-${CLANG_VERSION}" \
        "libc++-${CLANG_VERSION}-dev" \
        "libc++abi-${CLANG_VERSION}-dev" 
fi

# Get/set CMake version.
if [ ! "$(which cmake)" ]; then
    cmake_ver='0'
else
    cmake_ver="$(cmake --version 2>&1 | head -n1 | cut -d ' ' -f3 | awk '{print $NF}')"
fi

# Give user permissions to access USB port, not needed if not using PX4 HIL.
# TODO: figure out how to do below in travis. Install additional tools, CMake if required.
if [ "$(uname)" = 'Darwin' ]; then
    if [ -n "${whoami}" ]; then # travis
        sudo dseditgroup -o edit -a "$(whoami)" -t user dialout
    fi
    brew update
    # Conditionally install lower CMake version.
    if ( version_less_than_equal_to "$cmake_ver" "$CMAKE_VERSION_MIN" ); then
        brew install cmake
    else
        echo "Compatible version of CMake already installed: $cmake_ver"
    fi
else
    if [ -n "${whoami}" ]; then # travis
        sudo /usr/sbin/useradd -G dialout "$USER"
        sudo usermod -a -G dialout "$USER"
    fi
    if ( version_less_than_equal_to "$cmake_ver" "$CMAKE_VERSION_MIN" ); then
        sudo apt-get -y install --no-install-recommends make cmake
    else
        echo "Compatible version of CMake already installed: $cmake_ver"
    fi
fi

# Download and unpack RPCLib.
if [ ! -d "./external/rpclib/rpclib-${RPCLIB_VERSION}" ]; then
    # remove previous versions and create empty directory
    rm -rf "./external/rpclib"
    mkdir -p "./external/rpclib"
    echo '-----------------------------------------------------------------------------------------'
    echo ' Downloading RPCLib...'
    echo '-----------------------------------------------------------------------------------------'
    wget "https://github.com/rpclib/rpclib/archive/v${RPCLIB_VERSION}.zip"
    unzip -q "v${RPCLIB_VERSION}.zip" -d ./external/rpclib
    rm "v${RPCLIB_VERSION}.zip"
fi

# Download and unpack high-polycount SUV asset for Unreal Engine.
if [ "${HIGH_POLYCOUNT_SUV}" = 'true' ]; then
    if [ ! -d ./UnrealPlugin/Unreal/Plugins/AutonomySim/Content/VehicleAdv ]; then
        mkdir -p ./UnrealPlugin/Unreal/Plugins/AutonomySim/Content/VehicleAdv
    fi
    if [ ! -d "./UnrealPlugin/Unreal/Plugins/AutonomySim/Content/VehicleAdv/SUV/v${UNREAL_ASSET_VERSION}" ]; then
        echo '-----------------------------------------------------------------------------------------'
        echo ' Downloading Unreal high-polycount SUV asset...'
        echo '-----------------------------------------------------------------------------------------'
        if [ -d ./temp/suv ]; then
            rm -rf ./temp/suv
        fi
        mkdir -p ./temp/suv
        wget "$HIGH_POLYCOUNT_SUV_URL" -P ./temp/suv
        if [ -d ./UnrealPlugin/Unreal/Plugins/AutonomySim/Content/VehicleAdv/SUV ]; then
            rm -rf ./UnrealPlugin/Unreal/Plugins/AutonomySim/Content/VehicleAdv/SUV
        fi
        unzip -q ./temp/suv/car_assets.zip -d ./UnrealPlugin/Unreal/Plugins/AutonomySim/Content/VehicleAdv
        rm -rf ./temp/suv
    fi
else
    echo "Skipped: Download of Unreal high-polycount SUV asset. The default Unreal Engine vehicle will be used."
fi

# Download and unpack Eigen3 C++ library.
if [ ! -d './AutonomyLib/deps/eigen3' ]; then
    echo 'Installing Eigen C++ library...'
    mkdir -p ./temp/eigen
    wget "https://gitlab.com/libeigen/eigen/-/archive/${EIGEN_VERSION}/eigen-${EIGEN_VERSION}.zip" -P ./temp/eigen
    unzip -q "./temp/eigen/eigen-${EIGEN_VERSION}.zip" -d ./temp/eigen
    mkdir -p ./AutonomyLib/deps/eigen3
    mv "./temp/eigen/eigen-${EIGEN_VERSION}/Eigen" ./AutonomyLib/deps/eigen3
    rm -rf ./temp/eigen
else
    echo "Skipped: Eigen is already installed."
fi

# popd >/dev/null # pop script directory off of the stack

set +x  # disable printing shell commands before executing

echo '-----------------------------------------------------------------------------------------'
echo ' Success: AutonomySim setup complete.'
echo '-----------------------------------------------------------------------------------------'

exit 0

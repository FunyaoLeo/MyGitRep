#!/usr/bin/env bash

TMP_NAME=project4
TMP_DIR=/tmp/${TMP_NAME}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function error_exit()
{
   echo -e "ERROR: $1" 1>&2
   rm -rf ${TMP_DIR}
   exit 1
}

# make sure running in container
if [ `whoami` != "cs144" ]; then
    error_exit "You need to run this script within the container"
fi

# clean any existing files
rm -rf ${TMP_DIR}
mkdir ${TMP_DIR}

# change to dir contains this script
cd $DIR

# check file existence
if [ -f "project4.zip" ]; then
    error_exit "$DIR/project4.zip already exists, remove it before running the script"
fi

if [ ! -f "TEAM.txt" ]; then
    error_exit "Lack $DIR/TEAM.txt"
fi

# check the format of TEAM.txt
VALID_UID=$(grep -E "^[0-9]{9}\s*$" TEAM.txt)
if [ -z "${VALID_UID}" ]; then
    error_exit "No valid UID was found in TEAM.txt.\nInclude one 9-digit UID per line. No spaces or dashes, please."
fi
NON_UID=$(grep -v -E "^[0-9]{9}\s*$" TEAM.txt)
if [ -n "${NON_UID}" ]; then
    error_exit "Following lines are invalid in TEAM.txt\n${NON_UID}\nInclude one 9-digit UID per line. No spaces or dashes, please."
fi


# main

# check if there is 192.168.X.X string in the source code
grep '192.168.' src/app/*.ts > /dev/null
if [ $? -eq 0 ]; then
    echo '[WARNING] The script detected that your code has string 192.168.X.X'
    echo '[WARNING] Please ensure that your submitted Angular code uses localhost as'
    echo '[WARNING] the hostname of the server API, not 192.168.X.X'
fi 

echo "Building your project ..."
ng build
if [ $? -ne 0 ]; then
    error_exit "Run ng build failed."
else
    echo "Run ng build succeeds."
fi

echo "Creating project4.zip file ..."
zip -rq ${TMP_DIR}/project4.zip . -x 'node_modules/*' package.sh
if [ $? -ne 0 ]; then
    error_exit "Create project4.zip failed, check for error messages in console."
fi
mv ${TMP_DIR}/project4.zip .
if [ $? -ne 0 ]; then
    error_exit "Create project4.zip failed, check for error messages in console."
else
    echo "[SUCCESS] Created '$DIR/project4.zip', please submit it to CCLE."
fi

exit 0

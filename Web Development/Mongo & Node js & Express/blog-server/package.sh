#!/usr/bin/env bash

TESTURL="http://localhost:3000/blog/cs144/1"
TMP_NAME=project3
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
if [ -f "project3.zip" ]; then
    rm -f project3.zip
fi

if [ ! -f "TEAM.txt" ]; then
    error_exit "Missing $DIR/TEAM.txt"
fi

if [ ! -f "db.sh" ]; then
    error_exit "Missing $DIR/db.sh"
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

zip -r project3.zip . -x 'node_modules/*' package.sh
if [ $? -ne 0 ]; then
    error_exit "Create project3.zip failed, check for error messages in console."
fi

# unzip the packaged file
"Testing your project3.zip for basic sanity check..."
cd $TMP_DIR
unzip $DIR/project3.zip

# run npm install
"Installing dependent node modules..."
npm install

# check if mongodb server is running
pgrep mongo > /dev/null
if [ $? -ne 0 ]; then
   echo "MongoDB server is not running. Starting the server..."
   echo "password" | sudo -S mongod --fork --logpath /var/log/mongodb/mongodb.log
fi

# drop all collections in BlogServer database
echo "Deleting all documents in BlogServer database..."
cat << EOF | mongo
    use BlogServer;
    db.dropDatabase();
EOF

# load initial documents to mongodb
echo "Loading initial documents to MongoDB using your db.sh..."
mongo < ./db.sh

# run the server
echo "Running your blog server..."
npm start &
if [ $? -ne 0 ]; then
    error_exit "Failed to run your blog server. Is your code in a runable state? Are you running another server at port 3000?"
fi
PID=$!
sleep 5

# send a request to the blog server
echo "Retrieving $TESTURL from your server..."
curl -s $TESTURL &> /dev/null
if [ $? -ne 0 ]; then
    error_exit "Failed to retrieve $TESTURL from your server"
fi

# kill npm process and the node server
echo "Stopping the node server..."
kill $PID
kill `pgrep node`

# remove temp files
cd $DIR
rm -rf $TMP_DIR

echo "[SUCCESS] Created '$DIR/project3.zip', please submit it to CCLE."

exit 0

#!/bin/bash

. _pick_pythons.sh

XMLLINT=`which xmllint`

#Halt on error
set -e
#Display all executed commands
set -x

#NOTE: Python2's ETree does not understnad the "unicode" output encoding.
#"$PYTHON2" cat_fileobjects.py ../samples/simple.xml
"$PYTHON3" cat_fileobjects.py ../samples/simple.xml

if [ -x "$XMLLINT" ]; then
  "$PYTHON3" cat_fileobjects.py ../samples/simple.xml | "$XMLLINT" -
else
  echo "Warning: xmllint not found.  Skipped check for if generated DFXML is valid XML." >&2
fi

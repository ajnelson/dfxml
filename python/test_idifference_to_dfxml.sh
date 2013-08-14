#!/bin/bash

. _pick_pythons.sh

#Halt on error
set -e
#Display all executed commands
set -x

"$PYTHON3" idifference.py --xml idifference_test.dfxml ../samples/difference_test_[01].xml
xmllint --format idifference_test.dfxml >idifference_test_formatted.dfxml

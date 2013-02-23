#!/bin/bash

#This script tests idifference.py on a hand-written pair of DFXML files, measuring the expected output.

if [ $# -ne 0 ]; then
  echo Usage: $0 >&2
  exit 1
fi

trap "set +x; echo Test failed. >&2" EXIT

set -e

TESTSCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IDIFFERENCE_SCRIPT=${TESTSCRIPTDIR}/../python/idifference.py
IDIFFERENCE_OUTPUT=${TESTSCRIPTDIR}/tmp.txt
SAMPLE_DIR=${TESTSCRIPTDIR}/../samples

python3 ${IDIFFERENCE_SCRIPT} --annotate-with-char ${SAMPLE_DIR}/diffee_time0.xml ${SAMPLE_DIR}/diffee_time1.xml >${IDIFFERENCE_OUTPUT}

#Test that a regular expression ($1) occurs exactly n ($2) times
assert_equal() {
  test `grep "$1" ${IDIFFERENCE_OUTPUT} | wc -l` -eq $2
}

set -x

#idifference is known to pass these tests.
assert_equal '\bNO_CHANGE\b' 0
assert_equal '^-.*\bCHANGE___erased\b' 1
assert_equal '^r.*\bCHANGE___renamed\b.*\b_CHANGE___renamed\b' 1
assert_equal '^~.*\bCHANGE___content_and_mtime\b.*SHA1 changed' 1
assert_equal '^~.*\bCHANGE___content_and_mtime\b.*mtime changed' 1
assert_equal '^+.*\bCHANGE___new_file\b' 1
#TODO Decide if it's "Correct" for an explicit time zone change to be registered as a difference.  Or, it might be worth just adding another flag to idifference.py to account for the user's decision.
assert_equal '^~.*\bCHANGE___timestamp_changes_format_only\b.*mtime changed' 1
assert_equal '^-.*\bCHANGE___unallocated\b' 1

#(Test code templates)
#assert_equal '^+.*\b\b' 1
#assert_equal '^-.*\b\b' 1
#assert_equal '^r.*\b\b.*\b\b' 1
#assert_equal '^~.*\b\b.*' 1

#TODO Write sufficient tests for these files
#      <filename>CHANGE___erased___replaced_by_other_partition_file</filename>
#      <filename>CHANGE___erased___replaced_by_sibling</filename><!--CHANGE: Inode remains the same, checksum does not.-->
#      <filename>CHANGE___moved_to_erased_P1G_file</filename>
#      <filename>CHANGE___move_from_P1G_to_P2G</filename>
#      <filename>_CHANGE___move_from_P1M_to_P3G___change_name</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_content___change_mtime</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_name</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G</filename>
#      <filename>CHANGE___renamed_to_erased_sibling___change_checksum_and_mtime</filename>

set +x

trap - EXIT

echo "Tests successful."

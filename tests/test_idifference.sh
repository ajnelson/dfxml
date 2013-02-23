#!/bin/bash

#This script tests idifference.py on a hand-written pair of DFXML files, measuring the expected output.

if [ $# -ne 0 ]; then
  echo Usage: $0 >&2
  exit 1
fi

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

assert_equal '\bNO_CHANGE\b' 0

#      <filename>CHANGE___content_and_mtime</filename>
#      <filename>CHANGE___erased</filename>
#      <filename>CHANGE___erased___replaced_by_other_partition_file</filename>
#      <filename>CHANGE___erased___replaced_by_sibling</filename><!--CHANGE: Inode remains the same, checksum does not.-->
#      <filename>CHANGE___moved_to_erased_P1G_file</filename>
#      <filename>CHANGE___move_from_P1G_to_P2G</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_content___change_mtime</filename>
#      <filename>_CHANGE___move_from_P1M_to_P3G___change_name</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_name</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G</filename>
#      <filename>CHANGE___new_file</filename>
#      <filename>_CHANGE___renamed</filename>
#      <filename>CHANGE___renamed</filename>
#      <filename>CHANGE___renamed_to_erased_sibling___change_checksum_and_mtime</filename>
#      <filename>CHANGE___timestamp_changes_format_only</filename>
#      <filename>CHANGE___unallocated</filename>

echo "Tests successful."

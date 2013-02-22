#!/bin/bash

if [ $# -lt 1 ]; then
  echo Usage: $0 idifference_output_txt >&2
  exit 1
fi

set -e

IDIFFERENCE_OUTPUT=$1

#Test that a regular expression ($1) occurs exactly n ($2) times
assert_equal() {
  test `grep "$1" ${IDIFFERENCE_OUTPUT} | wc -l` -eq $2
}

assert_equal NO_CHANGE 0

#      <filename>CHANGE___content_and_mtime</filename>
#      <filename>CHANGE___content_and_mtime</filename>
#      <filename>CHANGE___erased</filename>
#      <filename>CHANGE___erased___replaced_by_other_partition_file</filename>
#      <filename>CHANGE___erased___replaced_by_other_partition_file</filename>
#      <filename>CHANGE___erased___replaced_by_sibling</filename>
#      <filename>CHANGE___erased___replaced_by_sibling</filename><!--CHANGE: Inode remains the same, checksum does not.-->
#      <filename>CHANGE___moved_to_erased_P1G_file</filename>
#      <filename>CHANGE___move_from_P1G_to_P2G</filename>
#      <filename>CHANGE___move_from_P1G_to_P2G</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_content___change_mtime</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_content___change_mtime</filename>
#      <filename>_CHANGE___move_from_P1M_to_P3G___change_name</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G___change_name</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G</filename>
#      <filename>CHANGE___move_from_P1M_to_P3G</filename>
#      <filename>CHANGE___new_file</filename>
#      <filename>_CHANGE___renamed</filename>
#      <filename>CHANGE___renamed</filename>
#      <filename>CHANGE___renamed_to_erased_sibling___change_checksum_and_mtime</filename>
#      <filename>CHANGE___timestamp_changes_format_only</filename>
#      <filename>CHANGE___timestamp_changes_format_only</filename>
#      <filename>CHANGE___unallocated</filename>
#      <filename>CHANGE___unallocated</filename>

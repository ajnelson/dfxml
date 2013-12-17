#!/usr/bin/env python3

__version__ = "0.1.3"

import os
import logging
import Objects
import idifference
import copy
import make_differential_dfxml

_logger = logging.getLogger(os.path.basename(__file__))

def enumerated_changes(filelist):
    res = set()
    for fi in filelist:
        diffs_remaining = copy.copy(fi.diffs)
        if "filename" in diffs_remaining:
            diffs_remaining.pop("filename")
        res.add((fi.filename, "renamed to", fi.original_fileobject.filename))
    return sorted(res)

class FOCounter(object):
    "Counter for FileObjects.  Does not count differences (differential annotations)."

    def __init__(self):
        self._inodes = set()
        self._fo_tally = 0
        self._fo_allocation_tallies_inode = {True:0, False:0, None:0}
        self._fo_allocation_tallies_name = {True:0, False:0, None:0}

    def add(self, obj):
        assert isinstance(obj, Objects.FileObject)
        self._inodes.add((obj.partition, obj.inode))
        self._fo_tally += 1

        self._fo_allocation_tallies_inode[obj.alloc_inode] += 1
        self._fo_allocation_tallies_name[obj.alloc_name] += 1

    @property
    def inode_tally(self):
        return len(self._inodes)

    @property
    def fo_tally(self):
        return self._fo_tally

    @property
    def fo_tally_alloc_inode(self):
        return self._fo_allocation_tallies_inode[True]

    @property
    def fo_tally_alloc_name(self):
        return self._fo_allocation_tallies_name[True]

    @property
    def fo_tally_nullalloc_inode(self):
        return self._fo_allocation_tallies_inode[None]

    @property
    def fo_tally_nullalloc_name(self):
        return self._fo_allocation_tallies_name[None]

    @property
    def fo_tally_unalloc_inode(self):
        return self._fo_allocation_tallies_inode[False]

    @property
    def fo_tally_unalloc_name(self):
        return self._fo_allocation_tallies_name[False]

def main():
    global args
    new_files = []
    deleted_files = []
    renamed_files = []
    modified_files = []
    changed_files = []
    unchanged_files = []

    original_dfxml_files = []

    obj_alloc_counters = [FOCounter(), FOCounter()]

    for (event, obj) in Objects.iterparse(args.infile):
        if isinstance(obj, Objects.FileObject):
            #_logger.debug("Inspecting %s for changes" % obj)
            if "_new" in obj.diffs:
                new_files.append(obj)
            elif "_deleted" in obj.diffs:
                deleted_files.append(obj)
            elif "_renamed" in obj.diffs:
                renamed_files.append(obj)
            elif "_modified" in obj.diffs:
                modified_files.append(obj)
            elif "_changed" in obj.diffs:
                changed_files.append(obj)
            else:
                unchanged_files.append(obj)

            obj_alloc_counters[1].add(obj)
            if obj.original_fileobject:
                obj_alloc_counters[0].add(obj.original_fileobject)
        elif isinstance(obj, Objects.VolumeObject):
            #TODO
            pass
        elif isinstance(obj, Objects.DFXMLObject):
            #Nothing happens with this DFXMLObject after the start.
            if event != "start":
                continue
            for source in obj.sources:
                _logger.debug("Adding to inspection queue: Source file %r." % source)
                original_dfxml_files.append(source)

    #Count basic allocation statistics from source files
    file_alloc_counters = []
    for (num, path) in enumerate(original_dfxml_files):
        file_alloc_counters.append(FOCounter())
        for (event, obj) in Objects.iterparse(path):
            if not isinstance(obj, Objects.FileObject):
                continue
            if event != "end":
                continue
            if make_differential_dfxml.ignorable_name(obj.filename):
                continue
            file_alloc_counters[num].add(obj)


    idifference.h2("New files:")
    res = [(obj.mtime, obj.filename or "", obj.filesize) for obj in new_files]
    idifference.table(sorted(res))

    idifference.h2("Deleted files:")
    res = [(obj.mtime, obj.filename or "", obj.filesize) for obj in deleted_files]
    idifference.table(sorted(res))

    idifference.h2("Renamed files:")
    res = enumerated_changes(renamed_files)
    idifference.table(res, break_on_change=True)

    idifference.h2("Summary:")
    summ_recs = None
    if len(file_alloc_counters) != 2:
       summ_recs = [
         ("Prior image's file (file object) tally", "(Unavailable)"),
         ("Prior image's file (inode) tally", "(Unavailable)"),
         ("Current image's file (file object) tally", "(Unavailable)"),
         ("Current image's file (inode) tally", "(Unavailable)"),
       ]
    else:
        summ_recs = [
          ("From reading the original files", ""),
          ("Prior image's file (file object) tally", str(file_alloc_counters[0].fo_tally)),
          ("  Inode allocation", ""),
          ("    Allocated", str(file_alloc_counters[0].fo_tally_alloc_inode)),
          ("    Unallocated", str(file_alloc_counters[0].fo_tally_unalloc_inode)),
          ("    Unknown", str(file_alloc_counters[0].fo_tally_nullalloc_inode)),
          ("  Name allocation", ""),
          ("    Allocated", str(file_alloc_counters[0].fo_tally_alloc_name)),
          ("    Unallocated", str(file_alloc_counters[0].fo_tally_unalloc_name)),
          ("    Unknown", str(file_alloc_counters[0].fo_tally_nullalloc_name)),
          ("  Unallocated, unmatched", "TODO"),
          ("Prior image's file (inode) tally", str(file_alloc_counters[0].inode_tally)),
          ("Current image's file (file object) tally", str(file_alloc_counters[1].fo_tally)),
          ("  Inode allocation", ""),
          ("    Allocated", str(file_alloc_counters[1].fo_tally_alloc_inode)),
          ("    Unallocated", str(file_alloc_counters[1].fo_tally_unalloc_inode)),
          ("    Unknown", str(file_alloc_counters[1].fo_tally_nullalloc_inode)),
          ("  Name allocation", ""),
          ("    Allocated", str(file_alloc_counters[1].fo_tally_alloc_name)),
          ("    Unallocated", str(file_alloc_counters[1].fo_tally_unalloc_name)),
          ("    Unknown", str(file_alloc_counters[1].fo_tally_nullalloc_name)),
          ("  Unallocated, unmatched", "TODO"),
          ("Current image's file (inode) tally", str(file_alloc_counters[1].inode_tally)),

          ("", ""),
          ("", ""),
          ("From retained objects", ""),

          ("Prior image's file (file object) tally", str(obj_alloc_counters[0].fo_tally)),
          ("  Inode allocation", ""),
          ("    Allocated", str(obj_alloc_counters[0].fo_tally_alloc_inode)),
          ("    Unallocated", str(obj_alloc_counters[0].fo_tally_unalloc_inode)),
          ("    Unknown", str(obj_alloc_counters[0].fo_tally_nullalloc_inode)),
          ("  Name allocation", ""),
          ("    Allocated", str(obj_alloc_counters[0].fo_tally_alloc_name)),
          ("    Unallocated", str(obj_alloc_counters[0].fo_tally_unalloc_name)),
          ("    Unknown", str(obj_alloc_counters[0].fo_tally_nullalloc_name)),
          ("  Unallocated, unmatched", "TODO"),
          ("Prior image's file (inode) tally", str(obj_alloc_counters[0].inode_tally)),
          ("  (None, None) a counted (partition, inode)", str((None, None) in obj_alloc_counters[0]._inodes)),
          ("Current image's file (file object) tally", str(obj_alloc_counters[1].fo_tally)),
          ("  Inode allocation", ""),
          ("    Allocated", str(obj_alloc_counters[1].fo_tally_alloc_inode)),
          ("    Unallocated", str(obj_alloc_counters[1].fo_tally_unalloc_inode)),
          ("    Unknown", str(obj_alloc_counters[1].fo_tally_nullalloc_inode)),
          ("  Name allocation", ""),
          ("    Allocated", str(obj_alloc_counters[1].fo_tally_alloc_name)),
          ("    Unallocated", str(obj_alloc_counters[1].fo_tally_unalloc_name)),
          ("    Unknown", str(obj_alloc_counters[1].fo_tally_nullalloc_name)),
          ("  Unallocated, unmatched", "TODO"),
          ("Current image's file (inode) tally", str(obj_alloc_counters[1].inode_tally)),
          ("  (None, None) a counted (partition, inode)", str((None, None) in obj_alloc_counters[1]._inodes))
        ]

    summ_recs += [
      ("", ""),
      ("New files", str(len(new_files))),
      ("Deleted files", str(len(deleted_files))),
      ("Renamed files", str(len(renamed_files))),
      ("Files with modified content", str(len(modified_files))),
      ("Files with changed file properties", str(len(changed_files)))
    ]

    idifference.table(summ_recs)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("infile")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    if not args.infile.endswith("xml"):
        raise Exception("Input file should be a DFXML file, and should end with 'xml': %r." % args.infile)

    if not os.path.exists(args.infile):
        raise Exception("Input file does not exist: %r." % args.infile)

    main()

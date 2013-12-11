#!/usr/bin/env python3

import sys
import os

import logging
_logger = logging.getLogger(os.path.basename(__file__))

sys.path.append("..")
import Objects
import make_differential_dfxml

import copy
import collections
import subprocess #For pretty-printing with xmllint

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    d0 = Objects.DFXMLObject()
    d1 = Objects.DFXMLObject()

    #Make the objects interesting
    v0 = Objects.VolumeObject()
    v0.partition_offset = 512*63
    v0.fstype_str = "NTFS"
    _logger.debug("v0 = " + repr(v0))
    d0.append(v0)
    f0 = Objects.FileObject()
    f0.filename = "home/admin/.ssh/config"
    f0.alloc_inode = True
    f0.alloc_name = True
    f0.md5 = "2b00042f7481c7b056c4b410d28f33cf"
    v0.append(f0)

    v1 = Objects.VolumeObject()
    v1 = copy.copy(v0)
    v1.fstype_str = "ntfs"
    _logger.debug("v1 = " + repr(v1))
    d1.append(v1)

    #Output
    d0_fn = __file__ + "-d0.xml"
    d1_fn = __file__ + "-d1.xml"
    print(d0.to_dfxml(), file=open(d0_fn, "w"))
    print(d1.to_dfxml(), file=open(d1_fn, "w"))

    d01 = make_differential_dfxml.make_differential_dfxml(d0_fn, d1_fn)
    d01_fn = __file__ + "-d01.xml"

    print(d01.to_dfxml(), file=open(d01_fn, "w"))

    #Issue some pretty-print calls
    d0_pfn = __file__ + "-d0.dfxml"
    d1_pfn = __file__ + "-d1.dfxml"
    d01_pfn = __file__ + "-d01.dfxml"

    for (pre, post) in [(d0_fn, d0_pfn), (d1_fn, d1_pfn), (d01_fn, d01_pfn)]:
        with open(post, "wb") as outfile:
            subprocess.check_call(["xmllint", "--format", pre], stdout=outfile)

    #Test counts
    tallies_objtype = collections.defaultdict(lambda: 0)
    for obj in d01:
        tallies_objtype[type(obj)] += 1
    _logger.debug("Object type tallies: %s." % repr(tallies_objtype))
    _logger.debug("VolumeObject tallies: %s." % repr(tallies_objtype[Objects.VolumeObject]))


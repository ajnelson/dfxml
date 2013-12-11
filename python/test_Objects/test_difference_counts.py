#!/usr/bin/env python3

import sys
import os
import logging

sys.path.append("..")
import Objects
import make_differential_dfxml

import subprocess #For pretty-printing with xmllint

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    d0 = Objects.DFXMLObject()
    d1 = Objects.DFXMLObject()

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

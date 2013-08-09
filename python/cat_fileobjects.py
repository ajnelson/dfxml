#!/usr/bin/env python3
#Make a new DFXML file of all fileobjects in an input DFXML file.

__version__ = "0.0.1"

import sys
import xml.etree.ElementTree as ET
import dfxml

if sys.version < "3":
    sys.stderr.write("Due to Unicode issues with Python 2's ElementTree, Python 3 and up is required.\n")
    exit(1)

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <filename.xml>\n" % sys.argv[0])
        exit(1)
    print("""\
<?xml version="1.0" encoding="UTF-8"?>
<dfxml xmloutputversion="1.0">
  <creator version="1.0">
    <program>%s</program>
    <version>%s</version>
    <execution_environment>
      <command_line>%s</command_line>
    </execution_environment>
  </creator>\
""" % (sys.argv[0], __version__, " ".join(sys.argv)))
    for fi in dfxml.iter_dfxml(xmlfile=open(sys.argv[1], "rb"), preserve_elements=True):
        print(ET.tostring(fi.xml_element, encoding="unicode"))
    print("""</dfxml>""")

if __name__ == "__main__":
    main()

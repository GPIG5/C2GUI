#!/usr/bin/env python

#
# Generated Tue May 24 14:21:58 2016 by generateDS.py version 2.22b.
#
# Command line options:
#   ('-o', 'schema.py')
#   ('-s', 'schemaSubs.py')
#
# Command line arguments:
#   ..\schema\gpig.xsd
#
# Command line:
#   generateDS.py -o "schema.py" -s "schemaSubs.py" ..\schema\gpig.xsd
#
# Current working directory (os.getcwd()):
#   generateds
#

import sys
from lxml import etree as etree_

import c2ext.schema as supermod


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc


#
# Globals
#

ExternalEncoding = 'utf-8'


#
# Data representation classes
#


class gpigDataSub(supermod.gpigData):
    def __init__(self, gisposition=None):
        super(gpigDataSub, self).__init__(gisposition, )


supermod.gpigData.subclass = gpigDataSub


# end class gpigDataSub


class gisPositionSub(supermod.gisPosition):
    def __init__(self, position=None, timestamp=None, value=None):
        super(gisPositionSub, self).__init__(position, timestamp, value, )


supermod.gisPosition.subclass = gisPositionSub


# end class gisPositionSub


class positionSub(supermod.position):
    def __init__(self, extensiontype_=None):
        super(positionSub, self).__init__(extensiontype_, )


supermod.position.subclass = positionSub


# end class positionSub


class pointSub(supermod.point):
    def __init__(self, position=None):
        super(pointSub, self).__init__(position, )


supermod.point.subclass = pointSub


# end class pointSub


class coordSub(supermod.coord):
    def __init__(self, latitude=None, longitude=None):
        super(coordSub, self).__init__(latitude, longitude, )


supermod.coord.subclass = coordSub


# end class coordSub


class boundingBoxSub(supermod.boundingBox):
    def __init__(self, topleft=None, topright=None):
        super(boundingBoxSub, self).__init__(topleft, topright, )


supermod.boundingBox.subclass = boundingBoxSub


# end class boundingBoxSub


class polarSub(supermod.polar):
    def __init__(self, point=None, radius=None):
        super(polarSub, self).__init__(point, radius, )


supermod.polar.subclass = polarSub


# end class polarSub


class polySub(supermod.poly):
    def __init__(self, coords=None):
        super(polySub, self).__init__(coords, )


supermod.poly.subclass = polySub


# end class polySub


class timestampSub(supermod.timestamp):
    def __init__(self, date=None):
        super(timestampSub, self).__init__(date, )


supermod.timestamp.subclass = timestampSub


# end class timestampSub


class dataTypeSub(supermod.dataType):
    def __init__(self, extensiontype_=None):
        super(dataTypeSub, self).__init__(extensiontype_, )


supermod.dataType.subclass = dataTypeSub


# end class dataTypeSub


class blockageSub(supermod.blockage):
    def __init__(self, image=None):
        super(blockageSub, self).__init__(image, )


supermod.blockage.subclass = blockageSub


# end class blockageSub


class imageSub(supermod.image):
    def __init__(self, url=None):
        super(imageSub, self).__init__(url, )


supermod.image.subclass = imageSub


# end class imageSub


class deliverySub(supermod.delivery):
    def __init__(self):
        super(deliverySub, self).__init__()


supermod.delivery.subclass = deliverySub


# end class deliverySub


class depthSub(supermod.depth):
    def __init__(self, depth_member=None):
        super(depthSub, self).__init__(depth_member, )


supermod.depth.subclass = depthSub


# end class depthSub


class flowSub(supermod.flow):
    def __init__(self, flow_member=None):
        super(flowSub, self).__init__(flow_member, )


supermod.flow.subclass = flowSub


# end class flowSub


class gateSub(supermod.gate):
    def __init__(self, position=None):
        super(gateSub, self).__init__(position, )


supermod.gate.subclass = gateSub


# end class gateSub


class strandedPersonSub(supermod.strandedPerson):
    def __init__(self, image=None):
        super(strandedPersonSub, self).__init__(image, )


supermod.strandedPerson.subclass = strandedPersonSub


# end class strandedPersonSub


class waterEdgeSub(supermod.waterEdge):
    def __init__(self):
        super(waterEdgeSub, self).__init__()


supermod.waterEdge.subclass = waterEdgeSub


# end class waterEdgeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'blockage'
        rootClass = supermod.blockage
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'blockage'
        rootClass = supermod.blockage
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from io import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'blockage'
        rootClass = supermod.blockage
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'blockage'
        rootClass = supermod.blockage
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    main()

import Core.protobuf.qsmq_pb2 as pb
from Core.abstract_classes import ProtobufTranscoder


class BoundingBox(ProtobufTranscoder):
    def __init__(self, x, y, w, h):
        """Python representation of the bounding box that has protobuf definition.

        Parameters
        ----------
        x : int
            center of bounding box in x-coordinate
        y : int
            center of bounding box in y-coordinate
        w : int
            width of bounding box
        h : int
            height of bounding box

        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return "{}(x={} y={} w={} h={})".format(self.__class__.__name__, self.x, self.y, self.w, self.h)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.w == other.w and self.h == other.h

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        if dest is None:
            dest = pb.BBox()
        dest.x, dest.y, dest.w, dest.h = self.x, self.y, self.w, self.h
        return dest

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage):
        assert isinstance(pbmessage, pb.BBox)
        return cls(pbmessage.x, pbmessage.y, pbmessage.w, pbmessage.h)

    @classmethod
    def fromXY1XY2(cls, x1, y1, x2, y2):
        x = int((x1 + x2) / 2)
        y = int((y1 + y2) / 2)
        w = int(abs(x1 - x2))
        h = int(abs(y1 - y2))
        return cls(x, y, w, h)

    @classmethod
    def fromXY1WH(cls, x1, y1, w, h):
        x = int(x1 + w / 2)
        y = int(y1 + h / 2)
        return cls(x, y, w, h)

    def XY1(self):
        x1 = self.x - int(self.w / 2)
        y1 = self.y - int(self.h / 2)
        return x1, y1

    def XY2(self):
        x2 = self.x + int(self.w / 2)
        y2 = self.y + int(self.h / 2)
        return x2, y2

    def WH(self):
        return self.w, self.h


class Point(ProtobufTranscoder):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}(x={},y={})".format(self.__class__.__name__, self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        if dest is None:
            dest = pb.Point()
        dest.x, dest.y = self.x, self.y
        return dest

    def setFromProtobufEquivalent(self, pbmessage):
        assert isinstance(pbmessage, pb.Point)
        self.x, self.y = pbmessage.x, pbmessage.y

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage, sharedStorage=None):
        assert isinstance(pbmessage, pb.Point)
        return cls(pbmessage.x, pbmessage.y)


class Polygon(ProtobufTranscoder):
    def __init__(self, points=[]):
        assert isinstance(points, list) and (len(points) == 0 or isinstance(points[0], Point))
        self.points = points

    def __repr__(self):
        repr = "{}(len={} ".format(self.__class__.__name__, len(self.points))
        if len(self.points) > 0:
            if len(self.points) > 6:
                repr += ",".join(map(str, self.points[:5])) + "..."
            else:
                repr += ",".join(map(str, self.points))
        repr += ")"
        return repr

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        if dest is None:
            dest = pb.Polygon()
        pp = [p.getProtobufEquivalent() for p in self.points]
        dest.p.extend(pp)
        dest.closed = True
        return dest

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage):
        return cls([Point.fromProtobufEquivalent(cc) for cc in pbmessage.p])


class ObjectSegmentation(ProtobufTranscoder):
    def __init__(self, polygons=[]):
        assert isinstance(polygons, list)
        assert len(polygons) == 0 or isinstance(polygons[0], Polygon)
        self.polygons = polygons

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        if dest is None:
            dest = pb.SegmObject()
        dest.polys.extend([poly.getProtobufEquivalent() for poly in self.polygons])
        return dest

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage):
        return cls([Polygon.fromProtobufEquivalent(poly) for poly in pbmessage.polys])


if __name__ == '__main__':
    p1 = Polygon()
    print(p1)
    p1 = Polygon([Point(1, 20000)])
    print(p1)
    p1 = Polygon([Point(r, r) for r in range(4)])
    print(p1)
    p1 = Polygon([Point(r, r) for r in range(8)])
    print(p1)
    p1 = Polygon([1, 2, 3, 4])
    print(p1)

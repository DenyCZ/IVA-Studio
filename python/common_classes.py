import json
import time

import numpy as np

import Core.protobuf.qsmq_pb2 as pb
from Core.abstract_classes import ProtobufTranscoder
from Core.geometric_classes import Point, BoundingBox, ObjectSegmentation
from Core.messages_transcode import encodeimage, decodeimage


class ObjectAnnotation(ProtobufTranscoder):
    pbekvivalent = pb.ObjectAnnotation

    def __init__(self, class_id=0, score=0.0, bbox=None, segmentation=None, features={}, floorplanPoint=None, **kwargs):
        assert isinstance(class_id, int)
        assert isinstance(score, (float, int))
        assert bbox is None or isinstance(bbox, BoundingBox)
        assert floorplanPoint is None or isinstance(floorplanPoint, Point)
        assert segmentation is None or isinstance(segmentation, ObjectSegmentation)
        assert isinstance(features, dict)
        self.class_id = class_id
        self.score = score
        self.bbox = bbox
        self.segmentation = segmentation
        self.features = features
        self.floorplanPoint = floorplanPoint

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        if dest is None:
            dest = self.pbekvivalent()
        dest.class_id = self.class_id
        dest.score = self.score
        if not self.bbox is None:
            self.bbox.getProtobufEquivalent(dest=dest.bbox)
        if not self.segmentation is None:
            self.segmentation.getProtobufEquivalent(dest=dest.segm)
        if not self.floorplanPoint is None:
            self.floorplanPoint.getProtobufEquivalent(dest=dest.florplanpoint)
        dest.features = json.dumps(self.features)
        return dest

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage, sharedStorage=None):
        bbox = BoundingBox.fromProtobufEquivalent(pbmessage.bbox) if pbmessage.HasField("bbox") else None
        segmentation = ObjectSegmentation.fromProtobufEquivalent(pbmessage.segm) if pbmessage.HasField("segm") else None
        features = json.loads(pbmessage.features)
        floorplanPoint = Point.fromProtobufEquivalent(pbmessage.florplanpoint) if pbmessage.HasField(
            "florplanpoint") else None
        ret = cls(class_id=pbmessage.class_id,
                  score=pbmessage.score,
                  bbox=bbox,
                  segmentation=segmentation,
                  features=features,
                  floorplanPoint=floorplanPoint)
        return ret


class AnnotatedImageView(ProtobufTranscoder):
    pbekvivalent = pb.ImageView

    def __init__(self, convType, convParams, image, objannotations=[]):
        #assert isinstance(convType, )
        assert isinstance(convParams, tuple)
        if image is not None:
            assert isinstance(image, np.ndarray) and len(image.shape) == 3
        assert isinstance(objannotations, list)
        assert len(objannotations) == 0 or isinstance(objannotations[0], ObjectAnnotation)
        self.convType = convType
        self.convParams = convParams
        self.image = image
        self.imgKey = None
        self.objannotations = objannotations

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        assert hasattr(sharedStorage, 'uniqueKey')
        assert hasattr(sharedStorage, 'set')
        if dest is None:
            dest = self.pbekvivalent()
        dest.conversionType = self.convType
        dest.conversionParams.extend(list(self.convParams))
        if self.imgKey is None:
            imgbuf = encodeimage(self.image)
            key = sharedStorage.uniqueKey()
            sharedStorage.set(key, imgbuf)
            self.imgKey = key
        dest.imgKey = self.imgKey
        if len(self.objannotations) > 0:
            pbobjs = [objann.getProtobufEquivalent(sharedStorage=sharedStorage) for objann in self.objannotations]
            dest.objectAnnotations.extend(pbobjs)
        return dest

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage, sharedStorage=None):
        assert hasattr(sharedStorage, 'get')
        imgkey = pbmessage.imgKey
        imgbuf = sharedStorage.get(imgkey)
        image = decodeimage(imgbuf)
        pbannotations = [ObjectAnnotation.fromProtobufEquivalent(objann) for objann in pbmessage.objectAnnotations]
        ret = cls(convType=pbmessage.conversionType,
                  convParams=tuple(pbmessage.conversionParams),
                  image=image,
                  objannotations=pbannotations)
        ret.imgKey = imgkey
        return ret


class AnnotatedCamera(ProtobufTranscoder):
    pbekvivalent = pb.CameraImage

    def __init__(self, videoStreamName, imageViews=[], timestamp=None):
        assert isinstance(videoStreamName, str)
        assert isinstance(imageViews, list)
        assert len(imageViews) == 0 or isinstance(imageViews[0], AnnotatedImageView)
        if not isinstance(timestamp, (int, float)):
            timestamp = time.time()
        self.videoStreamName = videoStreamName
        self.imageViews = imageViews
        self.timestamp = timestamp

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        if dest is None:
            dest = self.pbekvivalent()
        dest.videoStreamName = self.videoStreamName
        dest.timestamp = self.timestamp
        dest.views.extend([view.getProtobufEquivalent(sharedStorage=sharedStorage) for view in self.imageViews])
        return dest

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage, sharedStorage=None):
        views = [AnnotatedImageView.fromProtobufEquivalent(view, sharedStorage=sharedStorage) for view in
                 pbmessage.views]
        return cls(videoStreamName=pbmessage.videoStreamName,
                   imageViews=views,
                   timestamp=pbmessage.timestamp)

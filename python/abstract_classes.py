class ProtobufTranscoder:
    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        raise NotImplementedError
    @classmethod
    def fromProtobufEquivalent(cls, pbmessage, sharedStorage=None):
        raise NotImplementedError
    def serialize(self, sharedStorage=None):
        pbobj = self.getProtobufEquivalent(sharedStorage=sharedStorage)
        return pbobj.SerializeToString()
    @classmethod
    def parse(cls, buffer, sharedStorage=None):
        pbobj = cls.pbekvivalent()
        pbobj.ParseFromString(buffer)
        return cls.fromProtobufEquivalent(pbobj, sharedStorage=sharedStorage)


class SharedStorage:
    def get(self, key):
        raise NotImplementedError
    def set(self, key, data):
        raise NotImplementedError
    def uniqueKey(self):
        raise NotImplementedError



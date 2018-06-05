"""Base classes for subclasses working with Protobuf and Redis

Authors
-------
Martin Cerny, martin.cerny@quantasoft.com
"""


class ProtobufTranscoder:
    """Base class for transocding to/from protobuf.

    This is a base class for transcoding to/from protobuf. All its' subclasses must implement methods
    `getProtobufEquivalent` and `fromProtobufEquivalent`.

    See Also
    --------
    abstract_classes : AnnotatedCamera, AnnotatedImageView, ObjectAnnotation
    """

    def getProtobufEquivalent(self, dest=None, sharedStorage=None):
        """
        Abstract function that must be implemented in subclasses.

        Parameters
        ----------
        dest : None or Protobuf class
            If None, the new object must be created.
            Otherwise: Protobuf class in the definition of `qsmq.proto` and it's equivalent representation as a subclass.
        sharedStorage : SharedStorage
            This value specifies that message is passed to redis and only the reference
            to that object is passed in the message. It is suitable for large objects.

        Returns
        -------
        object of type desc
            Returns the same type as `desc`. If `desc==None` then new object returned.

        """
        raise NotImplementedError

    @classmethod
    def fromProtobufEquivalent(cls, pbmessage, sharedStorage=None):
        """

        Parameters
        ----------
        pbmessage : string
            The string representation of the object.
        sharedStorage : SharedStorage
            This value specifies that message is passed to redis and only the reference
            to that object is passed in the message. It is suitable for large objects.

        Returns
        -------
        obj
            Protobuf representation of the string in `pbmessage`.

        """
        raise NotImplementedError

    def serialize(self, sharedStorage=None):
        """
        Serialize the object into string

        Parameters
        ----------
        sharedStorage ; SharedStorage
            This value specifies that message is passed to redis and only the reference
            to that object is passed in the message. It is suitable for large objects.

        Returns
        -------
        str
            String representation of the protobuf object.
        """
        pbobj = self.getProtobufEquivalent(sharedStorage=sharedStorage)
        return pbobj.SerializeToString()

    @classmethod
    def parse(cls, buffer, sharedStorage=None):
        """
        Deserealization of the buffer.

        Parameters
        ----------
        buffer : bytes
            Serialized string.
        sharedStorage : SharedStorage
            This value specifies that message is passed to redis and only the reference
            to that object is passed in the message. It is suitable for large objects.

        Returns
        -------
        obj
            Object that is parsed from buffer.

        """
        pbobj = cls.pbekvivalent()
        pbobj.ParseFromString(buffer)
        return cls.fromProtobufEquivalent(pbobj, sharedStorage=sharedStorage)


class SharedStorage:
    """Global in memory storage for large files.

    To reduce the size of exchange message in RabbitMQ system the shared storage, e.g. Redis is used. It's subclasses
    must implement methods `get`, `set`, `uniqueKey`.

    See Also
    --------
    Implementations of subclasses
        * messages_transcode.RedisSharedStorage

    """

    def get(self, key):
        raise NotImplementedError

    def set(self, key, data):
        raise NotImplementedError

    def uniqueKey(self):
        raise NotImplementedError

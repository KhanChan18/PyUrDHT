import chordspacemath as space
import threading

class PeerInfo(object):

    """
        Peerinfo does not actually do much
        I might just reduce it to a 2-tuple

        right now UrDHT is not enforcing a mapping of hashIDs to servers
    """

    def __init__(self, hashID, addr, loc):
        """
            hashID is a string encoded in multihash format
            addr is whatever the network module needs to connect
        """
        self.id = hashID
        self.addr = addr
        self.loc = loc

    def __str__(self):
        return """{"id":"%s", "addr":"%s", "loc":[%f,%f]}""" % \
            (self.id, self.addr, self.loc[0], self.loc[1])

    def __hash__(self):
        return hash((hash(self.id), hash(self.addr)))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return str(self)


class ChordLogic(object):
    """docstring for ChordLogic"""
    def __init__(self, peerinfo, key):
        self.network = None
        self.database = None
        self.key = key
        self.shortPeers = []
        self.longPeers = []
        self.seekCandidates = []
        self.notifiedMe = []
        self.locPeerDict = {}
        self.info = peerinfo
        if peerinfo.loc is None:
            self.loc = space.idToPoint(2, self.info.id)
            self.info.loc = self.loc
        else:
            self.loc = peerinfo.loc
        self.janitorThread = None
        self.peersLock = threading.Lock()
        self.notifiedLock = threading.Lock()

    def setup(self, network, database):
        self.network = network
        self.database =  database
        self.janitorThread =  ChordJanitor(self)

    def seek(self, key):
        loc = space.idToPoint(key)


    def getNotified(self, origin):
        with self.notifiedLock:
            self.notifiedMe.append(origin)
        return True

class ChordJanitor(object):
    def __init__(self, parent):
        """
        Initialized the janitor with parent as the node that created it.
        """
        threading.Thread.__init__(self)
        self.parent = parent
        self.running = True
        self.runningLock = threading.Lock()
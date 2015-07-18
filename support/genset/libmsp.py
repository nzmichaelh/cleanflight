import collections
import struct

FORMATS = {
    (1, False): 'B',
    (2, False): 'H',
    (4, False): 'I',
    (1, True): 'c',
    (2, True): 'h',
    (4, True): 'i',
}

class Field:
    def __init__(self, name, size, signed, count=None):
        self.name = name
        self.size = size
        self.signed = signed
        self.count = count

class Message:
    def decode(self, body):
        for name in self.PARAMS:
            field = getattr(self, name)
            fmt = FORMATS[(field.size, field.signed)]
            size = struct.calcsize(fmt)
            if field.count is None:
                total = size
            elif field.count < 0:
                total = len(body)
            else:
                total = field.count*size
            if total > len(body):
                if field.count is None:
                    setattr(self, name, 0)
                else:
                    setattr(self, name, [])
                body = b''
                continue

            if field.count is None:
                value = struct.unpack_from('<' + fmt, body, 0)[0]
            else:
                count = field.count
                if count < 0:
                    count = len(body) // size
                value = tuple(struct.unpack_from('<' + fmt, body, i*size)[0] for i in range(count))
                if size == 1 and field.signed:
                    value = b''.join(value)

            body = body[total:]
            setattr(self, name, value)
        if body:
            print('{}: Left {} bytes behind.'.format(self.__class__.__name__, len(body)))
            
    def __repr__(self):
        params = ' '.join('{}: {}'.format(x, getattr(self, x)) for x in self.PARAMS)
        if params:
            return '<{} {}>'.format(self.__class__.__name__, params)
        else:
            return '<{}>'.format(self.__class__.__name__)
    
class Enum:
    @classmethod
    def name(cls, id):
        for name, value in cls.__dict__.items():
            if value == id:
                return name
        else:
            return None

class Registry:
    def __init__(self):
        self.pgs = {}

    def register(self, msg):
        assert msg.PGN not in self.pgs
        self.pgs[msg.PGN] = msg

    def decode(self, pgn, body):
        if pgn in self.pgs:
            pg = self.pgs[pgn]()
            pg.decode(body)
            return pg
        else:
            return None


class Link:
    def __init__(self, port, registry):
        self.port = port
        self.registry = registry
        self.state = None
        self.cmd = None

    def frame(self, cmd, body=b''):
        payload = bytes((len(body), cmd)) + body
        chk = 0
        for b in payload:
            chk ^= b
        return b'$M<' + payload + bytes((chk & 0xFF,))

    def request(self, pg):
        if isinstance(pg, Message):
            pgn = pg.PGN
        else:
            pgn = pg
        self.port.write(self.frame(pgn))

    def feed(self, data):
        for ch in data:
            if self.state is None:
                if ch == ord('$'):
                    self.state = 'm'
                    self.body = []
            elif self.state == 'm':
                if ch == ord('M'):
                    self.state = 'arrow'
                else:
                    self.state = None
            elif self.state == 'arrow':
                if ch == ord('>'):
                    self.state = 'count'
                else:
                    self.state = None
            elif self.state == 'count':
                self.count = ch
                self.state = 'cmd'
            elif self.state == 'cmd':
                self.cmd = ch
                self.state = 'payload'
            elif self.state == 'payload':
                self.body.append(ch)
            elif self.state == 'chk':
                expect = self.count ^ self.cmd
                for b in self.body:
                    expect ^= b
                if expect == ch:
                    yield self.registry.decode(self.cmd, bytes(self.body))
                self.state = None
            else:
                assert False
                self.state = None

            if self.state == 'payload' and len(self.body) == self.count:
                self.state = 'chk'

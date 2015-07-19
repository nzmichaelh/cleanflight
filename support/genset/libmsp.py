import struct


class Field:

    """A single typed field."""

    FMTS = {
        (1, False): 'B',
        (2, False): 'H',
        (4, False): 'I',
        (1, True): 'c',
        (2, True): 'h',
        (4, True): 'i',
    }

    def __init__(self, name, size, signed, count=None):
        self.name = name
        self.size = size
        self.signed = signed
        self.count = count

    @property
    def is_array(self):
        return self.count is not None

    @property
    def is_var_array(self):
        return self.count < 0

    @property
    def fmt(self):
        return self.FMTS[(self.size, self.signed)]

    @property
    def wire_size(self):
        return struct.calcsize(self.fmt)

    @property
    def is_char(self):
        return self.size == 1 and self.signed

    def unpack(self, body, offset):
        return struct.unpack_from('<' + self.fmt, body, offset)[0]


class Message:

    """A message made of fields."""

    def decode(self, body):
        for name in self.PARAMS:
            f = getattr(self, name)
            fmt = f.fmt
            size = f.wire_size
            if not f.is_array:
                total = size
            elif f.is_var_array:
                total = len(body)
            else:
                total = f.count * size

            if total > len(body):
                if not f.is_array:
                    setattr(self, name, 0)
                else:
                    setattr(self, name, [])
                body = b''
                continue

            if not f.is_array:
                value = f.unpack(body, 0)
            else:
                count = total // size
                value = tuple(f.unpack(body, i * size) for i in range(count))
                if f.is_char:
                    value = b''.join(value)

            body = body[total:]
            setattr(self, name, value)
        if body:
            print('{}: Left {} bytes behind.'.format(
                self.__class__.__name__, len(body)))

    def __repr__(self):
        name = self.__class__.__name__
        names = self.PARAMS
        values = (getattr(self, x) for x in names)
        pairs = ('{}: {}'.format(x, y) for x, y in zip(names, values))
        params = ' '.join(pairs)

        if params:
            return '<{} {}>'.format(name, params)
        else:
            return '<{}>'.format(name)


class Enum:

    """An enumeration."""
    @classmethod
    def name(cls, id):
        for name, value in cls.__dict__.items():
            if value == id:
                return name
        else:
            return None


class Registry:

    """A registry of messages including a map from PGN to message."""

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

    """A two way link implementing the MSP framing."""

    def __init__(self, port, registry):
        self.port = port
        self.registry = registry
        self.state = None
        self.cmd = None
        self.body = []

        self.bytes_rxed = 0
        self.frames_rxed = 0
        self.chk_fails = 0

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
        frame = self.frame(pgn)
        wrote = self.port.write(frame)
        assert wrote == len(frame)

    def feed(self, data):
        self.bytes_rxed += len(data)

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
                self.count = ch + 3
                self.body = [ch]
                self.state = 'payload'
            elif self.state == 'payload':
                self.body.append(ch)

                if len(self.body) == self.count:
                    expect = 0
                    for b in self.body:
                        expect ^= b
                    if expect == 0:
                        count, cmd, body, chk = self.body[0], self.body[
                            1], self.body[2:-1], self.body[-1]
                        self.frames_rxed += 1
                        yield self.registry.decode(cmd, bytes(body))
                    else:
                        self.chk_fails += 1
                    self.state = None
            else:
                assert False
                self.state = None

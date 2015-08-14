import struct


class Field:

    """A single typed field."""

    FMTS = {
        (1, False): 'B',
        (2, False): 'H',
        (4, False): 'I',
        (1, True): 'b',
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

    def decode(self, body, offset):
        return struct.unpack_from('<' + self.fmt, body, offset)[0]

    def encode(self, value):
        return struct.pack('<' + self.fmt, value)

class InnerMessage:
    def __init__(self, name, klass, count=None):
        self.name = name
        self.klass = klass
        self.count = count
        self.template = klass()

    is_char = False

    @property
    def is_array(self):
        return self.count is not None

    @property
    def is_var_array(self):
        return self.count < 0

    @property
    def wire_size(self):
        return self.template.wire_size

    def decode(self, body, offset):
        inner = self.klass()
        inner.decode(body[offset:])
        return inner

class Message:

    """A message made of fields."""
    def params(self):
        return [getattr(self.__class__, name) for name in self.PARAMS]

    def decode(self, body, offset=0):
        for param in self.params():
            f = param
            size = f.wire_size
            if not f.is_array:
                total = size
            elif f.is_var_array:
                total = len(body)
            else:
                total = f.count * size

            if total > len(body):
                if not f.is_array:
                    setattr(self, f.name, 0)
                else:
                    setattr(self, f.name, [])
                body = b''
                continue

            if not f.is_array:
                value = f.decode(body, 0)
            else:
                count = total // size
                value = tuple(f.decode(body, i * size) for i in range(count))
                if f.is_char:
                    value = b''.join(value)

            body = body[total:]
            setattr(self, f.name, value)
        return body

    def encode(self):
        body = b''
        for param in self.params():
            body += param.encode(getattr(self, param.name))
        return body

    @property
    def wire_size(self):
        return sum(x.wire_size for x in self.params())

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

    @classmethod
    def flags(cls, ids):
        values = []
        for name, value in cls.__dict__.items():
            if isinstance(value, int):
                if ids & value:
                    values.append((value, name))
        values.sort(key=lambda x: x[0])
        return ' | '.join(x[-1] for x in values)


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

    def send(self, msg):
        frame = self.frame(msg.PGN, msg.encode())
        wrote = self.port.write(frame)
        assert wrote == len(frame)

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

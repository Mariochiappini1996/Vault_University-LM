from io import BytesIO
import helpers

class Block:

    def __init__(self, version, prev_hash, merkle_root, timestamp, bits, nonce):
        self.version = version
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce

    @classmethod
    def parse(cls, byte_string):
        reader = BytesIO(byte_string)
        version = reader.read(4)
        prev_hash = reader.read(32)
        merkle_root = reader.read(32)
        timestamp = reader.read(4)
        bits = reader.read(4)
        nonce = reader.read(4)
        return cls(version[::-1], prev_hash[::-1], merkle_root[::-1],\
                   timestamp[::-1], bits[::-1], nonce[::-1]) 

    def serialize(self):
        return self.version[::-1] + self.prev_hash[::-1] + \
               self.merkle_root[::-1] + self.timestamp[::-1] +\
               self.bits[::-1] + self.nonce[::-1]

    def hash(self):
        return helpers.hash256(self.serialize())[::-1] 

    def target(self):
        return int.from_bytes(self.bits[1:], 'big') * 256**(self.bits[0] - 3)

    def is_valid_target(self):
        return int.from_bytes(self.hash(),'big') <= self.target()

    def __str__(self):
        out = dict()
        out['version'] = self.version.hex()
        out['prev_hash'] = self.prev_hash.hex()
        out['merkle_root'] = self.merkle_root.hex()
        out['timestamp'] = self.timestamp.hex()
        out['bits'] = self.bits.hex()
        out['nonce'] = int(self.nonce.hex(), 16)
        return out.__str__()

    def update_nonce(self, i):
        self.nonce = i.to_bytes(4, 'big')

if __name__ == '__main__':
    header = '00c0b32d3cbe7b47fc6a62c2f3d60b26d8d11fab00bd1be0972a00000000000000000000699a838304ba15e09b2b01dea786ff83355763959401bb04ce38de8993099ff8919adc6984060217cd51d8c4'
    blk = Block.parse(bytes.fromhex(header))
    print(blk)

    print(blk.hash().hex())
    print(blk.is_valid_target())

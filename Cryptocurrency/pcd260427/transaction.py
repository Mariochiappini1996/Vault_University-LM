import helpers
from script import Script


class TxOut:

    def __init__(self, value, script_pk):
        self.value = value
        self.script_pk = script_pk

    @classmethod
    def parse(cls, reader):
        value = reader.read(8)[::-1]
        script_len = helpers.varint2int(reader)
        script_pk = Script.parse(reader, script_len)
        return cls(value, script_pk)

    def __str__(self):
        out = dict()
        out['value'] = int.from_bytes(self.value, 'big')
        out['script_pk'] = str(self.script_pk)
        return out.__str__()


class TxIn:

    def __init__(self, prev_tx, prev_idx, script_sig, sequence):
        self.prev_tx = prev_tx
        self.prev_idx = prev_idx
        self.script_sig = script_sig
        self.sequence = sequence

    @classmethod
    def parse(cls, reader):
        prev_tx = reader.read(32)[::-1]
        prev_idx = reader.read(4)
        script_len = helpers.varint2int(reader)
        script_sig = Script.parse(reader, script_len)
        sequence = reader.read(4)
        return cls(prev_tx, prev_idx, script_sig, sequence)

    def __str__(self):
        out = dict()
        out['prev_tx'] = self.prev_tx.hex()
        out['prev_idx'] = int.from_bytes(self.prev_idx)
        out['script_sig'] = str(self.script_sig)
        out['sequence'] = self.sequence.hex()
        return out.__str__()


class Tx:

    def __init__(self, version, inputs, outputs, locktime):
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime

    @classmethod
    def parse(cls, reader):
        version = reader.read(4)[::-1]
        n_in = helpers.varint2int(reader)
        inputs = [TxIn.parse(reader) for _ in range(n_in)]
        n_out = helpers.varint2int(reader)
        outputs = [TxOut.parse(reader) for _ in range(n_out)]
        locktime = reader.read(4)
        return cls(version, inputs, outputs, locktime)

    def __str__(self):
        out = dict()
        out['version'] = int.from_bytes(self.version, 'big')
        out['inputs'] = [tx_in.__str__() for tx_in in self.inputs]
        out['outputs'] = [tx_out.__str__() for tx_out in self.outputs]
        out['locktime'] = self.locktime.hex()
        return out.__str__()

if __name__ == '__main__':
    from io import BytesIO

    txhex = '0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce2585\
             7fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f77\
             32e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831c\
             c56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a\
             62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab3\
             7397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286b\
             ee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482eca\
             d7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b86\
             43f656b412a3ac00000000'
    txhex = '010000000110ee96aa946338cfd0b2ed0603259cfe2f5458c32ee4bd7b88b583769c6b046e010000006b483045022100e5e4749d539a163039769f52e1ebc8e6f62e39387d61e1a305bd722116cded6c022014924b745dd02194fe6b5cb8ac88ee8e9a2aede89e680dcea6169ea696e24d52012102b4b754609b46b5d09644c2161f1767b72b93847ce8154d795f95d31031a08aa2ffffffff028098f34c010000001976a914a134408afa258a50ed7a1d9817f26b63cc9002cc88ac8028bb13010000001976a914fec5b1145596b35f59f8be1daf169f375942143388ac00000000'

    reader = BytesIO(bytes.fromhex(txhex))
    tx = Tx.parse(reader)
    print(tx)

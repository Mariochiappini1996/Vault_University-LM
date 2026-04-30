import secrets
import helpers
from io import BytesIO
import transaction

# Testing TxOut
value = secrets.token_bytes(4) + 4*b'\x00'
n = 515
script_len = helpers.int2varint(n)
script_pk = secrets.token_bytes(n)

bs = value + script_len + script_pk
reader = BytesIO(bs)

tx_out = transaction.TxOut.parse(reader)

print(tx_out)


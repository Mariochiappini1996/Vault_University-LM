def varint2int(reader):
    first = int.from_bytes(reader.read(1))
    if first <= 252:
        return first
    if first == 253:
        return int.from_bytes(reader.read(2)[::-1])
    if first == 254:
        return int.from_bytes(reader.read(4)[::-1])
    if first == 255:
        return int.from_bytes(reader.read(8)[::-1])

def int2varint(n):
    if n < 0 or n >= 2**64:
        return None
    if n <= 252:
        return n.to_bytes(1, 'little')
    if n < 2**16:
        return int(253).to_bytes(1,'little') + n.to_bytes(2, 'little')
    if n < 2**32:
        return int(254).to_bytes(1,'little') + n.to_bytes(4, 'little')
    if n < 2**64:
        return int(255).to_bytes(1,'little') + n.to_bytes(8, 'little')
        


if __name__ == '__main__':
    from io import BytesIO
    h = 'fd0302'
    reader = BytesIO(bytes.fromhex(h))

    print(varint2int(reader))

    print(int2varint(515).hex())

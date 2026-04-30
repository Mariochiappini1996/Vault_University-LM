import helpers

class Script:

    opcodes = helpers.opcodes('opcodes.cfg')

    def __init__(self, cmds):
        self.cmds = cmds

    @classmethod
    def parse(cls, reader, script_len):
        cmds = []
        counter = 0
        while counter < script_len:
            first = int.from_bytes(reader.read(1))
            counter += 1
            if 1 <= first <= 75:
                cmds.append(reader.read(first))
                counter += first
            elif first == 76:
                cmd_len = int.from_bytes(reader.read(1))
                cmds.append(reader.read(cmd_len))
                counter += cmd_len + 1
            elif first == 77:
                cmd_len = int.from_bytes(reader.read(2), 'little')
                cmds.append(reader.read(cmd_len))
                counter += cmd_len + 2
            elif first == 78:
                cmd_len = int.from_bytes(reader.read(4), 'little')
                cmds.append(reader.read(cmd_len))
                counter += cmd_len + 4
            else:
                cmds.append(first)
        return cls(cmds)


    def __str__(self):
        return ' '.join([Script.opcodes[cmd] if type(cmd) == int else cmd.hex() for cmd in self.cmds])

if __name__ == '__main__':
    from io import BytesIO
    script_hex = '00142f4cf673d4ba8c2620e03eb5fb6c09c124a3cedb'
    script_len = len(script_hex) // 2
    sc = Script.parse(BytesIO(bytes.fromhex(script_hex)), script_len)

    print(sc)


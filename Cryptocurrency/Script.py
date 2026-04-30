import helpers



class Script:
    def __init__(self, cmds):
        self.cmds = cmds
    
    @classmethod
    def parse(cls, reader, script_len):
        cmds = []
        count = 0
        while count < script_len:
            first = int.from_bytes(reader.read(1), "little")
            count += 1
            if 1 <= first <= 75:
                cmds.append(reader.read(first))
                count += first
            elif first == 76:
                cmds.len = int.from_bytes(reader.read(1), "little")
                cmds.append(reader.read(cmds.len))
                count += cmds.len + 1
            elif first == 77:
                cmds.len = int.from_bytes(reader.read(2), "little")
                cmds.append(reader.read(cmds.len))
                count += cmds.len + 2
            elif first == 78:
                cmds.len = int.from_bytes(reader.read(4), "little")
                cmds.append(reader.read(cmds.len))
                count += cmds.len + 4
            else:
                cmds.append(first)
        return cls(cmds)
    
    def __str__(self):
        return " ".join([str(cmd) for cmd in self.cmds])

if __name__ == "__main__":
    from io import BytesIO
    script_hex = '410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac'
    
    script_len = len(script_hex) // 2
    sc = Script.parse(BytesIO(bytes.fromhex(script_hex)), script_len)
    print(sc)
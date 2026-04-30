from configparser import ConfigParser

def opcodes(fname):
    config = ConfigParser()
    config.read(fname)
    return {code: int(config["OPCODES"][code], 16) for code in config["OPCODES"]}

if __name__ == "__main__":
    print(opcodes("opcode.cfg"))
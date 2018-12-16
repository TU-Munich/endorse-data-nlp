import glob


def read_all_files(path):
    return glob.glob(path + "*")

def read_a_files(path):
    return glob.glob(path)
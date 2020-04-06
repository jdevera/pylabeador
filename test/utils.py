import os


def data_file_open(filename):
    test_dir = os.path.dirname(__file__)
    path = os.path.join(test_dir, filename)
    return open(path, 'r')


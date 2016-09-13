__author__ = 'hsi'


def get_sub_dict(dictionary, keys):
    return dict(zip(keys, map(dictionary.get, keys)))


def add_prefix_to_keys(prefix, dictionary):
    return dict(map(lambda e: (prefix + e[0], e[1]), list(dictionary.iteritems())))
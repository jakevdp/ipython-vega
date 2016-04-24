import os.path
import cgi
import json
import codecs
import collections
import pandas as pd


def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def scripts(paths):
    """ Generate script tags for the given path """
    out = []
    for path in paths:
        out.append(script(path))
    return u'\n'.join(out)


def abs_path(path):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        path)


def get_content(path):
    """ Get content of file """
    with codecs.open(abs_path(path), encoding='utf-8') as f:
        return f.read()

def sanitize(value):
    """ Makes sure that the data is compatible with JSON """
    if pd.isnull(value):
        # json doesn't support nan
        return None
    return value


def data(data, columns):
    """ Creates a dictionary from a pandas data frame """
    res = []
    for row in data.tolist():
        res.append({k: sanitize(v) for k, v in zip(columns, row)})
    return res


def escape(string):
    """ Escape the string """
    return cgi.escape(string, quote=True)
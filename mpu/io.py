#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Reading and writing common file formats."""

from __future__ import absolute_import

# core modules
from datetime import datetime
import csv
import hashlib
import json
import os
import pickle
import platform
import sys

# Make it work for Python 2+3 and with Unicode
import io as io_stl
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# internal modules
from mpu.datastructures import EList


def read(filepath, **kwargs):
    """
    Read a file.

    Supported formats:

    * CSV
    * JSON, JSONL
    * pickle

    Parameters
    ----------
    filepath : str
        Path to the file that should be read. This methods action depends
        mainly on the file extension.
    kwargs : dict
        Any keywords for the specific file format. For CSV, this is
        'delimiter', 'quotechar', 'skiprows', 'format'

    Returns
    -------
    data : str or bytes
    """
    if filepath.lower().endswith('.csv'):
        return _read_csv(filepath, kwargs)
    elif filepath.lower().endswith('.json'):
        with open(filepath) as data_file:
            data = json.load(data_file, **kwargs)
        return data
    elif filepath.lower().endswith('.jsonl'):
        return _read_jsonl(filepath, kwargs)
    elif filepath.lower().endswith('.pickle'):
        with open(filepath, 'rb') as handle:
            data = pickle.load(handle)
        return data
    elif (filepath.lower().endswith('.yml') or
          filepath.lower().endswith('.yaml')):
        raise NotImplementedError('YAML is not supported, because you need '
                                  'PyYAML in Python3. '
                                  'See '
                                  'https://stackoverflow.com/a/42054860/562769'
                                  ' as a guide how to use it.')
    elif (filepath.lower().endswith('.h5') or
          filepath.lower().endswith('.hdf5')):
        raise NotImplementedError('HDF5 is not supported. See '
                                  'https://stackoverflow.com/a/41586571/562769'
                                  ' as a guide how to use it.')
    else:
        raise NotImplementedError('File \'{}\' is not known.'.format(filepath))


def _read_csv(filepath, kwargs):
    """See documentation of mpu.io.read."""
    if 'delimiter' not in kwargs:
        kwargs['delimiter'] = ','
    if 'quotechar' not in kwargs:
        kwargs['quotechar'] = '"'
    if 'skiprows' not in kwargs:
        kwargs['skiprows'] = []
    if isinstance(kwargs['skiprows'], int):
        kwargs['skiprows'] = [i for i in range(kwargs['skiprows'])]
    if 'format' in kwargs:
        format_ = kwargs['format']
        kwargs.pop('format', None)
    else:
        format_ = 'default'
    skiprows = kwargs['skiprows']
    kwargs.pop('skiprows', None)

    kwargs_open = {'newline': ''}
    mode = 'r'
    if sys.version_info < (3, 0):
        kwargs_open.pop('newline', None)
        mode = 'rb'
    with open(filepath, mode, **kwargs_open) as fp:
        if format_ == 'default':
            reader = csv.reader(fp, **kwargs)
            data = EList([row for row in reader])
            data = data.remove_indices(skiprows)
        elif format_ == 'dicts':
            reader_list = csv.DictReader(fp, **kwargs)
            data = [row for row in reader_list]
        else:
            raise NotImplementedError('Format \'{}\' unknown'
                                      .format(format_))
    return data


def _read_jsonl(filepath, kwargs):
    """See documentation of mpu.io.read."""
    with open(filepath) as data_file:
        data = [json.loads(line, **kwargs)
                for line in data_file
                if len(line) > 0]
    return data


def write(filepath, data, **kwargs):
    """
    Write a file.

    Supported formats:

    * CSV
    * JSON, JSONL
    * pickle

    Parameters
    ----------
    filepath : str
        Path to the file that should be read. This methods action depends
        mainly on the file extension.
    data : dict or list
        Content that should be written
    kwargs : dict
        Any keywords for the specific file format.

    Returns
    -------
    data : str or bytes
    """
    if filepath.lower().endswith('.csv'):
        return _write_csv(filepath, data, kwargs)
    elif filepath.lower().endswith('.json'):
        return _write_json(filepath, data, kwargs)
    elif filepath.lower().endswith('.jsonl'):
        return _write_jsonl(filepath, data, kwargs)
    elif filepath.lower().endswith('.pickle'):
        return _write_pickle(filepath, data, kwargs)
    elif (filepath.lower().endswith('.yml') or
          filepath.lower().endswith('.yaml')):
        raise NotImplementedError('YAML is not supported, because you need '
                                  'PyYAML in Python3. '
                                  'See '
                                  'https://stackoverflow.com/a/42054860/562769'
                                  ' as a guide how to use it.')
    elif (filepath.lower().endswith('.h5') or
          filepath.lower().endswith('.hdf5')):
        raise NotImplementedError('YAML is not supported. See '
                                  'https://stackoverflow.com/a/41586571/562769'
                                  ' as a guide how to use it.')
    else:
        raise NotImplementedError('File \'{}\' is not known.'.format(filepath))


def _write_csv(filepath, data, kwargs):
    """See documentation of mpu.io.write."""
    kwargs_open = {'newline': ''}
    mode = 'w'
    if sys.version_info < (3, 0):
        kwargs_open.pop('newline', None)
        mode = 'wb'
    with open(filepath, mode, **kwargs_open) as fp:
        if 'delimiter' not in kwargs:
            kwargs['delimiter'] = ','
        if 'quotechar' not in kwargs:
            kwargs['quotechar'] = '"'
        with open(filepath, 'w') as fp:
            writer = csv.writer(fp, **kwargs)
            writer.writerows(data)
    return data


def _write_json(filepath, data, kwargs):
    """See documentation of mpu.io.write."""
    with io_stl.open(filepath, 'w', encoding='utf8') as outfile:
        if 'indent' not in kwargs:
            kwargs['indent'] = 4
        if 'sort_keys' not in kwargs:
            kwargs['sort_keys'] = True
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ': ')
        if 'ensure_ascii' not in kwargs:
            kwargs['ensure_ascii'] = False
        str_ = json.dumps(data, **kwargs)
        outfile.write(to_unicode(str_))
    return data


def _write_jsonl(filepath, data, kwargs):
    """See documentation of mpu.io.write."""
    with io_stl.open(filepath, 'w', encoding='utf8') as outfile:
        kwargs['indent'] = None  # JSON has to be on one line!
        if 'sort_keys' not in kwargs:
            kwargs['sort_keys'] = True
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ': ')
        if 'ensure_ascii' not in kwargs:
            kwargs['ensure_ascii'] = False
        for line in data:
            str_ = json.dumps(line, **kwargs)
            outfile.write(to_unicode(str_))
            outfile.write(u'\n')
    return data


def _write_pickle(filepath, data, kwargs):
    """See documentation of mpu.io.write."""
    if 'protocol' not in kwargs:
        kwargs['protocol'] = pickle.HIGHEST_PROTOCOL
    with open(filepath, 'wb') as handle:
        pickle.dump(data, handle, **kwargs)
    return data


def urlread(url, encoding='utf8'):
    """
    Read the content of an URL.

    Parameters
    ----------
    url : str

    Returns
    -------
    content : str
    """
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen
    response = urlopen(url)
    content = response.read()
    content = content.decode(encoding)
    return content


def download(source, sink=None):
    """
    Download a file.

    Parameters
    ----------
    source : str
        Where the file comes from. Some URL.
    sink : str or None (default: same filename in current directory)
        Where the file gets stored. Some filepath in the local file system.
    """
    try:
        from urllib.request import urlretrieve  # Python 3
    except ImportError:
        from urllib import urlretrieve  # Python 2
    if sink is None:
        sink = os.path.abspath(os.path.split(source)[1])
    urlretrieve(source, sink)
    return sink


def hash(filepath, method='sha1', buffer_size=65536):
    """
    Calculate a hash of a local file.

    Parameters
    ----------
    filepath : str
    method : {'sha1', 'md5'}
    buffer_size : int, optional (default: 65536 byte = 64 KiB)
        in byte

    Returns
    -------
    hash : str
    """
    if method == 'sha1':
        hash_function = hashlib.sha1()
    elif method == 'md5':
        hash_function = hashlib.md5()
    else:
        raise NotImplementedError('Only md5 and sha1 hashes are known, but '
                                  ' \'{}\' was specified.'.format(method))

    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(buffer_size)
            if not data:
                break
            hash_function.update(data)
    return hash_function.hexdigest()


def get_creation_datetime(filepath):
    """
    Get the date that a file was created.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    creation_datetime : datetime.datetime or None
    """
    if platform.system() == 'Windows':
        return datetime.fromtimestamp(os.path.getctime(filepath))
    else:
        stat = os.stat(filepath)
        try:
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return None


def get_modification_datetime(filepath):
    """
    Get the datetime that a file was last modified.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    modification_datetime : datetime.datetime

    """
    import tzlocal
    timezone = tzlocal.get_localzone()
    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
    return mtime.replace(tzinfo=timezone)


def get_access_datetime(filepath):
    """
    Get the last time filepath was accessed.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    access_datetime : datetime.datetime
    """
    import tzlocal
    tz = tzlocal.get_localzone()
    mtime = datetime.fromtimestamp(os.path.getatime(filepath))
    return mtime.replace(tzinfo=tz)


def get_file_meta(filepath):
    """
    Get meta-information about a file.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    meta : dict
    """
    meta = {}
    meta['filepath'] = os.path.abspath(filepath)
    meta['creation_datetime'] = get_creation_datetime(filepath)
    meta['last_access_datetime'] = get_access_datetime(filepath)
    meta['modification_datetime'] = get_modification_datetime(filepath)
    try:
        import magic
        f_mime = magic.Magic(mime=True, uncompress=True)
        f_other = magic.Magic(mime=False, uncompress=True)
        meta['mime'] = f_mime.from_file(meta['filepath'])
        meta['magic-type'] = f_other.from_file(meta['filepath'])
    except ImportError:
        pass
    return meta


def gzip_file(source, sink):
    """
    Create a GZIP file from a source file.

    Parameters
    ----------
    source : str
        Filepath
    sink : str
        Filepath
    """
    import gzip
    with open(source, 'rb') as f_in, gzip.open(sink, 'wb') as f_out:
        f_out.writelines(f_in)

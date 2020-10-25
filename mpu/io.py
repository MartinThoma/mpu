"""Reading and writing common file formats."""

# Core Library
import csv
import hashlib
import json
import os
import pickle
import platform
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# First party
from mpu.datastructures import EList


def read(filepath: str, **kwargs: Any) -> Any:
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
    kwargs : Dict
        Any keywords for the specific file format. For CSV, this is
        'delimiter', 'quotechar', 'skiprows', 'format'

    Returns
    -------
    data : Union[str, bytes] or other (e.g. format=dicts)
    """
    supported_formats = [".csv", ".json", ".jsonl", ".pickle"]
    if filepath.lower().endswith(".csv"):
        return _read_csv(filepath, kwargs)
    elif filepath.lower().endswith(".json"):
        with open(filepath, encoding="utf8") as data_file:
            data: Any = json.load(data_file, **kwargs)
        return data
    elif filepath.lower().endswith(".jsonl"):
        return _read_jsonl(filepath, kwargs)
    elif filepath.lower().endswith(".pickle"):
        with open(filepath, "rb") as handle:
            data_pkl = pickle.load(handle)
        return data_pkl
    elif filepath.lower().endswith(".yml") or filepath.lower().endswith(".yaml"):
        raise NotImplementedError(
            "YAML is not supported, because you need "
            "PyYAML in Python3. "
            "See "
            "https://stackoverflow.com/a/42054860/562769"
            " as a guide how to use it."
        )
    elif filepath.lower().endswith(".h5") or filepath.lower().endswith(".hdf5"):
        raise NotImplementedError(
            "HDF5 is not supported. See "
            "https://stackoverflow.com/a/41586571/562769"
            " as a guide how to use it."
        )
    else:
        raise NotImplementedError(
            f"File '{filepath}' does not end with one "
            f"of the supported file name extensions. "
            f"Supported are: {supported_formats}"
        )


def _read_csv(filepath: str, kwargs: Dict) -> Union[List, Dict]:
    """See documentation of mpu.io.read."""
    if "delimiter" not in kwargs:
        kwargs["delimiter"] = ","
    if "quotechar" not in kwargs:
        kwargs["quotechar"] = '"'
    if "skiprows" not in kwargs:
        kwargs["skiprows"] = []
    if isinstance(kwargs["skiprows"], int):
        kwargs["skiprows"] = list(range(kwargs["skiprows"]))
    if "format" in kwargs:
        format_ = kwargs["format"]
        kwargs.pop("format", None)
    else:
        format_ = "default"
    skiprows = kwargs["skiprows"]
    kwargs.pop("skiprows", None)

    with open(filepath, encoding="utf8") as fp:
        if format_ == "default":
            reader = csv.reader(fp, **kwargs)
            data_tmp = EList(list(reader))
            data: Union[List, Dict] = data_tmp.remove_indices(skiprows)
        elif format_ == "dicts":
            reader_list = csv.DictReader(fp, **kwargs)
            data = list(reader_list)
        else:
            raise NotImplementedError(f"Format '{format_}' unknown")
    return data


def _read_jsonl(filepath: str, kwargs: Dict) -> List:
    """See documentation of mpu.io.read."""
    with open(filepath, encoding="utf8") as data_file:
        data = [json.loads(line, **kwargs) for line in data_file if len(line) > 0]
    return data


def write(filepath: str, data: Union[Dict, List], **kwargs: Dict) -> Any:
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
        mainly on the file extension. Make sure that it ends in .csv, .json,
        .jsonl, or .pickle.
    data : Union[Dict, List]
        Content that should be written
    kwargs : Dict
        Any keywords for the specific file format.

    Returns
    -------
    data : str or bytes
    """
    supported_formats = [".csv", ".json", ".jsonl", ".pickle"]
    if filepath.lower().endswith(".csv"):
        return _write_csv(filepath, data, kwargs)
    elif filepath.lower().endswith(".json"):
        return _write_json(filepath, data, kwargs)
    elif filepath.lower().endswith(".jsonl"):
        return _write_jsonl(filepath, data, kwargs)
    elif filepath.lower().endswith(".pickle"):
        return _write_pickle(filepath, data, kwargs)
    elif filepath.lower().endswith(".yml") or filepath.lower().endswith(".yaml"):
        raise NotImplementedError(
            "YAML is not supported, because you need "
            "PyYAML in Python3. "
            "See "
            "https://stackoverflow.com/a/42054860/562769"
            " as a guide how to use it."
        )
    elif filepath.lower().endswith(".h5") or filepath.lower().endswith(".hdf5"):
        raise NotImplementedError(
            "HDF5 is not supported. See "
            "https://stackoverflow.com/a/41586571/562769"
            " as a guide how to use it."
        )
    else:
        raise NotImplementedError(
            f"File '{filepath}' does not end in one of the "
            f"supported formats. Supported are: {supported_formats}"
        )


def _write_csv(filepath: str, data: Any, kwargs: Dict) -> Any:
    """See documentation of mpu.io.write."""
    with open(filepath, "w", encoding="utf8") as fp:
        if "delimiter" not in kwargs:
            kwargs["delimiter"] = ","
        if "quotechar" not in kwargs:
            kwargs["quotechar"] = '"'
        writer = csv.writer(fp, **kwargs)
        writer.writerows(data)
    return data


def _write_json(filepath: str, data: Any, kwargs: Dict) -> Any:
    """See documentation of mpu.io.write."""
    with open(filepath, "w", encoding="utf8") as outfile:
        if "indent" not in kwargs:
            kwargs["indent"] = 4
        if "sort_keys" not in kwargs:
            kwargs["sort_keys"] = True
        if "separators" not in kwargs:
            kwargs["separators"] = (",", ": ")
        if "ensure_ascii" not in kwargs:
            kwargs["ensure_ascii"] = False
        str_ = json.dumps(data, **kwargs)
        outfile.write(str_)
    return data


def _write_jsonl(filepath: str, data: Any, kwargs: Dict) -> Any:
    """See documentation of mpu.io.write."""
    with open(filepath, "w", encoding="utf8") as outfile:
        kwargs["indent"] = None  # JSON has to be on one line!
        if "sort_keys" not in kwargs:
            kwargs["sort_keys"] = True
        if "separators" not in kwargs:
            kwargs["separators"] = (",", ": ")
        if "ensure_ascii" not in kwargs:
            kwargs["ensure_ascii"] = False
        for line in data:
            str_ = json.dumps(line, **kwargs)
            outfile.write(str_)
            outfile.write("\n")
    return data


def _write_pickle(filepath: str, data: Any, kwargs: Dict) -> Any:
    """See documentation of mpu.io.write."""
    if "protocol" not in kwargs:
        kwargs["protocol"] = pickle.HIGHEST_PROTOCOL
    with open(filepath, "wb") as handle:
        pickle.dump(data, handle, **kwargs)
    return data


def urlread(url: str, encoding: str = "utf8") -> str:
    """
    Read the content of an URL.

    Parameters
    ----------
    url : str
    encoding : str (default: "utf8")

    Returns
    -------
    content : str
    """
    # Core Library
    from urllib.request import urlopen

    response = urlopen(url)
    content = response.read()
    content = content.decode(encoding)
    return content


def download(source: str, sink: Optional[str] = None) -> str:
    """
    Download a file.

    Parameters
    ----------
    source : str
        Where the file comes from. Some URL.
    sink : str, optional (default: same filename in current directory)
        Where the file gets stored. Some filepath in the local file system.
    """
    # Core Library
    from urllib.request import urlretrieve

    if sink is None:
        sink = os.path.abspath(os.path.split(source)[1])
    urlretrieve(source, sink)
    return sink


def hash(filepath: str, method: str = "sha1", buffer_size: int = 65536) -> str:
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
    if method == "sha1":
        hash_function = hashlib.sha1()
    elif method == "md5":
        hash_function = hashlib.md5()
    else:
        raise NotImplementedError(
            f"Only md5 and sha1 hashes are known, but '{method}' was specified."
        )

    with open(filepath, "rb") as fp:
        while True:
            data = fp.read(buffer_size)
            if not data:
                break
            hash_function.update(data)
    return hash_function.hexdigest()


def get_creation_datetime(filepath: str) -> Optional[datetime]:
    """
    Get the date that a file was created.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    creation_datetime : Optional[datetime]
    """
    if platform.system() == "Windows":
        return datetime.fromtimestamp(os.path.getctime(filepath))
    else:
        stat = os.stat(filepath)
        try:
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return None


def get_modification_datetime(filepath: str) -> datetime:
    """
    Get the datetime that a file was last modified.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    modification_datetime : datetime

    """
    # Third party
    import tzlocal

    timezone = tzlocal.get_localzone()
    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
    return mtime.replace(tzinfo=timezone)


def get_access_datetime(filepath: str) -> datetime:
    """
    Get the last time filepath was accessed.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    access_datetime : datetime
    """
    # Third party
    import tzlocal

    tz = tzlocal.get_localzone()
    mtime = datetime.fromtimestamp(os.path.getatime(filepath))
    return mtime.replace(tzinfo=tz)


def get_file_meta(filepath: str) -> Dict[str, Any]:
    """
    Get meta-information about a file.

    Parameters
    ----------
    filepath : str

    Returns
    -------
    meta : dict
    """
    meta: Dict[str, Any] = {
        "filepath": os.path.abspath(filepath),
        "creation_datetime": get_creation_datetime(filepath),
        "last_access_datetime": get_access_datetime(filepath),
        "modification_datetime": get_modification_datetime(filepath),
    }
    try:
        # Third party
        import magic

        f_mime = magic.Magic(mime=True, uncompress=True)
        f_other = magic.Magic(mime=False, uncompress=True)
        meta["mime"] = f_mime.from_file(meta["filepath"])
        meta["magic-type"] = f_other.from_file(meta["filepath"])
    except ImportError:
        pass
    return meta


def gzip_file(source: str, sink: str) -> None:
    """
    Create a GZIP file from a source file.

    Parameters
    ----------
    source : str
        Filepath
    sink : str
        Filepath
    """
    # Core Library
    import gzip

    with open(source, "rb") as f_in, gzip.open(sink, "wb") as f_out:
        f_out.writelines(f_in)

#!/usr/bin/env python

"""Convenience functions for AWS interactions."""

# Core Library
import enum
import os
from collections import namedtuple
from tempfile import mkstemp

# Third party
import boto3


def list_files(bucket, prefix="", profile_name=None):
    """
    List up to 1000 files in a bucket.

    Parameters
    ----------
    bucket : str
    profile_name : str, optional
        AWS profile

    Returns
    -------
    s3_paths : List[str]
    """
    session = boto3.Session(profile_name=profile_name)
    conn = session.client("s3")
    keys = []
    ret = conn.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if "Contents" not in ret:
        return []
    # Make this a generator in future and use the marker:
    # https://boto3.readthedocs.io/en/latest/reference/services/
    #     s3.html#S3.Client.list_objects
    for key in conn.list_objects_v2(Bucket=bucket, Prefix=prefix)["Contents"]:
        keys.append("s3://" + bucket + "/" + key["Key"])
    return keys


def s3_read(source, profile_name=None):
    """
    Read a file from an S3 source.

    Parameters
    ----------
    source : str
        Path starting with s3://, e.g. 's3://bucket-name/key/foo.bar'
    profile_name : str, optional
        AWS profile

    Returns
    -------
    content : bytes

    Raises
    ------
    botocore.exceptions.NoCredentialsError
        Botocore is not able to find your credentials. Either specify
        profile_name or add the environment variables AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN.
        See https://boto3.readthedocs.io/en/latest/guide/configuration.html
    """
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client("s3")
    bucket_name, key = _s3_path_split(source)
    s3_object = s3.get_object(Bucket=bucket_name, Key=key)
    body = s3_object["Body"]
    return body.read()


class ExistsStrategy(enum.Enum):
    """Strategies what to do when a file already exists."""

    RAISE = "raise"
    REPLACE = "replace"
    ABORT = "abort"


def s3_download(
    source, destination=None, exists_strategy=ExistsStrategy.RAISE, profile_name=None
):
    """
    Copy a file from an S3 source to a local destination.

    Parameters
    ----------
    source : str
        Path starting with s3://, e.g. 's3://bucket-name/key/foo.bar'
    destination : str, optional
        If none is given, a temporary file is created
    exists_strategy : {'raise', 'replace', 'abort'}
        What is done when the destination already exists?
        * `ExistsStrategy.RAISE` means a RuntimeError is raised,
        * `ExistsStrategy.REPLACE` means the local file is replaced,
        * `ExistsStrategy.ABORT` means the download is not done.
    profile_name : str, optional
        AWS profile

    Returns
    -------
    download_path : str
        Path of the downloaded file.

    Raises
    ------
    botocore.exceptions.NoCredentialsError
        Botocore is not able to find your credentials. Either specify
        profile_name or add the environment variables AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY and AWS_SESSION_TOKEN.
        See https://boto3.readthedocs.io/en/latest/guide/configuration.html
    """
    if not isinstance(exists_strategy, ExistsStrategy):
        raise ValueError(
            "exists_strategy '{}' is not in {}".format(exists_strategy, ExistsStrategy)
        )
    session = boto3.Session(profile_name=profile_name)
    s3 = session.resource("s3")
    bucket_name, key = _s3_path_split(source)
    if destination is None:
        _, filename = os.path.split(source)
        prefix, suffix = os.path.splitext(filename)
        _, destination = mkstemp(prefix=prefix, suffix=suffix)
    elif os.path.isfile(destination):
        if exists_strategy is ExistsStrategy.RAISE:
            raise RuntimeError("File '{}' already exists.".format(destination))
        elif exists_strategy is ExistsStrategy.ABORT:
            return
    s3.Bucket(bucket_name).download_file(key, destination)
    return destination


def s3_upload(source, destination, profile_name=None):
    """
    Copy a file from a local source to an S3 destination.

    Parameters
    ----------
    source : str
    destination : str
        Path starting with s3://, e.g. 's3://bucket-name/key/foo.bar'
    profile_name : str, optional
        AWS profile
    """
    session = boto3.Session(profile_name=profile_name)
    s3 = session.resource("s3")
    bucket_name, key = _s3_path_split(destination)
    with open(source, "rb") as data:
        s3.Bucket(bucket_name).put_object(Key=key, Body=data)


S3Path = namedtuple("S3Path", ["bucket_name", "key"])


def _s3_path_split(s3_path):
    """
    Split an S3 path into bucket and key.

    Parameters
    ----------
    s3_path : str

    Returns
    -------
    splitted : (str, str)
        (bucket, key)

    Examples
    --------
    >>> _s3_path_split('s3://my-bucket/foo/bar.jpg')
    S3Path(bucket_name='my-bucket', key='foo/bar.jpg')
    """
    if not s3_path.startswith("s3://"):
        raise ValueError(
            "s3_path is expected to start with 's3://', " "but was {}".format(s3_path)
        )
    bucket_key = s3_path[len("s3://") :]
    bucket_name, key = bucket_key.split("/", 1)
    return S3Path(bucket_name, key)

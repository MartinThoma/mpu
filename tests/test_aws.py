#!/usr/bin/env python

"""Test mpu.aws module."""

# Core Library
import filecmp
import os
from tempfile import mkstemp

# Third party
import boto3
import pkg_resources
import pytest
from moto import mock_s3

# First party
# internal modules
import mpu.aws


@pytest.mark.xfail
@mock_s3
def test_list_no_files():
    """Test if listing files of an S3 bucket works."""
    # We need to create the bucket since this is all in Moto's 'virtual'
    # AWS account
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="mybucket")
    assert mpu.aws.list_files("mybucket") == []

    # Test upload
    path = "files/example.csv"
    local_path = pkg_resources.resource_filename(__name__, path)
    mpu.aws.s3_upload(local_path, "s3://mybucket/example_test.csv")
    assert mpu.aws.list_files("mybucket") == ["s3://mybucket/example_test.csv"]

    # Test download
    _, destination = mkstemp(suffix="example.csv")
    os.remove(destination)  # make sure this file does NOT exist
    mpu.aws.s3_download("s3://mybucket/example_test.csv", destination)
    assert filecmp.cmp(destination, local_path)
    os.remove(destination)  # cleanup of mkstemp

    # Test download without destination
    destination = mpu.aws.s3_download("s3://mybucket/example_test.csv")
    os.remove(destination)

    # Test download: File exists
    _, destination = mkstemp(suffix="example.csv")
    with pytest.raises(RuntimeError):
        mpu.aws.s3_download(
            "s3://mybucket/example_test.csv",
            destination,
            exists_strategy=mpu.aws.ExistsStrategy.RAISE,
        )
    with pytest.raises(ValueError):
        mpu.aws.s3_download(
            "s3://mybucket/example_test.csv",
            destination,
            exists_strategy="raises",
        )
    mpu.aws.s3_download(
        "s3://mybucket/example_test.csv",
        destination,
        exists_strategy=mpu.aws.ExistsStrategy.ABORT,
    )
    mpu.aws.s3_download(
        "s3://mybucket/example_test.csv",
        destination,
        exists_strategy=mpu.aws.ExistsStrategy.REPLACE,
    )

    mpu.aws.s3_read("s3://mybucket/example_test.csv")
    os.remove(destination)  # cleanup of mkstemp


def test_s3_path_split():
    with pytest.raises(ValueError):
        mpu.aws._s3_path_split("foo/bar")

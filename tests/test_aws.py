#!/usr/bin/env python
# -*- coding: utf-8 -*-

# core modules
from tempfile import mkstemp
import filecmp
import os
import pkg_resources
import unittest

# 3rd party modules
from moto import mock_s3
import boto3

# internal modules
import mpu.aws


class AWSTest(unittest.TestCase):

    @mock_s3
    def test_list_no_files(self):
        # We need to create the bucket since this is all in Moto's 'virtual'
        # AWS account
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='mybucket')
        self.assertEqual(mpu.aws.list_files('mybucket'), [])

        # Test upload
        path = '../tests/files/example.csv'
        local_path = pkg_resources.resource_filename('mpu', path)
        mpu.aws.s3_upload(local_path, 's3://mybucket/example_test.csv')
        self.assertEqual(mpu.aws.list_files('mybucket'),
                         ['s3://mybucket/example_test.csv'])

        # Test download
        _, destination = mkstemp(suffix='example.csv')
        os.remove(destination)  # make sure this file does NOT exist
        mpu.aws.s3_download('s3://mybucket/example_test.csv', destination)
        self.assertTrue(filecmp.cmp(destination, local_path))
        os.remove(destination)  # cleanup of mkstemp

        # Test download: File exists
        _, destination = mkstemp(suffix='example.csv')
        with self.assertRaises(RuntimeError):
            mpu.aws.s3_download('s3://mybucket/example_test.csv',
                                destination,
                                exists_strategy=mpu.aws.ExistsStrategy.RAISE)
        with self.assertRaises(ValueError):
            mpu.aws.s3_download('s3://mybucket/example_test.csv',
                                destination,
                                exists_strategy='raises')
        mpu.aws.s3_download('s3://mybucket/example_test.csv',
                            destination,
                            exists_strategy=mpu.aws.ExistsStrategy.ABORT)
        mpu.aws.s3_download('s3://mybucket/example_test.csv',
                            destination,
                            exists_strategy=mpu.aws.ExistsStrategy.REPLACE)

        mpu.aws.s3_read('s3://mybucket/example_test.csv')
        os.remove(destination)  # cleanup of mkstemp

    def test_s3_path_split(self):
        with self.assertRaises(ValueError):
            mpu.aws._s3_path_split('foo/bar')

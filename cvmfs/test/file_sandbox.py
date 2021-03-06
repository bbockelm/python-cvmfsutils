#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by René Meusel
This file is part of the CernVM File System auxiliary tools.
"""

import shutil
import os
import tempfile

class FileSandbox:
    """ Wraps the creation and automatic removal of temporary files """

    def __init__(self, file_prefix):
        self.file_prefix   = file_prefix
        self.temporary_dir = tempfile.mkdtemp(prefix=file_prefix)

    def __del__(self):
        shutil.rmtree(self.temporary_dir)


    def write_to_temporary(self, string_buffer):
        """ stores the provided content into a /tmp path that is returned """
        filename = None
        with tempfile.NamedTemporaryFile(mode='w+b',
                                         prefix=self.file_prefix,
                                         dir=self.temporary_dir,
                                         delete=False) as f:
            filename = f.name
            f.write(string_buffer)
        return filename


    def create_directory(self, directory_name):
        """ creates a directory under self.temporary_dir with the given name """
        os.mkdir(os.path.join(self.temporary_dir, directory_name))


    def write_to_file(self, file_path, string_buffer):
        """ creates the file_path and writes the data given in string_buffer """
        full_file_path = os.path.join(self.temporary_dir, file_path)
        if os.path.isfile(full_file_path):
            os.unlink(full_file_path)
        with open(full_file_path, "w+") as f:
            f.write(string_buffer)

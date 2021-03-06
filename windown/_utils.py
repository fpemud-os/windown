#!/usr/bin/env python3

# Copyright (c) 2005-2014 Fpemud <fpemud@sina.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import shutil


def force_rm(path):
    if os.path.islink(path):
        os.remove(path)
    elif os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.lexists(path):
        os.remove(path)             # other type of file, such as device node
    else:
        pass                        # path does not exist, do nothing


def force_mkdir(path):
    if os.path.islink(path):
        os.remove(path)
        os.mkdir(path)
    elif os.path.isfile(path):
        os.remove(path)
        os.mkdir(path)
    elif os.path.isdir(path):
        pass                        # already exists
    elif os.path.lexists(path):
        os.remove(path)             # other type of file, such as device node
        os.mkdir(path)
    else:
        os.mkdir(path)              # path does not exist


def force_symlink(target, link_path):
    if os.path.islink(link_path) and os.readlink(link_path) == target:      # already exist
        return
    force_rm(link_path)                   # os.symlink won't overwrite anything, so we delete it first
    os.symlink(target, link_path)

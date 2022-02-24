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


class ConfigBase:

    @property
    def download_command(self):
        raise NotImplementedError()

    @property
    def resume_download_command(self):
        raise NotImplementedError()


class Param:

    def __init__(self):
        self.use_tmp_or_cache_dir = None
        self.cache_dir = None

    def check(self):
        pass


class WindowsDownloaderParam(Param):

    class WindowsIdentifier:

        def __init__(self):
            self.arch = None
            self.version = None
            self.edition = None
            self.lang = None

    def __init__(self):
        super().__init__()
        self.use_full_path = None
        self.download_items = None

    def check(self):
        super().check()
        pass

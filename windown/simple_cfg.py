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

from ._config import ConfigBase


class Config(ConfigBase):

    def __init__(self):
        super().__init__()

        self._quiet = False
        self._downCmd = r'wget -t 3 -T 60 --passive-ftp -O \"${FILE}\" \"${URI}\"'
        self._resumeCmd = r'wget -c -t 3 -T 60 --passive-ftp -O \"${FILE}\" \"${URI}\"'
        self._downQuietCmd = r'wget -q -t 3 -T 60 --passive-ftp -O \"${FILE}\" \"${URI}\"'
        self._resumeQuietCmd = r'wget -q -c -t 3 -T 60 --passive-ftp -O \"${FILE}\" \"${URI}\"'
        self._checksumMasTries = 5

        self.check()

    @property
    def quiet(self):
        return self._quiet

    @property
    def fetch_command(self):
        return self._downCmd

    @property
    def resume_command(self):
        return self._resumeCmd

    @property
    def fetch_command_quiet(self):
        return self._downQuietCmd

    @property
    def resume_command_quiet(self):
        return self._resumeQuietCmd

    @property
    def checksum_failure_max_tries(self):
        return self._checksumMasTries

    @quiet.setter
    def quiet(self, value):
        self._quiet = value
        self.check()

    @fetch_command.setter
    def fetch_command(self, value):
        self._downCmd = value
        self.check()

    @resume_command.setter
    def resume_command(self, value):
        self._resumeCmd = value
        self.check()

    @fetch_command_quiet.setter
    def fetch_command_quiet(self, value):
        self._downQuietCmd = value
        self.check()

    @resume_command_quiet.setter
    def resume_command_quiet(self, value):
        self._resumeQuietCmd = value
        self.check()

    @checksum_failure_max_tries.setter
    def checksum_failure_max_tries(self, value):
        self._checksumMasTries = value
        self.check()

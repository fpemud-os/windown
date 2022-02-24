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
import re
from ._config import ConfigBase
from ._errors import ConfigError


class Config(ConfigBase):

    DEFAULT_CONFIG_DIR = "/etc/windown"

    def __init__(self, cfgdir=DEFAULT_CONFIG_DIR):
        super().__init__()

        self._mainConf = os.path.join(cfgdir, "windown.conf")

        defaultValue = "wget -t 3 -T 60 --passive-ftp -O \"\${FILE}\" \"\${URI}\""
        self._downCmd = self._getConfVar("FETCHCOMMAND", str, defaultValue)

        defaultValue = "wget -c -t 3 -T 60 --passive-ftp -O \"\${FILE}\" \"\${URI}\""
        self._resumeCmd = self._getConfVar("RESUMECOMMAND", str, defaultValue)

        defaultValue = 350 * 1024   # 350K
        self._fetchResumeMinSize = self._getConfVar("FETCH_RESUME_MIN_SIZE", int, defaultValue)

        defaultValue = 5
        self._checksumMasTries = self._getConfVar("CHECKSUM_FAILURE_MAX_TRIES", int, defaultValue)

        self.check()

    @property
    def fetch_command(self):
        return self._downCmd

    @property
    def resume_command(self):
        return self._resumeCmd

    @property
    def fetch_resume_min_size(self):
        return self._fetchResumeMinSize

    @property
    def checksum_failure_max_tries(self):
        return self._checksumMasTries

    def _getConfVar(self, varName, varClass, defaultValue=None):
        """Returns variable value, returns "" when not found
           Multiline variable definition is not supported yet"""

        assert varClass in [str, int]
        if defaultValue is not None:
            assert isinstance(defaultValue, varClass)

        buf = ""
        with open(self._mainConf, 'r') as f:
            buf = f.read()

        m = re.search("^%s=\"(.*)\"$" % (varName), buf, re.MULTILINE)
        if m is None:
            return defaultValue
        varVal = m.group(1)

        while True:
            m = re.search("\\${(\\S+)?}", varVal)
            if m is None:
                break
            varName2 = m.group(1)

            varVal2 = self._getConfVar(self._mainConf, varName2)
            if varVal2 is None:
                varVal2 = ""

            varVal = varVal.replace(m.group(0), str(varVal2))

        if varClass == str:
            return varVal
        elif varClass == int:
            try:
                return int(varVal)
            except ValueError:
                raise ConfigError("invalid type of variable %s" % (varName))
        else:
            assert False

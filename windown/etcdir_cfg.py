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
import pathlib
from ._config import ConfigBase
from ._errors import ConfigError


class Config(ConfigBase):

    DEFAULT_CONFIG_DIR = "/etc/windown"

    def __init__(self, cfgdir=DEFAULT_CONFIG_DIR):
        super().__init__()

        self._mainConf = os.path.join(cfgdir, "windown.conf")

        defaultValue = False
        self._quiet = self._getConfVar("QUIET", bool, defaultValue)

        defaultValue = r'wget -t 3 -T 60 --passive-ftp -O \"\${FILE}\" \"\${URI}\"'
        self._downCmd = self._getConfVar("FETCH_COMMAND", str, defaultValue)

        defaultValue = r'wget -c -t 3 -T 60 --passive-ftp -O \"\${FILE}\" \"\${URI}\"'
        self._resumeCmd = self._getConfVar("RESUME_COMMAND", str, defaultValue)

        defaultValue = r'wget -q -t 3 -T 60 --passive-ftp -O \"\${FILE}\" \"\${URI}\"'
        self._downQuietCmd = self._getConfVar("FETCH_COMMAND_QUIET", str, defaultValue)

        defaultValue = r'wget -q -c -t 3 -T 60 --passive-ftp -O \"\${FILE}\" \"\${URI}\"'
        self._resumeQuietCmd = self._getConfVar("RESUME_COMMAND_QUIET", str, defaultValue)

        defaultValue = 5
        self._checksumMasTries = self._getConfVar("CHECKSUM_FAILURE_MAX_TRIES", int, defaultValue)

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

    def _getConfVar(self, varName, varClass, defaultValue):
        """Returns variable value, returns "" when not found
           Multiline variable definition is not supported yet"""

        assert varClass in [str, int, bool]
        if defaultValue is not None:
            assert isinstance(defaultValue, varClass)

        if os.path.exists(self._mainConf):
            buf = pathlib.Path(self._mainConf).read_text()
        else:
            buf = ""

        m = re.search(r'^%s="(.*)"$' % (varName), buf, re.MULTILINE)
        if m is None:
            return defaultValue
        varVal = m.group(1)

        # while True:
        #     m = re.search(r'${(\S+)?}', varVal)
        #     if m is None:
        #         break
        #     varName2 = m.group(1)
        # 
        #     varVal2 = self._getConfVar(self._mainConf, varName2)
        #     if varVal2 is None:
        #         varVal2 = ""
        # 
        #     varVal = varVal.replace(m.group(0), str(varVal2))

        if varClass == str:
            return varVal
        elif varClass == int:
            try:
                return int(varVal)
            except ValueError:
                raise ConfigError("invalid type of variable %s" % (varName))
        elif varClass == bool:
            if varVal == "true":
                return True
            elif varVal == "false":
                return False
            else:
                raise ConfigError("invalid type of variable %s" % (varName))
        else:
            assert False

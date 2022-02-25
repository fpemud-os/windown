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

import abc
from ._errors import ConfigError


class ConfigBase(abc.ABC):

    @abc.abstractmethod
    @property
    def quiet(self):
        pass

    @abc.abstractmethod
    @property
    def fetch_command(self):
        pass

    @abc.abstractmethod
    @property
    def resume_command(self):
        pass

    @abc.abstractmethod
    @property
    def fetch_command_quiet(self):
        pass

    @abc.abstractmethod
    @property
    def resume_command_quiet(self):
        pass

    @abc.abstractmethod
    @property
    def fetch_resume_min_size(self):
        pass

    @abc.abstractmethod
    @property
    def checksum_failure_max_tries(self):
        pass

    def check(self):
        if "\${FILE}" not in self.fetch_command:
            raise ConfigError("")
        if "\${URI}" not in self.fetch_command:
            raise ConfigError("")

        if "\${FILE}" not in self.fetch_command_quiet:
            raise ConfigError("")
        if "\${URI}" not in self.fetch_command_quiet:
            raise ConfigError("")

        if "\${FILE}" not in self.resume_command:
            raise ConfigError("")
        if "\${URI}" not in self.resume_command:
            raise ConfigError("")

        if "\${FILE}" not in self.resume_command_quiet:
            raise ConfigError("")
        if "\${URI}" not in self.resume_command_quiet:
            raise ConfigError("")

        if not isinstance(self.checksum_failure_max_tries, int):
            raise ConfigError("")
        if self.checksum_failure_max_tries < 1:
            raise ConfigError("")

        if not isinstance(self.fetch_resume_min_size, int):
            raise ConfigError("")
        if self.fetch_resume_min_size < 1:
            raise ConfigError("")

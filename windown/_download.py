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
import subprocess


def do_fetch(cfg, filepath, myuris, digest=None, force=False):
    """
    Fetch files to dstdir and also verify digest if they are available.

    @param cfg: config instance.
    @type cfg: ConfigBase
    @param filepath: locale file path.
    @type filepath: str
    @param myuris: List of available fetch URIs.
    @type myuris: list
    @param digest: digest types and values of the fetched file.
    @type digests: str
    @param force: Force download, even when a file already exists. This is
        most useful when there are no digests available, since otherwise
        download will be automatically forced if the existing file does not
        match the available digests. Also, this avoids the need to remove the
        existing file in advance, which makes it possible to atomically replace
        interference with concurrent processes.
    @type force: bool
    """

    assert len(myuris) >= 1
    assert not (force and digest)   # since the force parameter can trigger unnecessary fetch when the digests match, do not allow force=True when digests are provided

    if force:
        fetchCmd = cfg.fetch_command
    elif os.path.exists(filepath) and os.path.getsize(filepath) > cfg.fetch_resume_min_size:
        print(">>> Resuming download...")
        fetchCmd = cfg.resume_command
    else:
        fetchCmd = cfg.fetch_command

    fetchCmd = fetchCmd.replace("${FILE}", filepath)
    fetchCmd = fetchCmd.replace("${URI}", myuris[0])

    subprocess.check_call(fetchCmd, shell=True, universal_newlines=True)


# Generally, downloading the same file repeatedly is a waste of bandwidth and time, so there needs to be a cap.
# checksum_failure_max_tries = cfg.checksum_failure_max_tries

# check space

# check degist

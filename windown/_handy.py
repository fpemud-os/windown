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
import hashlib
import subprocess
from ._utils import force_rm


def do_fetch(cfg, filepath, myuris, digest=None, digest_algorithm=None, force=False):
    """
    Fetch files to dstdir and also verify digest if they are available.

    @param cfg: config instance.
    @type cfg: ConfigBase
    @param filepath: locale file path.
    @type filepath: str
    @param myuris: List of available fetch URIs.
    @type myuris: list
    @param digest: digest values of the fetched file.
    @type digest: str
    @param digest_algorithm: digest algorithm of the digest.
    @type digest_algorithm: str
    @param force: Force download, even when a file already exists. This is
        most useful when there are no digests available, since otherwise
        download will be automatically forced if the existing file does not
        match the available digests. Also, this avoids the need to remove the
        existing file in advance, which makes it possible to atomically replace
        interference with concurrent processes.
    @type force: bool
    """

    assert len(myuris) >= 1
    assert not (digest and force)                   # since the force parameter can trigger unnecessary fetch when the digests match, do not allow force=True when digests are provided
    assert (digest and digest_algorithm) or (not digest and not digest_algorithm)

    if digest is None:
        digest = ""
    tempPath = filepath + ".__download__"
    vfailPath = filepath + ".verify_failed"

    checksum_failure_tries = 0
    fetch = 0                   # 0: unknown, 1: fetch; 2: resume, 3: finished, 4: re-fetch
    while True:
        # determine fetch or resume
        if force:
            fetch = 1
        elif os.path.exists(filepath):
            if digest != "":
                if _verify(filepath, digest, digest_algorithm):
                    fetch = 3
                else:
                    fetch = 4
            else:
                fetch = 3
        elif os.path.exists(tempPath):
            fetch = 2
        else:
            fetch = 1

        # print message
        if fetch == 1:
            pass
        elif fetch == 2:
            if not cfg.quiet:
                print(">>> Resuming fetching...")
        elif fetch == 3:
            if not cfg.quiet:
                print(">>> Already fetched...")
        elif fetch == 4:
            if not cfg.quiet:
                print(">>> Verify failed! Refetching...")
            os.rename(filepath, vfailPath)
            force_rm(filepath)
            force_rm(tempPath)
        else:
            assert False

        # run command
        if fetch == 1:
            cmd = cfg.fetch_command if not cfg.quiet else cfg.fetch_command_quiet
        elif fetch == 2:
            cmd = cfg.resume_command if not cfg.quiet else cfg.resume_command_quiet
        else:
            assert False
        cmd = cmd.replace(r'\"', r'"')                  # FIXME
        cmd = cmd.replace(r"${FILE}", tempPath)
        cmd = cmd.replace(r"${URI}", myuris[0])
        subprocess.check_call(cmd, shell=True, universal_newlines=True)

        # verify digest
        if digest != "":
            if not _verify(tempPath, digest, digest_algorithm):
                os.rename(tempPath, vfailPath)
                if checksum_failure_tries < cfg.checksum_failure_max_tries:
                    if not cfg.quiet:
                        print(">>> Verify failed! Refetching...")
                    checksum_failure_tries += 1
                    continue
                else:
                    print(">>> Verify failed!")
                    return

        # finished, we must jump out of the loop
        os.rename(tempPath, filepath)
        return


def _verify(filepath, digest, digest_algorithm):
    if digest_algorithm == "sha256":
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b''):
                h.update(byte_block)
        return h.hexdigest() == digest

    assert False


# Generally, downloading the same file repeatedly is a waste of bandwidth and time, so there needs to be a cap.
# checksum_failure_max_tries = cfg.checksum_failure_max_tries

# check space

# check degist

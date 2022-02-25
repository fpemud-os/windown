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


def do_fetch(cfg, filepath, myuris, digest=None, digest_algorithm=None, digest_filepath=None, force=False):
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
    @param digest_filepath: digest filepath.
    @type digest_filepath: str
    @param force: Force download, even when a file already exists. This is
        most useful when there are no digests available, since otherwise
        download will be automatically forced if the existing file does not
        match the available digests. Also, this avoids the need to remove the
        existing file in advance, which makes it possible to atomically replace
        interference with concurrent processes.
    @type force: bool
    """

    assert len(myuris) >= 1
    assert not (force and digest)                   # since the force parameter can trigger unnecessary fetch when the digests match, do not allow force=True when digests are provided
    assert (digest and digest_algorithm) or (not digest and not digest_algorithm)
    assert not (not digest and digest_filepath)

    checksum_failure_tries = 0
    bFetch = None
    while True:
        # determine fetch or resume
        if force:
            bFetch = True
        elif os.path.exists(filepath):
            if digest and _verify(filepath, digest, digest_algorithm):
                if not cfg.quiet:
                    print(">>> Already fetched...")
                return
            else:
                if not cfg.quiet:
                    print(">>> Resuming fetching...")
                bFetch = False
        else:
            bFetch = True

        # exec command
        if bFetch:
            cmd = cfg.fetch_command if not cfg.quiet else cfg.fetch_command_quiet
        else:
            cmd = cfg.resume_command if not cfg.quiet else cfg.resume_command_quiet
        cmd = cmd.replace("${FILE}", filepath)
        cmd = cmd.replace("${URI}", myuris[0])
        subprocess.check_call(cmd, shell=True, universal_newlines=True)

        # verify digest
        if digest and not _verify(filepath, digest, digest_algorithm):
            os.rename(filepath, filepath + ".verify_failed")
            if checksum_failure_tries < self._cfg.checksum_failure_max_tries:
                if not cfg.quiet:
                    print(">>> Verify failed! Refetching...")
                checksum_failure_tries += 1
                continue
            else:
                print(">>> Verify failed!")
                return

        # record digest
        if digest:
            if not digest_filepath:
                digest_filepath = filepath + ".digest"
            with open(digest_filepath, "w") as f:
                f.write(digest)

        # finished, we must jump out of the loop
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

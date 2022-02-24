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

'''
Various utilities.
'''

import os
import shutil
from ._errors import DownloadError


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
    force_rm(path)
    os.mkdir(path)


def fetch(cfg, filepath, myuris, digest=None, force=False):
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

    if force and digest:
        # Since the force parameter can trigger unnecessary fetch when the
        # digests match, do not allow force=True when digests are provided.
        raise DownloadError('fetch: force=True is not allowed when digests are provided')

    if len(myuris) == 0:
        raise DownloadError('fetch: not any uri specified')

    # Generally, downloading the same file repeatedly is a waste of bandwidth
    # and time, so there needs to be a cap.
    checksum_failure_max_tries = 5
    v = checksum_failure_max_tries
    try:
        v = int(mysettings.get("PORTAGE_FETCH_CHECKSUM_TRY_MIRRORS",
            checksum_failure_max_tries))
    except (ValueError, OverflowError):
        writemsg(_("!!! Variable PORTAGE_FETCH_CHECKSUM_TRY_MIRRORS"
            " contains non-integer value: '%s'\n") % \
            mysettings["PORTAGE_FETCH_CHECKSUM_TRY_MIRRORS"], noiselevel=-1)
        writemsg(_("!!! Using PORTAGE_FETCH_CHECKSUM_TRY_MIRRORS "
            "default value: %s\n") % checksum_failure_max_tries,
            noiselevel=-1)
        v = checksum_failure_max_tries
    if v < 1:
        writemsg(_("!!! Variable PORTAGE_FETCH_CHECKSUM_TRY_MIRRORS"
            " contains value less than 1: '%s'\n") % v, noiselevel=-1)
        writemsg(_("!!! Using PORTAGE_FETCH_CHECKSUM_TRY_MIRRORS "
            "default value: %s\n") % checksum_failure_max_tries,
            noiselevel=-1)
        v = checksum_failure_max_tries
    checksum_failure_max_tries = v
    del v



                if "${FILE}" not in resumecommand:
                    writemsg_level(
                        _("!!! %s does not contain the required ${FILE}"
                        " parameter.\n") % resumecommand_var,
                        level=logging.ERROR, noiselevel=-1)
                    missing_file_param = True

                if missing_file_param:
                    writemsg_level(
                        _("!!! Refer to the make.conf(5) man page for "
                        "information about how to\n!!! correctly specify "
                        "FETCHCOMMAND and RESUMECOMMAND.\n"),
                        level=logging.ERROR, noiselevel=-1)
                    if myfile != os.path.basename(loc):
                        return 0


    subprocess.check_call(cfg.download_command, )

    @staticmethod
    def wgetDownload(url, localFile=None):
        if localFile is None:
            FmUtil.cmdExec("wget", "-q", "--show-progress", *robust_layer.wget.additional_param(), url)
        else:
            FmUtil.cmdExec("wget", "-q", "--show-progress", *robust_layer.wget.additional_param(), "-O", localFile, url)


    pass


def wget_resume():
    pass

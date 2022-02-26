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
import time
import selenium
from ._utils import force_mkdir, force_symlink
from ._config import ConfigBase
from ._errors import ArgumentError
from ._handy import do_fetch


class WindowsDownloader:

    @staticmethod
    def get_product_id_list():
        ret = []

        # windows 98
        if True:
            ret += [
                "windows-98-se.x86.en-US",                  # language: English
                "windows-98-se.x86.es",                     # language: Spanish
                "windows-98-se.x86.it",                     # language: Italian
                "windows-98-se.x86.ja",                     # language: Japanese
                "windows-98-se.x86.ko",                     # language: Korean
                "windows-98-se.x86.pt-PT",                  # language: Portuguese
                "windows-98-se.x86.ru",                     # language: Russian
                "windows-98-se.x86.sl",                     # language: Slovenian
                "windows-98-se.x86.tr",                     # language: Turkish
            ]
            ret += [
                "windows-98-se-oem.x86.cz",                 # language: Czech
                "windows-98-se-oem.x86.en-US",              # language: English
                "windows-98-se-oem.x86.de",                 # language: German
                "windows-98-se-oem.x86.fi",                 # language: Finnish
                "windows-98-se-oem.x86.hu",                 # language: Hungarian
                "windows-98-se-oem.x86.nb",                 # language: Norwegian
                "windows-98-se-oem.x86.nl",                 # language: Dutch
                "windows-98-se-oem.x86.pl",                 # language: Polish
                "windows-98-se-oem.x86.pt-BR",              # language: Brazilian Portuguese
                "windows-98-se-oem.x86.sv",                 # language: Swedish
                "windows-98-se-oem.x86.zh-TW",              # language: Chinese Traditional
            ]

        # windows xp
        if True:
            t = [
                "windows-xp-home.x86.en-US",
                "windows-xp-professional.x86.en-US",
            ]
            ret += t
            ret += [x.replace("x86", "x86_64") for x in t]

        # windows 7
        if True:
            t = [
                "windows-7-starter.x86.en-US",
                "windows-7-home-basic.x86.en-US",
                "windows-7-home-premium.x86.en-US",
                "windows-7-professional.x86.en-US",
                "windows-7-ultimate.x86.en-US",
                "windows-7-enterprise.x86.en-US",
            ]
            ret += t
            ret += [x.replace("x86", "x86_64") for x in t]

        # windows 10
        if True:
            # from https://www.microsoft.com/en-US/software-download/windows10ISO
            t = [
                "windows-10.x86.ar",                        # language: Arabic
                "windows-10.x86.pt-BR",                     # language: Brazilian Portuguese
                "windows-10.x86.br",                        # language: Bulgarian
                "windows-10.x86.zh-CN",                     # language: Chinese Simplified
                "windows-10.x86.zh-TW",                     # language: Chinese Traditional
                "windows-10.x86.hr",                        # language: Croatian
                "windows-10.x86.cz",                        # language: Czech
                "windows-10.x86.da",                        # language: Danish
                "windows-10.x86.nl",                        # language: Dutch
                "windows-10.x86.en-US",                     # language: English
                "windows-10.x86.en",                        # language: English International
                "windows-10.x86.et",                        # language: Estonian
                "windows-10.x86.fi",                        # language: Finnish
                "windows-10.x86.fr-CA",                     # language: French Canadian
                "windows-10.x86.de",                        # language: German
                "windows-10.x86.el",                        # language: Greek
                "windows-10.x86.he",                        # language: Hebrew
                "windows-10.x86.hu",                        # language: Hungarian
                "windows-10.x86.it",                        # language: Italian
                "windows-10.x86.ja",                        # language: Japanese
                "windows-10.x86.ko",                        # language: Korean
                "windows-10.x86.lv",                        # language: Latvian
                "windows-10.x86.lt",                        # language: Lithuanian
                "windows-10.x86.nb",                        # language: Norwegian
                "windows-10.x86.pl",                        # language: Polish
                "windows-10.x86.pt-PT",                     # language: Portuguese
                "windows-10.x86.ro",                        # language: Romanian
                "windows-10.x86.ru",                        # language: Russian
                "windows-10.x86.sr",                        # language: Serbian Latin
                "windows-10.x86.sk",                        # language: Slovak
                "windows-10.x86.sl",                        # language: Slovenian
                "windows-10.x86.es",                        # language: Spanish
                "windows-10.x86.Spanish_(Mexico)",                                           # FIXME, "_" corresponding to " "
                "windows-10.x86.sv",                        # language: Swedish
                "windows-10.x86.th",                        # language: Thai
                "windows-10.x86.tr",                        # language: Turkish
                "windows-10.x86.uk",                        # language: Ukrainian
            ]
            ret += t
            ret += [x.replace("x86", "x86_64") for x in t]

        # windows 11
        if True:
            # from https://www.microsoft.com/en-US/software-download/windows11
            ret += [
                "windows-11.x86_64.ar",                      # language: Arabic
                "windows-11.x86_64.pt-BR",                   # language: Brazilian Portuguese
                "windows-11.x86_64.br",                      # language: Bulgarian
                "windows-11.x86_64.zh-CN",                   # language: Chinese Simplified
                "windows-11.x86_64.zh-TW",                   # language: Chinese Traditional
                "windows-11.x86_64.hr",                      # language: Croatian
                "windows-11.x86_64.cz",                      # language: Czech
                "windows-11.x86_64.da",                      # language: Danish
                "windows-11.x86_64.nl",                      # language: Dutch
                "windows-11.x86_64.en-US",                   # language: English
                "windows-11.x86_64.en",                      # language: English International
                "windows-11.x86_64.et",                      # language: Estonian
                "windows-11.x86_64.fi",                      # language: Finnish
                "windows-11.x86_64.fr-CA",                   # language: French Canadian
                "windows-11.x86_64.de",                      # language: German
                "windows-11.x86_64.el",                      # language: Greek
                "windows-11.x86_64.he",                      # language: Hebrew
                "windows-11.x86_64.hu",                      # language: Hungarian
                "windows-11.x86_64.it",                      # language: Italian
                "windows-11.x86_64.ja",                      # language: Japanese
                "windows-11.x86_64.ko",                      # language: Korean
                "windows-11.x86_64.lv",                      # language: Latvian
                "windows-11.x86_64.lt",                      # language: Lithuanian
                "windows-11.x86_64.nb",                      # language: Norwegian
                "windows-11.x86_64.pl",                      # language: Polish
                "windows-11.x86_64.pt-PT",                   # language: Portuguese
                "windows-11.x86_64.ro",                      # language: Romanian
                "windows-11.x86_64.ru",                      # language: Russian
                "windows-11.x86_64.sr",                      # language: Serbian Latin
                "windows-11.x86_64.sk",                      # language: Slovak
                "windows-11.x86_64.sl",                      # language: Slovenian
                "windows-11.x86_64.es",                      # language: Spanish
                "windows-11.x86_64.Spanish_(Mexico)",                                           # FIXME, "_" corresponding to " "
                "windows-11.x86_64.sv",                      # language: Swedish
                "windows-11.x86_64.th",                      # language: Thai
                "windows-11.x86_64.tr",                      # language: Turkish
                "windows-11.x86_64.uk",                      # language: Ukrainian
            ]

        return ret

    def __init__(self, cfg):
        assert isinstance(cfg, ConfigBase)
        self._cfg = cfg

    def download(self, product_id, dest_dir, create_product_subdir=False):
        assert product_id in self.get_product_id_list()

        if not os.path.isdir(dest_dir):
            raise ArgumentError("invalid destination directory %s" % (dest_dir))
        if len(os.listdir(dest_dir)) > 0:
            print("WARNING: destination directory is not empty, files may be overwrited.")

        self._download(product_id, dest_dir, create_product_subdir)

    def get_product_subdir(self, dest_dir, product_id):
        assert product_id in self.get_product_id_list()
        return os.path.join(dest_dir, product_id)

    def get_install_iso_filepath(self, dest_dir, product_id):
        assert product_id in self.get_product_id_list()
        return os.path.join(dest_dir, product_id + ".iso")

    def _download(self, productId, destDir, bCreateProductSubDir):
        destDir = os.path.join(destDir, productId)
        force_mkdir(destDir)

        if productId.startswith("windows-98-"):
            url, digest = _Win98.get_url_and_digest(productId)
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId.startswith("windows-xp-"):
            url = _WinXP.get_url(productId)
            self.__fetch_install_iso_file_simple(productId, url, destDir, digest=digest)
            return

        if productId.startswith("windows-7-"):
            url, digest = _Win7.get_url(productId)
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId.startswith("windows-10-"):
            edition, arch, lang = productId.split(".")
            url, digest = _Win10.get_url_and_digest(arch, lang)
            self.__fetch_install_iso_file_simple(productId, url, destDir, fn=(productId + ".iso"), digest=digest)
            return

        if productId.startswith("windows-11-"):
            edition, arch, lang = productId.split(".")
            url, digest = _Win10.get_url_and_digest(lang)
            self.__fetch_install_iso_file_simple(productId, url, destDir, fn=(productId + ".iso"), digest=digest)
            return

        print("WARNING: product-id %s not supported." % (productId))
        if bCreateProductSubDir:
            os.rmdir(destDir)

    def __fetch_install_iso_file_simple(self, productId, url, destDir, fn=None, digest=None):
        if fn is not None:
            fullfn = os.path.join(destDir, fn)
        else:
            fullfn = os.path.join(destDir, os.path.basename(url))

        if digest is not None:
            digestAlgo = "sha256"
        else:
            digestAlgo = None

        do_fetch(self._cfg, fullfn, [url], digest=digest, digest_algorithm=digestAlgo)

        if fullfn != (productId + ".iso"):
            force_symlink(fullfn, productId + ".iso")


class _Win98:

    @staticmethod
    def get_url_and_digest(productId):
        # from https://winworldpc.com
        wwpDict = {
            "windows-98-se.x86.en-US": {
                "ipfs": "QmTTNMpQALDzioSNdDJyr94rkz5tHoAHCDa155fvHyJb4L/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20(Retail%20Full).7z",
                "hash": "fae5e0759139e7a716782266dd940d9955c68188f4d5ce4cd004a1f7cdcbce63a2e1ec3ba7c6c4b1c1db511be9b409c33ec23c410e1624feb03b8dbe9670f7e4",
            },
            "windows-98-se.x86.it": {
                "ipfs": "QmNh9XDgj7wRyiGgRBK6E32oNyR3jwQXzB9Rjtd97z8jhP/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Italian]%20(ISO).7z",
                "hash": "02f2684b3fa8ec1360b2ef614deb9a10807e88bdf50fbf0c94e7cfbdd0049ba4b092da43aaf854bc2d4a63ac8e05f4ac818f9425e5978f6620a530e1ec22e748",
            },
            "windows-98-se.x86.ja": {
                "ipfs": "Qmcx6kupjyeVhzDZxGDV9ejRfZHDvn9nD6w3M8CFriPoy9/Microsoft%20Windows%2098%20Second%20Edition%20[Japanese]%20(Retail).7z",
                "hash": "6c70c33f1dee8fea9a69848e8c008d0594e10519",
            },
            "windows-98-se.x86.ko": {
                "ipfs": "QmYwiVxkcLUVJ21zc3icTaJf7sxBGTVNVvagNvguLyVNMi/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Korean].7z",
                "hash": "76b4efba67c752ddb415f2d50dcabaf17511f3cfbd4fa1a6eab5c1a8a875a1e72a4db34b052d65a1c1960cbd21de20a79c4854caf138c3fea531599b8516924b",
            },
            "windows-98-se.x86.pt-PT": {
                "ipfs": "QmcoMbStuYpPpnK7MAwVP5nb6f9ZwmdRHKX56kbgXK31hq/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Portuguese].7z",
                "hash": "7b5263b05c846c6853caba27985602d3d5ac61c4eb8398327ee1ffc62b09dc19a3e14ce66a9860641106b756ca049f00745cd017b330cf50d797130a1ccf1890",
            },
            "windows-98-se.x86.ru": {
                "ipfs": "QmcJh6sDnFURRSyykXHnPcQaUMf7dkKmSbpdwWeMWx8QRZ/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Russian].7z",
                "hash": "d9e638d16d1a798f9d39e2439c76c9ee2f94e341df631af3cb44f0b241c346aa40d60d9aecd5771efc26cfe08fabb550256dedf958450fc1c221f329d28bc680",
            },
            "windows-98-se.x86.sl": {
                "ipfs": "QmVe4wjgVVhRSp9Hgnfa2EcVNuMKANMbgcsPazxgPm9MDe/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Slovenian].7z",
                "hash": "0df54b644f189e28e2158a9f9953203ab4831c2f7a8c4115d82e1e8234d63a865c93097728dbd6d5e896500c2efc5d16f813d643ced52b4bcc01a7ab9f124dc5",
            },
            "windows-98-se.x86.es": {
                "ipfs": "QmPbSxkStSQWhkaHLEmWfuCXuybDVZPWJYUH18PzEJC8VE/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Spanish].7z",
                "hash": "7d6ea0bc92da115cd258dc4b1d8750455e9aa7e521f573eaf044aef9cece1057babcfb3da7cdc2e0e12abfedf29001d905ec2dc227e58739c5fa363c8597ac8b",
            },
            "windows-98-se.x86.tr": {
                "ipfs": "QmQWP3LnxrQG5Me6vnFjVbp1hA3WcNaKv4h5Yi1fzYCxst/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Turkish].7z",
                "hash": "7a59f5d69280889e9734a742a86d3356c1937a11582adfbeb87371fbdfe89f8bf9576b1d80fd6d5fe0f3f06a9632b577321a5cb730fc8b325fd4ec6548b5e571",
            },
            "windows-98-se-oem.x86.en-US": {
                "ipfs": "QmXZ9oEejNbr8gpGrZtPuFa4SSsjBgpunxyahHL53kyHRx/Microsoft%20Windows%2098%20Second%20Edition.7z",
                "hash": "b5d78b6a38b485a77c7d4a71d06a41f6201bfbd14c3bff41a551cc0455c23f9764415b0e000b50b85de5e4e3f9e992a9762bfe31ba68c036d33fc4610a0693ae",
            },
            "windows-98-se-oem.x86.cz": {
                "ipfs": "QmNuZBoFQNiKEEmj2QD4UsQG79aTxXthXTC89KDKoVEGsF/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20(OEM)%20[Czech]%20(ISO).7z",
                "hash": "f89eef24544109fedbb78148f9d86418f58ee5d0a029ab384294b41da0efb557b9ea769b112ee86bf5833d4458698835d3a4fb36beea6363bee1976a4347d951",
            },
            "windows-98-se-oem.x86.nl": {
                "ipfs": "Qmb6dGcF2D3goGzyd5QwdhGfQo2uaFar6ptvxLDhYKd5aZ/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Dutch]%20(OEM)%20(ISO).7z",
                "hash": "8f095532b152d1841daef3a1d2c075ffad09160c87629249946f839bdaf2cf1591eb3e7311735a94b2021131867bc728a6c52d0e4a0dc4a1c36fbc57c6e211d3",
            },
            "windows-98-se-oem.x86.fi": {
                "ipfs": "QmZjNEb9zk2nYjvmE5rBCbAywYyphzUG9zJ6GsMAW2GJFr/Microsoft%20Windows%2098%20Second%20Edition%20[Finnish]%20(OEM)%20(ISO).7z",
                "hash": "c510c7c739dd0bb8fd1628023d39359d9c0aba51",
            },
            "windows-98-se-oem.x86.de": {
                "ipfs": "Qmbg7ZeM3aJBGQeV3g6jUZvE6p45bzQGKXSsfv4pT9r47i/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[German]%20(ISO).7z",
                "hash": "a53863c42b889f21e093b8b3c958a4245773446709959479ec15ecc3ec48cc89e8133377ffd3f4c2d817e43d4fdab3416dbcb3ae26d9e6c737590320afd7be89",
            },
            "windows-98-se-oem.x86.hu": {
                "ipfs": "QmSUV3JM2m3vZnckD4dYds1qyhtt5DRUUTKQmBuoP636jN/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Hungarian]%20(ISO).7z",
                "hash": "8a80b80db5aff467e8286a478045f982ff0d397bc4f0ac4fc7004f25a27d11864b304a971913844a5712848f3dc117ed36a5c176c62533144158eedca3ae9658",
            },
            "windows-98-se-oem.x86.nb": {
                "ipfs": "QmRgwmnMhgjw5sWxidG9RrQs9LmKxjp7u9envEbz2HgvCU/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Norwegian]%20(OEM).7z",
                "hash": "76e8d1766b6622907c46dd205384e19aa45862b4070cfaf6f53988f46aad39b05b11a09e23fdd9c1192f60cfa8a5bdbd3052279a7cfd749d5c0d6618d2a04981",
            },
            "windows-98-se-oem.x86.pl": {
                "ipfs": "QmSR7JJ8koThZi9qnzNDxAn3xkk8uSq7vHPdKNWTBJZ3mc/Microsoft%20Windows%2098%20Second%20Edition%20[Polish]%20(OEM)%20(ISO).7z",
                "hash": "f7b51b107c67e692a9fc0be55666956fed8824fe",
            },
            "windows-98-se-oem.x86.pt-BR": {
                "ipfs": "QmdVGugKoJD8xrHHRonwMcBBrSquzFtEKutx44wujXmZ6R/Microsoft%20Windows%2098%20Second%20Edition%20[Portuguese-Brazil]%20(OEM)%20(ISO).7z",
                "hash": "a5cce6352a5215ef7a420843eff5df50db68af0a",
            },
            "windows-98-se-oem.x86.sv": {
                "ipfs": "QmUziMnCgwavWh7yweh2xBgsCrQuMj59Ugu2ExsZqpt1r2/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Swedish]%20[OEM].7z",
                "hash": "6df0d9c937058158126b80b315345f3a3cbfae06a1e62dddfab4aaff6a90773b480418ddde6a790eedf398282491ca941b3b2c8e85f4d5d1c757fafeb3a65318",
            },
            "windows-98-se-oem.x86.zh-TW": {
                "ipfs": "QmRVZVAUyJ99b75cjYndFPn2HpxQEsANDFK2wMvTmSXt3R/Microsoft%20Windows%2098%20Second%20Edition%20(4.10.2222)%20[Trad.%20Chinese]%20(OEM)%20(ISO).7z",
                "hash": "59105c256829e61c4155df3ad9e68f42b5f6c5006bb9ec9f43c8db763a2a465958320e8c28bfdd22cd996489227d28447de86e85d7d0e6aabae39e0e234f995f",
            },
        }

        # FIXME
        url = "http://gateway.pinata.cloud/ipfs"

        if productId in wwpDict:
            return (os.path.join(url, wwpDict[productId]["ipfs"]), wwpDict["hash"])

        assert False


class _WinXP:

    @staticmethod
    def get_url(productId):
        # from https://windowslay.com/windows-xp-sp3-iso-download/
        if productId == "windows-xp-home.x86.en-US":
            return "https://files.windowslay.com/en_windows_xp_professional_sp3_Nov_2013_Incl_SATA_Drivers.iso?_gl=1*1mgf9k5*_ga*NDQwNzA4Mzk1LjE2NDU4NDAyNzQ.*_ga_Z8ZFNPE9ZJ*MTY0NTg0MDI2NS4xLjEuMTY0NTg0MDQ4NS4w&_ga=2.40777185.291888328.1645840274-440708395.1645840274"

        # from https://windowslay.com/windows-xp-professional-64-bit-iso-download
        if productId == "windows-xp-professional.x86.en-US":
            return "https://files.windowslay.com/en_windows_xp_professional_64-bit_dvd.iso?_gl=1*1qg4di5*_ga*NDQwNzA4Mzk1LjE2NDU4NDAyNzQ.*_ga_Z8ZFNPE9ZJ*MTY0NTg0MDI2NS4xLjEuMTY0NTg0MDMyMC4w&_ga=2.235393346.291888328.1645840274-440708395.1645840274"

        assert False


class _Win7:

    @staticmethod
    def get_url(productId):
        # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links

        if productId == "windows-7-home-premium.x86.en-US":
            return "https://download.microsoft.com/download/E/D/A/EDA6B508-7663-4E30-86F9-949932F443D0/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x86FRE_en-US.iso"
        if productId == "windows-7-home-premium.x86_64.en-US":
            return "https://download.microsoft.com/download/E/A/8/EA804D86-C3DF-4719-9966-6A66C9306598/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x64FRE_en-US.iso"
        if productId == "windows-7-professional.x86.en-US":
            return "https://download.microsoft.com/download/C/0/6/C067D0CD-3785-4727-898E-60DC3120BB14/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x86FRE_en-US.iso"
        if productId == "windows-7-professional.x86_64.en-US":
            return "https://download.microsoft.com/download/0/6/3/06365375-C346-4D65-87C7-EE41F55F736B/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x64FRE_en-US.iso"
        if productId == "windows-7-ultimate.x86.en-US":
            return "https://download.microsoft.com/download/1/E/6/1E6B4803-DD2A-49DF-8468-69C0E6E36218/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x86FRE_en-US.iso"
        if productId == "windows-7-ultimate.x86_64.en-US":
            return "https://download.microsoft.com/download/5/1/9/5195A765-3A41-4A72-87D8-200D897CBE21/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x64FRE_en-US.iso"

        if productId.startswith("windows-7-enterprise-"):
            if productId == "windows-7-enterprise.x86.en-US":
                url = "https://idatavn-my.sharepoint.com/:u:/g/personal/data01_phanmemchat_net/Eec-CsxcwntJkpS_qCnrYPEBp5GFlChmzzfFAlisjR96Kw?e=fpr76R"
            elif productId == "windows-7-enterprise.x86_64.en-US":
                url = "https://idatavn-my.sharepoint.com/:u:/g/personal/data01_phanmemchat_net/EbQ80EYnmyNFqprGKPmf3xgBzyHkeLvPTeGOpvhmePYh5Q?e=lwMDXi"
            else:
                assert False

            browser = selenium.webdriver.WebKitGTK()
            browser.implicitly_wait(60)
            try:
                browser.get(url)
                time.sleep(5)

                button = browser.find_elements_by_xpath("//button[class='od-Button od-ButtonBarCommand od-ButtonBarCommand--button']")[1]
                button.click()

                return url
            finally:
                browser.quit()


class _Win10:

    archDict = {
        "x86":    "32-bit",
        "x86_64": "64-bit",
    }

    langDict = {
        "ar":    "Arabic",
        "pt-BR": "Brazilian Portuguese",
        "br":    "Bulgarian",
        "zh-CN": "Chinese Simplified",
        "zh-TW": "Chinese Traditional",
        "hr":    "Croatian",
        "cz":    "Czech",
        "da":    "Danish",
        "nl":    "Dutch",
        "en-US": "English",
        "en":    "English International",
        "et":    "Estonian",
        "fi":    "Finnish",
        "fr-CA": "French Canadian",
        "de":    "German",
        "el":    "Greek",
        "he":    "Hebrew",
        "hu":    "Hungarian",
        "it":    "Italian",
        "ja":    "Japanese",
        "ko":    "Korean",
        "lv":    "Latvian",
        "lt":    "Lithuanian",
        "nb":    "Norwegian",
        "pl":    "Polish",
        "pt-PT": "Portuguese",
        "ro":    "Romanian",
        "ru":    "Russian",
        "sr":    "Serbian Latin",
        "sk":    "Slovak",
        "sl":    "Slovenian",
        "es":    "Spanish",
        "Spanish_(Mexico)": "Spanish (Mexico)",
        "sv":    "Swedish",
        "th":    "Thai",
        "tr":    "Turkish",
        "uk":    "Ukrainian",
    }

    @classmethod
    def get_url_and_digest(cls, arch, lang):
        browser = selenium.webdriver.WebKitGTK()
        browser.implicitly_wait(60)
        try:
            browser.get('https://www.microsoft.com/en-US/software-download/windows10ISO')
            time.sleep(5)

            browser.find_element_by_id("product-edition").select_by_index(1)
            browser.find_element_by_id("submit-proudct-edition").click()
            time.sleep(5)

            browser.find_element_by_id("product-language").select_by_visible_text(cls.langDict[lang])
            browser.find_element_by_id("submit-sku").click()
            time.sleep(5)

            url = browser.find_element_by_partial_link_text(cls.archDict[arch]).get_attribute('href')
            digest = browser.find_element_by_xpath("//td[text='%s %s']/following-sibling" % (cls.langDict[lang], cls.archDict[arch])).text
            return (url, digest)
        finally:
            browser.quit()


class _Win11:

    # same as windows 10
    langDict = _Win10.langDict

    @classmethod
    def get_url_and_digest(cls, lang):
        browser = selenium.webdriver.WebKitGTK()
        browser.implicitly_wait(60)
        try:
            browser.get('https://www.microsoft.com/en-US/software-download/windows11')
            time.sleep(5)

            browser.find_element_by_id("product-edition").select_by_index(1)
            browser.find_element_by_id("submit-proudct-edition").click()
            time.sleep(5)

            browser.find_element_by_id("product-language").select_by_visible_text(cls.langDict[lang])
            browser.find_element_by_id("submit-sku").click()
            time.sleep(5)

            url = browser.find_element_by_partial_link_text('64-bit').get_attribute('href')
            digest = browser.find_element_by_xpath("//td[text='%s 64-bit']/following-sibling" % (cls.langDict[lang])).text
            return (url, digest)
        finally:
            browser.quit()

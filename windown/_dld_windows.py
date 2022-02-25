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
from ._config import ConfigBase, Param
from ._errors import ArgumentError, DownloadError
from ._handy import do_fetch


class WindowsDownloader:

    @staticmethod
    def get_product_id_list():
        ret = []

        # windows 98
        if True:
            ret += [
                "windows-98.x86.en-US",
                "windows-98-se.x86.en-US",
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

    def __init__(self, cfg, param):
        assert isinstance(cfg, ConfigBase)
        assert isinstance(param, Param) and param.check()
        self._cfg = cfg
        self._param = param

    def download(self, product_id_list, dest_dir):
        for product_id in product_id_list:
            if product_id not in self.get_product_id_list():
                raise ArgumentError("invalid product-id %s" % (product_id))
        if not os.path.isdir(dest_dir):
            raise ArgumentError("invalid destination directory %s" % (dest_dir))
        if len(os.listdir(dest_dir)) > 0:
            print("WARNING: destination directory is not empty, files may be overwrited.")

        if len(product_id_list) == 1:
            self._download(product_id_list[0], dest_dir, False)
        else:
            for product_id in product_id_list:
                d = os.path.join(dest_dir, product_id)
                force_mkdir(d)
                self._download(product_id, d, True)

    def _download(self, productId, destDir, bDeleteWhenNotSupport):
        if productId.startswith("windows-7-"):
            url, digest = _Win7.get_url(arch, lang)
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
        if bDeleteWhenNotSupport:
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
            force_symlink(fullfn, os.path.join(destDir, productId + ".iso"))


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


# https://tb.rg-adguard.net/public.php?lang=zh-CN

# # good
# https://github.com/pbatard/Fido/blob/master/Fido.ps1

# https://superuser.com/questions/1175110/safe-way-to-verify-that-a-microsoft-iso-has-not-been-tampered-with


# reply this issue:
# https://github.com/pbatard/rufus/issues/1875



# https://www.heidoc.net/php/myvsdump.php


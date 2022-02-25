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
from ._download import do_fetch


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
            # "_" corresponding to " "
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
                "windows-10.x86.en_US",                     # language: English
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
                "windows-10.x86.Spanish_(Mexico)",
                "windows-10.x86.sv",                        # language: Swedish
                "windows-10.x86.th",                        # language: Thai
                "windows-10.x86.tr",                        # language: Turkish
                "windows-10.x86.uk",                        # language: Ukrainian
            ]
            ret += t
            ret += [x.replace("x86", "x86_64") for x in t]

        # windows 11
        if True:
            ret += [
                "windows-11.x86.en-US",
                "windows-11.x86_64.en-US",
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
        if productId == "windows-7-home-premium.x86.en-US":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            url = "https://download.microsoft.com/download/E/D/A/EDA6B508-7663-4E30-86F9-949932F443D0/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x86FRE_en-US.iso"
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId == "windows-7-home-premium.x86_64.en-US":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            url = "https://download.microsoft.com/download/E/A/8/EA804D86-C3DF-4719-9966-6A66C9306598/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x64FRE_en-US.iso"
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId == "windows-7-professional.x86.en-US":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            url = "https://download.microsoft.com/download/C/0/6/C067D0CD-3785-4727-898E-60DC3120BB14/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x86FRE_en-US.iso"
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId == "windows-7-professional.x86_64.en-US":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            url = "https://download.microsoft.com/download/0/6/3/06365375-C346-4D65-87C7-EE41F55F736B/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x64FRE_en-US.iso"
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId == "windows-7-ultimate.x86.en-US":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            url = "https://download.microsoft.com/download/1/E/6/1E6B4803-DD2A-49DF-8468-69C0E6E36218/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x86FRE_en-US.iso"
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId == "windows-7-ultimate.x86_64.en-US":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            url = "https://download.microsoft.com/download/5/1/9/5195A765-3A41-4A72-87D8-200D897CBE21/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x64FRE_en-US.iso"
            self.__fetch_install_iso_file_simple(productId, url, destDir)
            return

        if productId.startswith("windows-10-"):
            edition, arch, lang = productId.split(".")
            url = _Win10.get_url(arch, lang)
            self.__fetch_install_iso_file_simple(productId, url, destDir, fn=(productId + ".iso"))
            return

        print("WARNING: product-id %s not supported." % (productId))
        if bDeleteWhenNotSupport:
            os.rmdir(destDir)

    def __fetch_install_iso_file_simple(self, productId, url, destDir, fn=None):
        if fn is not None:
            fullfn = os.path.join(destDir, fn)
        else:
            fullfn = os.path.join(destDir, os.path.basename(url))

        do_fetch(self._cfg, fullfn, [url])

        if fullfn != (productId + ".iso"):
            force_symlink(fullfn, os.path.join(destDir, productId + ".iso"))


class _Win10:

    @staticmethod
    def get_url(arch, lang):
        browser = selenium.webdriver.WebKitGTK()
        try:
            browser.implicitly_wait(5)

            browser.get('https://www.microsoft.com/en-US/software-download/windows10ISO')
            time.sleep(5)

            browser.find_element_by_id("product-edition").select_by_index(1)
            browser.find_element_by_id("submit-proudct-edition").click()
            time.sleep(5)

            d = {
                "ar":    "Arabic",
                "pt-BR": "Brazilian Portuguese",
                "br":    "Bulgarian",
                "zh-CN": "Chinese Simplified",
                "zh-TW": "Chinese Traditional",
                "hr":    "Croatian",
                "cz":    "Czech",
                "da":    "Danish",
                "nl":    "Dutch",
                "en_US": "English",
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
            browser.find_element_by_id("product-language").select_by_visible_text(d[lang])
            browser.find_element_by_id("submit-sku").click()
            time.sleep(5)

            d = {
                "x86":    "32-bit",
                "x86_64": "64-bit",
            }
            return browser.find_element_by_partial_link_text(d[arch]).get_attribute('href')
        finally:
            browser.quit()





https://tb.rg-adguard.net/public.php?lang=zh-CN

# good
https://github.com/pbatard/Fido/blob/master/Fido.ps1

https://superuser.com/questions/1175110/safe-way-to-verify-that-a-microsoft-iso-has-not-been-tampered-with


reply this issue:
https://github.com/pbatard/rufus/issues/1875



https://www.heidoc.net/php/myvsdump.php



import sys, time
from selenium import webdriver

selectEdition = """
options = Array.from(document.querySelectorAll('#product-edition option'));
optionToSelect = Math.max.apply(null, options.map(o => o.value));
options.filter(o => o.value == optionToSelect)[0].selected=true;
"""

selectLanguage = """
options = Array.from(document.querySelectorAll('#product-languages option'));
options.filter(o => o.value.includes('"English"'))[0].selected=true;
"""

options = webdriver.firefox.options.Options()
options.headless = True
profile = webdriver.FirefoxProfile()
browser = webdriver.Firefox(profile, options=options)

link = ''

try:
    browser.get('https://www.microsoft.com/en-US/software-download/windows10ISO')
    time.sleep(5)
    browser.execute_script(selectEdition)
    browser.find_element_by_id('submit-product-edition').click()
    time.sleep(5)
    browser.execute_script(selectLanguage)
    browser.find_element_by_id('submit-sku').click()
    time.sleep(5)
    link = browser.find_element_by_partial_link_text('64-bit').get_attribute('href')
    time.sleep(5)

finally:
    browser.quit()
    print(link)
    sys.exit(1 if len(link) == 0 else 0)




import sys, json, time
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
def showiso(isoname):
    iso = {
        'Windows81': '52',
        'Win10Education': '1056',
        'Win10HomeAndPro': '1060',
        'Win10HomeChina': '1061'
    }
    x = json.dumps(iso)
    x = json.loads(x)
    if(isoname == ''):
        for isos in iso:
            print(isos)
    else:
        opts = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows Phone 10.0;  Android 6.0.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Mobile Safari/537.36 Edge/14.14348")
        browser = Firefox(profile, firefox_options=opts)
        iso = x[isoname]
        print(iso)
        product = "document.getElementById('product-edition').innerHTML = `<option value='" + str(iso) + "' selected='selected'>dio</option>`"
        print(product)
        browser.get("https://www.microsoft.com/en-us/software-download/windows10ISO")
        time.sleep(2)
        browser.execute_script(product)
        browser.find_element_by_id('submit-product-edition').click()
        time.sleep(5)

if __name__ == '__main__':
    usage = "windows iso downloader\nusage:\n./" + sys.argv[0] + " --showiso\n./" + sys.argv[0] + " windowsISONAME"
    if(len(sys.argv) == 1):
        print(usage)
    elif(len(sys.argv) == 2):
        if(sys.argv[1] == "--showiso"):
            print('available iso:')
            showiso('')
            exit(0)
        try:
            showiso(sys.argv[1])
        except Exception as e:
            print(e)
            print('iso not found.')
    else:
        print(usage)
        exit(1)


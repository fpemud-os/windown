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

from ._config import ConfigBase, Param


class WindowsDownloader:

    @staticmethod
    def get_product_id_list(self):
        ret = []

        # windows 98
        if True:
            ret += [
                "windows-98.x86.en_us",
                "windows-98-se.x86.en_us",
            ]

        # windows xp
        if True:
            t = [
                "windows-xp-home.x86.en_us",
                "windows-xp-professional.x86.en_us",
            ]
            ret += t
            ret += [x.replace("x86", "x86_64") for x in t]

        # windows 7
        if True:
            t = [
                "windows-7-starter.x86.en_us",
                "windows-7-home-basic.x86.en_us",
                "windows-7-home-premium.x86.en_us",
                "windows-7-professional.x86.en_us",
                "windows-7-ultimate.x86.en_us",
                "windows-7-enterprise.x86.en_us",
            ]
            ret += t
            ret += [x.replace("x86", "x86_64") for x in t]

        return ret

    def __init__(self, cfg=None, param=None):
        if cfg is not None:
            assert isinstance(cfg, ConfigBase)
            self._cfg = cfg
        else:
            self._cfg = EtcDirConfig()

        assert isinstance(param, Param)
        assert param.check()
        self._param = param

    def download(self, product_id_list, dest_dir):
        if not os.path.isdir(dest_dir):
            raise ArgumentError("invalid destination directory %s" % (dest_dir))
        if len(os.listdir(dest_dir)) > 0:
            print("WARNING: destination directory is not empty, files may be overwrited.")

        if len(product_id_list) == 1:
            self._download(product_id_list[0], dest_dir)
        else:
            for product_id in product_id_list:
                d = os.path.join(dest_dir, product_id)
                force_mkdir(d)
                self._download(product_id, d)

    def _download(self, product_id, dest_dir):
        if product_id == "windows-7-home-premium.x86.en_us":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            # this is an easy one
            url = "https://download.microsoft.com/download/E/D/A/EDA6B508-7663-4E30-86F9-949932F443D0/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x86FRE_en-us.iso"
            # FIXME: wget


        if product_id == "windows-7-home-premium.x86_64.en_us":
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            # this is an easy one
            url = "https://download.microsoft.com/download/E/A/8/EA804D86-C3DF-4719-9966-6A66C9306598/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_HOMEPREMIUM_x64FRE_en-us.iso"
            # FIXME: wget






    def get_install_iso_filename_by_arch_version(self, arch, version):
        versionPathDict = {
            wstage4.Version.WINDOWS_98: "windows-98",
            wstage4.Version.WINDOWS_XP: "windows-xp",
            wstage4.Version.WINDOWS_7: "windows-7",
        }
        archNameDict = {
            wstage4.Arch.X86: "x86",
            wstage4.Arch.X86_64: "amd64",
        }

        if version == wstage4.Version.WINDOWS_98:
            return versionPathDict[version] + "-setup.iso"
        elif version in wstage4.Version.WINDOWS_XP:
            return versionPathDict[version] + "-setup-" + archNameDict[arch] + ".iso"
        elif version == wstage4.Version.WINDOWS_7:
            return versionPathDict[version] + "-setup-" + archNameDict[arch] + ".iso"
        else:
            assert False

    def get_install_iso_filepath_by_arch_version(self, arch, version):
        if version == wstage4.Version.WINDOWS_98:
            # FIXME
            return "/usr/share/microsoft-windows-xp-setup-cd/windows-xp-setup-amd64.iso"
        else:
            return os.path.join(self._dir, self.get_install_iso_filename_by_arch_version(arch, version))

    def get_prefered_edition_by_version(self, version):
        d = {
            wstage4.Version.WINDOWS_98: wstage4.Edition.WINDOWS_98_SE,
            wstage4.Version.WINDOWS_XP: wstage4.Edition.WINDOWS_XP_PROFESSIONAL,
            wstage4.Version.WINDOWS_7: wstage4.Edition.WINDOWS_7_ULTIMATE,
        }
        return d[version]

    def download_files_by_arch_version(self, arch, version):
        fullfn = self.get_install_iso_filepath_by_arch_version(arch, version)

        # FIXME
        if version == wstage4.Version.WINDOWS_98:
            if os.path.exists(fullfn):
                return fullfn
            else:
                raise Exception("windows 98 iso does not exist")

        url = self._get_url_by_arch_edition(arch, self.get_prefered_edition_by_version(version))
        if os.path.exists(fullfn):
            print("Files already downloaded.")
        else:
            FmUtil.wgetDownload(url, fullfn)
        return fullfn

    def _get_url_by_arch_edition(self, arch, edition):
        if arch == wstage4.Arch.X86 and edition == wstage4.Edition.WINDOWS_7_PROFESSIONAL:
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            return "https://download.microsoft.com/download/C/0/6/C067D0CD-3785-4727-898E-60DC3120BB14/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_PROFESSIONAL_x86FRE_en-us.iso"

        if arch == wstage4.Arch.X86_64 and edition == wstage4.Edition.WINDOWS_7_PROFESSIONAL:
            # from https://techpp.com/2018/04/16/windows-7-iso-official-direct-download-links
            return "https://download.microsoft.com/download/5/1/9/5195A765-3A41-4A72-87D8-200D897CBE21/7601.24214.180801-1700.win7sp1_ldr_escrow_CLIENT_ULTIMATE_x64FRE_en-us.iso"

        assert False




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
    browser.get('https://www.microsoft.com/en-us/software-download/windows10ISO')
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
        browser.get("https://www.microsoft.com/it-it/software-download/windows10ISO")
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
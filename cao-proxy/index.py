from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.firefox.options import Options
import os
import sys
import requests
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from xvfbwrapper import Xvfb

_api_url = "http://toolnuoi999.tk/api"

def _init_driver():
    firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
    # firefox_capabilities['marionette'] = True
    firefox_capabilities['binary'] = 'geckodriver.exe'
    firefox_capabilities['acceptInsecureCerts'] = True
    firefox_capabilities['acceptUntrustedCertificates'] = True
    firefox_capabilities['assumeUntrustedCertificateIssuer'] = True
    firefox_capabilities['acceptNextAlert'] = True

    fp = webdriver.FirefoxProfile()
    fp.accept_untrusted_certs = True
    fp.assume_untrusted_cert_issuer = True
    # fp.setAcceptUntrustedCertificates = True
    # fp.setAssumeUntrustedCertificateIssuer = False
    fp.accept_next_alert = True
    fp.set_preference('permissions.default.image', 2)
    fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    fp.update_preferences()

    options = Options()

    driver = webdriver.Firefox(firefox_options=options, firefox_profile=fp, capabilities=firefox_capabilities)

    return driver

#cao https://www.sslproxies.org/

def _cao_sslproxies_org():
    vdisplay = Xvfb()
    vdisplay.start()
    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = _init_driver()

    url = "https://www.sslproxies.org/"
    driver.get(url)

    # driver.find_element_by_xpath("//select[@name='proxylisttable_length']/option[3]").click()


    while "disabled" not in driver.find_element_by_id("proxylisttable_next").get_attribute("class"):
        rows = driver.find_elements_by_xpath("//tr[@role='row']")

        for row in rows:
            try:

                ip = row.find_elements_by_tag_name('td')[0].get_attribute('innerHTML').strip()
                port = row.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').strip()

                print('ip|port : {}|{}'.format(ip, port))

                _create_proxy({
                    'ip': ip,
                    'port': port,
                    'status': 1
                })
            except Exception as e:
                print(e)

        driver.find_element_by_id("proxylisttable_next").find_element_by_tag_name("a").click()


    driver.save_screenshot('cao_sslproxies_org.png')
    driver.quit()
    display.stop()
    vdisplay.stop()

def _cao_spys_one():
    #http://spys.one/en/https-ssl-proxy/
    vdisplay = Xvfb()
    vdisplay.start()
    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = _init_driver()

    url = "http://spys.one/en/https-ssl-proxy/"
    driver.get(url)

    links = []

    for a in driver.find_elements_by_class_name("spy1xx")[0].find_elements_by_tag_name("a"):
        links.append("{}/{}".format("http://spys.one/en/https-ssl-proxy", a.text.strip()) )

    for link in links:
        driver.get(link)
        rows = driver.find_elements_by_class_name("spy1xx")

        for row in rows:
            try:
                raw = row.find_elements_by_tag_name("td")[0].text

                ip = raw.split(" ")[1].split(":")[0]
                port = raw.split(" ")[1].split(":")[1]

                print('ip|port : {}|{}'.format(ip, port))

                _create_proxy({
                    'ip': ip,
                    'port': port,
                    'status': 1
                })
            except Exception as e:
                print(e)

    driver.quit()
    display.stop()
    vdisplay.stop()
def _create_proxy(proxy):
    _proxy = requests.post("{}/proxy".format(_api_url), proxy).json()
    return _proxy


_cao_sslproxies_org()
_cao_spys_one()
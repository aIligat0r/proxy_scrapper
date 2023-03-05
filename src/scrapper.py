import re
import argparse

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from bs4 import BeautifulSoup
import fake_headers
import requests


def get_driver():
    service = Service(executable_path=r"../bin/geckodriver.exe")
    driver = Firefox(service=service)
    return driver


class Socks5Scrapper:
    """
    Free SOCKS5 resources parser
    """

    HEADERS = fake_headers.Headers(headers=True).generate()

    def __init__(self):
        self.driver = None

    def get_page(self, url: str) -> BeautifulSoup:
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def free_proxy_cz(self):
        url = "http://free-proxy.cz/ru/proxylist/country/all/socks5/ping/all"
        html = self.get_page(url)
        ips = html.find_all("td", {"class": "left", "style": "text-align:center"})
        ports = html.find_all("span", {"class": "fport"})
        return ["%s:%s" % (ips[i].text, ports[i].text) for i in range(len(ips))]

    def spys_one(self):
        url = "https://spys.one/socks/"
        html = self.get_page(url)
        ips = html.find_all(
            "tr", {"onmouseover": re.compile(r"this.style.background=")}
        )
        return [re.sub("SOCKS5.*", "", socks.text) for socks in ips]

    def hidemy_name(self):
        url = "https://hidemy.name/ru/proxy-list/?type=5#list"
        html = BeautifulSoup(
            str(self.get_page(url).find_all("div", {"class": "table_block"})),
            "html.parser",
        )
        ips = html.find_all("td")
        result = []
        i = 0
        try:
            for ip in range(len(ips[7:])):
                result.append(ips[7:][i].text + ":" + ips[7:][i + 1].text)
                i += 7
        except:
            pass
        return result

    def freeproxy_world(self):
        url = "https://www.freeproxy.world/?type=socks5"
        html = self.get_page(url)
        ips = html.find_all("td", {"class": "show-ip-div"})
        ports = html.find_all("a", {"href": re.compile(r"/?port=\d*")})
        return [
            ips[i].text.replace("\n", "") + ":" + ports[i].text for i in range(len(ips))
        ]

    def proxy_list_download(self):
        url = "https://www.proxy-list.download/SOCKS5"
        html = self.get_page(url)
        ips = html.find_all("td")
        result = []
        i = 0
        try:
            for ip in range(len(ips)):
                result.append(
                    ips[i].text.replace("\n", "").replace(" ", "")
                    + ":"
                    + ips[i + 1].text.replace("\n", "").replace(" ", "")
                )
                i += 5
        except:
            pass
        return result

    def proxydocker_com(self):
        url = "https://www.proxydocker.com/en/socks5-list/"
        html = self.get_page(url)
        return [
            socks.text
            for socks in html.find_all(
                "a",
                {
                    "href": re.compile(
                        r"https://www\.proxydocker\.com/en/proxy/\d\d?\d?\d?\."
                    )
                },
            )
        ]

    def vpnside_com(self):
        url = "https://www.vpnside.com/proxy/list/"
        self.driver.get(url)
        self.driver.find_element(By.XPATH, '//*[@id="table_1"]/thead/tr/th[4]').click()
        self.driver.find_element(By.XPATH, '//*[@id="table_1"]/thead/tr/th[4]').click()
        socks = []
        for i in range(25):
            ip = self.driver.find_element(
                By.XPATH,
                f"/html/body/div[1]/div[3]/div/main/article/div/div/div/table/tbody/tr[{i + 1}]/td[1]",
            ).text
            port = self.driver.find_element(
                By.XPATH,
                f"/html/body/div[1]/div[3]/div/main/article/div/div/div/table/tbody/tr[{i + 1}]/td[2]",
            ).text
            socks.append(f"{ip}:{port}")
        return socks

    def premiumproxy_net(self):
        socks = []
        url = "https://premiumproxy.net/socks-proxy-list"
        response = requests.get(url, headers=self.HEADERS)
        html = BeautifulSoup(response.text, "html.parser")
        trs = html.find_all("tr", {"class": "pp1x"})
        for i in trs:
            host_port = i.find_next("font", {"class": "pp14"})
            if host_port:
                socks.append(host_port.text)
        return list(set(socks))

    def geonode_com(self):
        url = (
            "https://proxylist.geonode.com/api/proxy-list?"
            "limit=500&page=1&sort_by=lastChecked"
            "&sort_type=desc&protocols=socks5"
        )
        socks = []
        for retry in range(3):
            try:
                response_data = requests.get(url, headers=self.HEADERS).json()["data"]
                for sock in response_data:
                    socks.append("%s:%s" % (sock["ip"], sock["port"]))
                return socks
            except:
                pass
        return socks

    def github_public_repos(self):
        socks = []
        repos_urls = [
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/baklazhan1337/proxier/main/socks5.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        ]
        for url in repos_urls:
            response = requests.get(url)
            socks += response.text.split()
        return list(set(socks))

    @staticmethod
    def _args_conf():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-d",
            "--driver",
            help="get socks5 via driver (from dynamic content resources)",
            action="store_true",
        )
        return parser.parse_args()

    def get_socks_list(self):
        args = Socks5Scrapper._args_conf()
        socks_list = []
        resources = {
            "geonode.com": self.geonode_com(),
            "github": self.github_public_repos(),
        }
        if args.driver:
            self.driver = get_driver()
            resources.update(
                {
                    "spys.one": self.spys_one(),
                    "hidemy.name": self.hidemy_name(),
                    "free-proxy.cz": self.free_proxy_cz(),
                    "freeproxy.world": self.freeproxy_world(),
                    "proxy-list.download": self.proxy_list_download(),
                    "proxydocker.com": self.proxydocker_com(),
                    "vpnside.com": self.vpnside_com(),
                    "premiumproxy.net": self.premiumproxy_net(),
                }
            )
            self.driver.close()
        for resource in resources:
            if not resources[resource]:
                print("[-] empty results from", resource)
                continue
            socks_list += resources[resource]
        return list(set(socks_list))

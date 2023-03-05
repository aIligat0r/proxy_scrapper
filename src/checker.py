from multiprocessing.dummy import Pool

import urllib3
import requests
import fake_headers
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

THREADS = 250
RETRIES = 3
TIMEOUT = 15
URL_FOR_CHECK = "https://api.myip.la"
OUT_FILENAME = "checked_socks.txt"
with open("../socks_list/%s" % OUT_FILENAME, "w") as file:
    pass  # clean file


class ProxyChecker:
    """
    SOCKS5 checker via HTTP requests
    Save good results to 'socks_list/checked_socks.txt'
    """

    HEADERS = fake_headers.Headers(headers=True).generate()

    def __init__(self, socks_list: list):
        self.socks_list = socks_list

    def _requester(self, socks: str):
        proxy = {"http": "socks5h://%s" % socks, "https": "socks5h://%s" % socks}
        for retry in range(RETRIES):
            try:
                response = requests.get(
                    url=URL_FOR_CHECK,
                    headers=self.HEADERS,
                    timeout=TIMEOUT,
                    proxies=proxy,
                )
                ProxyChecker._save_socks(socks)
                return socks
            except:
                pass
        return False

    def pool_requests(self):
        results = []
        with Pool(THREADS) as pool:
            for result in tqdm(
                pool.imap_unordered(self._requester, self.socks_list),
                total=len(self.socks_list),
            ):
                results.append(result)
        return results

    @staticmethod
    def _save_socks(socks: str):
        with open("../socks_list/%s" % OUT_FILENAME, "a") as out_file:  ###
            out_file.write(socks + "\n")

    def run(self):
        check = ProxyChecker(self.socks_list)
        check.pool_requests()

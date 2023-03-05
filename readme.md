# SOCKS5 proxies scrapper

### Get socks5 proxies from:
* http://free-proxy.cz
* https://spys.one
* https://hidemy.name
* https://www.freeproxy.world
* https://www.proxy-list.download
* https://www.proxydocker.com
* https://www.vpnside.com
* https://premiumproxy.net
* https://proxylist.geonode.com

#### Аnd from public repositories that are updated frequently:
* https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
* https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt
* https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt
* https://raw.githubusercontent.com/baklazhan1337/proxier/main/socks5.txt
* https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt

### On some resources a content is dynamic. In this regard the webdriver (Firefox) is used
You can also use it without a webdriver to get a SOCKS5 proxy from resources without dynamic content.

To use the driver, you need to download `geckodriver` from ( https://github.com/mozilla/geckodriver/releases ) and put it in the `bin/`
And run with the -d flag:
```commandline
$ python main.py -d
```

Without using the Firefox webdriver:
```commandline
$ python main.py
```

After receiving the socks5 proxy list, the proxies are checked using HTTP requests (script `checker.py`).

The available socks5 proxies are stored in the `socks_list/` directory.

#### Good luck!
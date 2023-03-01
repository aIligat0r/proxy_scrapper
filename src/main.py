import scrapper
import checker


def main():
    socks5_list = scrapper.Socks5Scrapper().get_socks_list()
    checker.ProxyChecker(socks5_list).run()


if __name__ == '__main__':
    main()
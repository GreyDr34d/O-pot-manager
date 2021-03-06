#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :shodan.py
@Description :
@Date        :2021/04/20 18:56:59
@Author      :dr34d
@Version     :1.0
'''

import urllib

from configparser import ConfigParser
from manager.lib.core.log import logger
import requests


class Shodan():
    def __init__(self, conf_path, token=None):
        self.headers = None
        self.credits = 0
        self.conf_path = conf_path

        if self.conf_path:
            self.parser = ConfigParser()
            self.parser.read(self.conf_path)
            try:
                self.token = self.parser.get("Shodan", 'Token')
            except Exception:
                pass

        if token:
            self.token = token
        self.check_token()

    def token_is_available(self):
        if self.token:
            try:
                resp = requests.get(
                    'https://api.shodan.io/account/profile?key={0}'.format(
                        self.token))
                if resp and resp.status_code == 200 and "member" in resp.json(
                ):
                    return True
            except Exception as ex:
                logger.error(str(ex))
        return False

    def check_token(self):
        token_is_available = self.token_is_available()
        if token_is_available == True:
            return True
        else:
            new_token = input("Shodan API Token:")
            self.token = new_token
            if self.token_is_available():
                self.write_conf()
                return True
            else:
                logger.error("The shodan api token is incorrect. "
                             "Please enter the correct api token.")
                self.check_token()

    def write_conf(self):
        if not self.parser.has_section("Shodan"):
            self.parser.add_section("Shodan")
        try:
            self.parser.set("Shodan", "Token", self.token)
            self.parser.write(open(self.conf_path, "w"))
        except Exception as ex:
            logger.error(str(ex))

    def get_resource_info(self):
        if self.check_token():
            try:
                resp = requests.get(
                    'https://api.shodan.io/account/profile?key={0}'.format(
                        self.token))
                if resp and resp.status_code == 200 and 'credits' in resp.json(
                ):
                    content = resp.json()
                    self.credits = content['credits']
                    return True
            except Exception as ex:
                logger.error(str(ex))
        return False

    def search(self, dork, pages=1, resource='host'):
        search_result = set()
        try:
            for page in range(1, pages + 1):
                url = "https://api.shodan.io/shodan/{0}/search?key={1}&query={2}&page={3}".format(
                    resource, self.token, urllib.parse.quote(dork), page)
                resp = requests.get(url)
                if resp and resp.status_code == 200 and "total" in resp.json():
                    content = resp.json()
                    for match in content['matches']:
                        ans = match['domains'][0] if len(
                            match['domains']) > 0 else None
                        if ans:
                            search_result.add(ans)
                else:
                    logger.error("[PLUGIN] Shodan:{}".format(resp.text))
        except Exception as ex:
            logger.error(str(ex))
        return search_result


if __name__ == "__main__":
    sd = Shodan(conf_path="conf.rc", token="")
    search_result = sd.search('wordpress')
    print(search_result)

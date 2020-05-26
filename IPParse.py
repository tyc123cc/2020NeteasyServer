# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

class IPParse:
    def __init__(self,filename):
        DOMTree = xml.dom.minidom.parse(filename)
        self.collection = DOMTree.documentElement

    def getIPandPort(self):
        connect = self.collection.getElementsByTagName("connect")
        for item in connect:
            IP = item.getElementsByTagName('IP')[0]
            port = item.getElementsByTagName('port')[0]
        return str(IP.childNodes[0].data),int(port.childNodes[0].data)

if __name__ == '__main__':
    parse = IPParse("ConnectConf.xml")
    print parse.getIPandPort()
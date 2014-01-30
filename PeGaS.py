#! /usr/bin/env python

import urllib2, re, socket
from termcolor import colored

############Settings##################
proxy_list = []
log = 2 
time_out = 3
socket.setdefaulttimeout(time_out)

def open_url(get_url):
	header = urllib2.build_opener()
	header.addheaders = [('User-agent', 'Mozilla/7.0')]
	body = header.open(get_url)
	return body.read()


def reg_ip(text):
	p = re.compile('[\d]+\.[\d]+\.[\d]+\.[\d]+:[\d]+')
	if (p.findall(text) != []): 
		if (log == 2): print "ALL IP"
		return p.findall(text)
	else:   
		p = re.compile('[\d]+\.[\d]+\.[\d]+\.[\d]+')
		tmp = p.findall(text)
		all_=[]
		for ip in tmp:
			all_+=add_port(ip)
		print all_		
	return  all_

def proxy_bad(pip):
        try:
                proxy = urllib2.ProxyHandler({'http' : pip})
                opener = urllib2.build_opener(proxy)
                opener.addheaders = [('User-agent', 'Mozilla/7.0')]
                urllib2.install_opener(opener)
                req = urllib2.Request('http://2ip.ru')
                body = urllib2.urlopen(req)
                body.read()
#       except urllib2.HTTPError, e:
#               return e.code
        except Exception, detail:
                #print "ERROR:", detail
                return 1

def add_port(ip):
	tmp=[]
	return [ip+':80',ip+':8080',ip+':3128']


def proxy_good(pip):
	try:
                proxy = urllib2.ProxyHandler({'http' : pip})
                opener = urllib2.build_opener(proxy)
                opener.addheaders = [('User-agent', 'Mozilla/7.0')]
                urllib2.install_opener(opener)
                req = urllib2.Request("http://instagram.com/","a+")
                body = urllib2.urlopen(req)
#		print body.read(68),'<=================='
  		if (body.read(98) == '<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en" class="hl-en not-logged-in ">'):
			return pip
#       except urllib2.HTTPError, e:
#               return e.code
        except Exception, detail:
                #print "ERROR:", detail
                return 0


#scan=opener.open('http://spys.ru/free-proxy-list/VE/')
#p.findall(scan.read())



site_list = []

def create_site_list(file_name):
	rgx = re.compile(r'\n')
	#if test_url(rgx):
	return rgx.split(open(file_name).read())[:-1]


def create_ip_list(sites):
	proxy_list = []
	for site in sites:
		if (log >= 1): print "grab - ",site
		new_proxy = reg_ip(open_url(site)) 
		if (log == 2): print "added -  ",new_proxy
		proxy_list+=new_proxy
#	if (log == 2): print colored (proxy_list, "red")
	return proxy_list
		
def write_good(pip):
	head = open("good.txt", "a+")
	head.write(pip+"\n")

		
def tmp():
	header = urllib2.build_opener()
	header.addheaders = [('User-agent', 'Mozilla/7.0')]
	body = header.open("http://twitter.com","a+")
	#body.seek(10,6)
	#if (log): print body.read(128)
	#if (body.read(128) == '<!DOCTYPE html>\n<html data-nav-highlight-class-name=\"highlight-global-nav-home\">\n<head>\n\n<title>Twitter</title>'): print "ALL olrigth"
	#print '<!DOCTYPE html><html data-nav-highlight-class-name=\"highlight-global-nav-home\">'

def test_url(url):
	try:
		#tmp = 'http://'+url
                req = urllib2.Request(url,"a+")
                body = urllib2.urlopen(req)
		print  body.read(1),'<++++++++++'
		return 1
        except Exception, detail:
                print "ERROR:", detail
                return 0



	

def main():
	for ip in create_ip_list(create_site_list('site.txt')):
#		for pip in add_port(ip): 
#        		if (log): print "----------->",pip
#		if test_url(ip):
		if(proxy_good(ip)):
			write_good(ip)
			if (log >= 1): print colored("[+]", "red"), colored(ip, "green")
		else:
			if (log == 2): print colored ("[-]","grey"),colored (ip,"grey")
			pass

main()
#tmp()

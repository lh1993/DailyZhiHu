# -*- coding:utf-8 -*-

import urllib2, re, os
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

zhihu = open('zhihu.txt', 'wb')

# 获取网页源码
def getHtml(url):
    Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36'}
    request = urllib2.Request(url, headers=Headers)
    response = urllib2.urlopen(request)
    html = response.read()
    # print html
    return html

# 获取标题超链接
def getUrl(html):
    link = re.compile('<a href="/story/(.*?)"', re.S)
    items = re.findall(link, html)
    url = []
    for item in items:
        url.append("http://daily.zhihu.com/story/"+item)
        # print url[-1]
    return url

# 获取文章标题和内容
def getContext(url):
    html = getHtml(url)
    headline = re.compile('<h1 class="headline-title">(.*?)</h1>', re.S)
    items = re.findall(headline, html)
    #print '#####'+items[0]+'#####'
    for item in items:
        zhihu.write("#" * 5 + item + '#' * 5 + os.linesep)
        # print("#" * 5 + item + '#' * 5)

    content = re.compile('<div class="content">(.*?)</div>', re.S)
    items = re.findall(content, html)
    for item in items:
        for content in contentFiltrate(item):
            zhihu.write(content + os.linesep)
            # print content

# 去掉文章内容的标签
def contentFiltrate(content):
    htmlParser = HTMLParser.HTMLParser()
    pattern = re.compile('<p>(.*?)</p>|<li>(.*?)</li>.*?', re.S)
    items = re.findall(pattern, content)
    result = []
    for index in items:
        if index != '':
            for content in index:
                tag = re.search('<.*?>', content)
                http = re.search('<.*?http.*?>', content)
                html_tag = re.search('&', content)

                if html_tag:
                    content = htmlParser.unescape(content)

                if http:
                    continue
                elif tag:
                    pattern = re.compile('(.*?)<.*?>(.*?)</.*?>(.*?)')
                    items = re.findall(pattern, content)
                    content_tags = ''
                    if len(items) > 0:
                        for item in items:
                            if len(item) > 0:
                                for item_s in item:
                                    content_tags = content_tags + item_s
                            else:
                                content_tags = content_tags + item
                        content_tags = re.sub('<.*?>', '', content_tags)
                        result.append(content_tags)
                    else:
                        continue
                else:
                    result.append(content)
    return result

# 主函数
def main():
    url = "http://daily.zhihu.com/"
    # 获取主页的网页源代码
    html = getHtml(url)
    # 获取各个标题的超链接
    links = getUrl(html)
    # 获取各个标题名称及内容
    for link in links:
        try:
            getContext(link)
        except Exception, e:
            print e

if __name__ == "__main__":
    main()

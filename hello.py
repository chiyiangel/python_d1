import http.cookiejar
import urllib.request
import gzip
import csv
from bs4 import BeautifulSoup


def ungzip(data):
    try:  # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data


def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


if __name__ == '__main__':
    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.douban.com',
        'DNT': '1'
    }

    url = 'https://www.douban.com/'
    url += '/accounts/login'
    opener = getOpener(header)

    id = ''
    password = ''
    postDict = {
        'form_email': id,
        'form_password': password,
        'remember': 'y',
        'source': 'index_nav'
    }
    postData = urllib.parse.urlencode(postDict).encode()
    op = opener.open(url, postData)
    # data = op.read()
    # data = ungzip(data)

    movieUrl = "https://movie.douban.com/subject/25824686/comments?status=P"
    mop = opener.open(movieUrl)

    data = mop.read()
    data = ungzip(data)
    html = data.decode('utf-8')

    bsObj = BeautifulSoup(html, 'html.parser')
    commentList = bsObj.findAll('div', {'class': 'comment-item'})

    csvFile = open("./data/comment.csv", 'w+', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)

    try:
        for comment in commentList:
            name = comment.find('a').attrs['title']
            rateVote = comment.find('span', {'class': 'votes'}).getText()
            commentText = comment.find('p').getText()
            commentStr = '用户名：%s，赞同数：%s，影评：%s' % (name.strip(), rateVote.strip(), commentText.strip())
            writer.writerow((name.strip(), rateVote.strip(), commentText.strip()))
            print(commentStr)
    finally:
        csvFile.close()

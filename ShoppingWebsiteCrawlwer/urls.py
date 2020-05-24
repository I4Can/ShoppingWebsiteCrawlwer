def jd(start, end,keyword):
    for page in range(start, end + 1):
        yield 'https://search.jd.com/Search?keyword={}&page={}'.format(keyword,str(page))

def tm(start,end,keyword):
    for page in range(start, end + 1):
        yield "https://list.tmall.com/search_product.htm?q={}s={}".format(keyword,page*60-60)


def sn(start, end, keyword):
    for page in range(start, end + 1):
        yield "https://search.suning.com/emall/searchV1Product.do?keyword={}&cp={}&pg=01".format(keyword, page-1)


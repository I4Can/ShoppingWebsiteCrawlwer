# ShoppingWebsiteCrawler
基于关键字的配置化电商爬虫，目前已实现京东和苏宁（淘宝反爬太严重，因为没有使用selenium）

    京东爬取结果：
    {'_id': '8790cfd4-520e-4411-a7e0-7644ce8c3943',
    'coupons': ',discount=600||quota=3600||url=//coupon.jd.com/ilink/couponActiveFront/front_index.action?key=8e8f2f81cc084da7a2dd7f104f0df59d&roleId=31439358&to=https://pro.jd.com/mall/active/3vhrJRWUDvx84MMSPJ2gnMuggew3/index.html,https://pro.m.jd.com/mall/active/3vhrJRWUDvx84MMSPJ2gnMuggew3/index.html',
    'date': '2020-05-24',
    'highest_price': 6228.0,
    'id': '5089273;100003742879;100010822348;6084367;100004950981;5089271;100006299884;100006011521;6077902;5089275;100006299882;100006011519;6077930;100008710200;6077932;5089257;100003742933;100010822378;5089255;100006299866;100010822350;6084369;100004950977;6077904;5475612;100003742935;100010822384',
    'lowest_price': 3899.0,
    'name': 'Apple iPhone 8 Plus (A1864) 128GB 深空灰色 移动联通电信4G手机',
    'shop': 'Apple产品京东自营旗舰店',
    'type': 'AppleiPhone 8 Plus',
    'url': 'https://item.jd.com/100008710200.html'}
<br>

    苏宁爬取结果：
    {'_id': 'cfca4e87-13ca-4b24-af86-f02a0ddf49bc',
    'brand': '华为(HUAWEI)',
    'coupons': ',满3999用10,满999用5',
    'date': '2020-05-24',
    'highest_price': 7388.0,
    'id': '11765498415,11759001246,11768439312,11765504868,11765499805,11759001337,11768439753,11759037172,11768439861,11765499292,11765498415,11759037273,11768440086,11787914135,11768438948,11765499596,11765499758,11765499656,11768439990,11759036941,11768438454,11765499397,11765498941,11759001441,11768439472,11759037104,11768438656,11765499531,11765499038,11759037227,11768439606',
    'img': '//imgservice.suning.cn/uimg1/b2c/image/E5gOdgOUiKPaODfNGSc9CQ.jpg_800w_800h_4e',
    'lowest_price': 4188.0,
    'name': '华为(HUAWEI)P40 Pro 5G 8GB+256GB 亮黑色 移动联通电信全网通5G手机',
    'shop': ' 天环云手机数码官方旗舰店',
    'type': 'P40 Pro 5G',
    'url': 'https://product.suning.com/0070142956/11765498415.html?safp=d488778a.SFS_10185344.16146068.2&safc=prd.0.0&safpn=10010'}

实现了API接口

* 传入京东或苏宁商品详情url，返回如上所示商品信息，格式->[item]

* 传入关键字和要爬取的个数，得到京东、苏宁推荐的前item_num个数商品，格式->[item1,item2,...,itemN]

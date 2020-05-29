from crawler_api import search_with_url_or_keyword

args = [("https://item.m.jd.com/product/100011336064.html?pps=reclike.FO4O305:FOFO004923E184O13O6:016DEDF44BDDAEEFO0400416O8C3O1FO3O643O7FFF5021813FO7O174923E1806055A6C358E9206D",None),
          ("https://item.jd.com/68330992891.html", None),
          ("https://product.suning.com/0000000000/11110814038.html?srcpoint=pindao_wjpdy_102017315244_prod02&safp=d488778a.wjpdy.102017315244.2&safc=prd.0.0",None),
          ("https://m.suning.com/product/0070214121/000000010702327599.html?safp=f73ee1cf.wapindex7.113464229882.3&safc=prd.1.rec_25-56_25-56_204_sys%3Arec,inpo%3A0,cpn%3A0,p%3A14-41,uuid%3Aacecdbb8191ec71728e9b94a9f364785,d%3A1,ab%3AH,dab%3A5-5_A&safpn=10001",None),
          ("手机",3),
          ("鞋子",2),
          ("https://item.taobao.com/item.htm?spm=a217m.12005862.1223185.2.2ddf1296YjHNEB&id=606930801180"),
          ("",None),
          ("电脑",0),
          "电脑", "???"]
if __name__ == "__main__":
    for i,arg in enumerate(args):
        try:
            r=search_with_url_or_keyword(*arg)
        except Exception as e:
            print(e)
            continue
        print("r"+str(i),":",r,"\n")

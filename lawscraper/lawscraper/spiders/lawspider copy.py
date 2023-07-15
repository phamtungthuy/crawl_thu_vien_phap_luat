import scrapy
from pathlib import Path
from lawscraper.items import LawItem
import os


class LawspiderSpider(scrapy.Spider):
    name = "lawspider2"
    allowed_domains = ["thuvienphapluat.vn"]
    start_page = 1
    end_page = 15262
    max_page = 15262
    error = 0
    max_error = 50
    def haveSomeFilesNotExist(self, current_page):
        for i in range(20):
            if not os.path.exists(f"./summary/page{(current_page - 1) * 20 + i + 1}.html"):
                return True
        return False
    
    
    def start_requests(self):
        url = "https://thuvienphapluat.vn/page/tim-van-ban.aspx?keyword=&area=0&match=True&type=0&status=0&signer=0&sort=6&lan=1&scan=0&org=0&fields="
        count = 0
        for i in range(self.start_page, self.end_page+1):
            # if self.error > self.max_error:
            #     break
            if self.haveSomeFilesNotExist(i):
                count += 1
                yield scrapy.Request(url=f"{url}&page={i}", callback=self.parse2,
                                    meta={
                                        # "proxy": "http://phamtungthuy-rotate:tungthuy47@p.webshare.io:80",
                                        "current_page": i 
                                    })
        if count == 0:
            print("-------------------------Nothing to do------------------------")
    
    def parse2(self, respose):
        if response.url.find('checkvb.aspx') != -1:
            self.error += 1
            return
    def parse(self, response):
        if response.url.find('checkvb.aspx') != -1:
            self.error += 1
            return

        
        laws = response.css('p.nqTitle')
        
        for i in range(len(laws)):
            page_id = (response.meta.get("current_page") - 1) * 20 + i + 1
            # if self.error >= self.max_error:
            #     raise scrapy.exceptions.CloseSpider(reason='Maximum error count reached.')
            if not os.path.exists(f"./data/page{page_id}.html"):
                law = laws[i]
                law_url = law.css("a ::attr('href')").get()
                yield response.follow(law_url, callback = self.parse_law_page,
                                    meta={
                                        # "proxy": "http://phamtungthuy-rotate:tungthuy47@p.webshare.io:80",
                                        "page_id": page_id
                                  })
    
    def parse_law_page(self, response):
        if response.url.find('checkvb.aspx') != -1:
            self.error += 1
            return
        page_id = response.meta.get("page_id")
        filename = f"./data/page{page_id}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        # self.current_page_id +=1 


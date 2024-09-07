import csv

import scrapy


class AmazonDataSpider(scrapy.Spider):
    name = "amazon_data"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'session-id=132-1691153-3524911; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; ubid-main=130-5160799-3455460; JSESSIONID=B9D4C03382C1A9D14CD1FD132BB17899; session-token=4MctdfTryfN9SCSQaEYGbOedTsHob8Js7TK3aJDjkgX/wJxJNx/Oux3o4rwO46hX7K2WjlSCG27+K/86I4COPfyJoG9RIMn4SMAYakwayrp8jIZsTzbqbAcwb/UlzCxSJPb0HuWEYR5GgdlN7tnHaxEV5tkv90PpwKh6ItXWaHcB8io3VlOsUZI/tNdxwOrHjkxOK0xe1EMdDhKQKJfyz3nVpU9NvM37wvr99JYlgxiYjT8qasDqMJStBRJ6Aj8hxY8RtxreFK7oaowyZ5kQnE4ID1TEoBse+xtV1HJfmEPAr2bLpvABV6OV0ssh20oJEyoW5WoaUK7gQySgFgJms+vFEvenZLP0; csm-hit=tb:M356GWHMEV3B2DT04MWP+s-6M2C3VJ7WXT9SRDEKKVJ|1725690479829&t:1725690479829&adb:adblk_no',
        'device-memory': '8',
        'downlink': '9.95',
        'dpr': '1',
        'ect': '4g',
        'priority': 'u=0, i',
        'rtt': '300',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1366',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'viewport-width': '1366',
    }

    cookies = {
        'session-id': '132-1691153-3524911',
        'session-id-time': '2082787201l',
        'i18n-prefs': 'USD',
        'skin': 'noskin',
        'ubid-main': '130-5160799-3455460',
        'JSESSIONID': 'B9D4C03382C1A9D14CD1FD132BB17899',
        'session-token': '4MctdfTryfN9SCSQaEYGbOedTsHob8Js7TK3aJDjkgX/wJxJNx/Oux3o4rwO46hX7K2WjlSCG27+K/86I4COPfyJoG9RIMn4SMAYakwayrp8jIZsTzbqbAcwb/UlzCxSJPb0HuWEYR5GgdlN7tnHaxEV5tkv90PpwKh6ItXWaHcB8io3VlOsUZI/tNdxwOrHjkxOK0xe1EMdDhKQKJfyz3nVpU9NvM37wvr99JYlgxiYjT8qasDqMJStBRJ6Aj8hxY8RtxreFK7oaowyZ5kQnE4ID1TEoBse+xtV1HJfmEPAr2bLpvABV6OV0ssh20oJEyoW5WoaUK7gQySgFgJms+vFEvenZLP0',
        'csm-hit': 'tb:M356GWHMEV3B2DT04MWP+s-6M2C3VJ7WXT9SRDEKKVJ|1725690479829&t:1725690479829&adb:adblk_no',
    }

    def read_file(self, file):
        with open(f'input/{file}.csv')as file:
            data=list(csv.DictReader(file))
            return data



    def start_requests(self):
        input_file= 'AMZN US_Top_Search_Terms (Aug 2024)'
        input_file= 'keywords'
        input_File_Data=self.read_file(input_file)
        for each_row in input_File_Data:
            term= each_row.get('Search Term').lower().strip()
            url=f'https://www.amazon.com/s?k={term}'
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse,)

        # url='https://www.amazon.com/s?k=ipod'
        # yield scrapy.Request(url=url, headers=self.headers, callback=self.parse,)

    def parse(self, response):
        item= dict()
        divs= response.xpath('//div[@data-component-type="s-search-result"]')
        for each_div in divs[:]:

            ProductName = each_div.xpath('.//h2//span/text()').get('').strip()
            ASIN= each_div.xpath('.//@data-asin').get('').strip()
            Rating= each_div.xpath("//span[contains(@aria-label,'stars')]").get('').strip()
            NoOfReviews= each_div.xpath(".//span[contains(@aria-label,'ratings')]").get('').strip().replace('ratings','')
            url_suffix = each_div.xpath(".//h2//a/@href").get('')
            URL = f'https://www.amazon.com{url_suffix}' if url_suffix else ''
            Price= each_div.xpath(".//span[@class='a-price']//span[@class='a-offscreen']/text()").get('').strip()
            SaveCoupon= each_div.xpath(".//span[@class='s-coupon-unclipped']/span[1]/text()").get('').strip().replace('Save','').strip()

            ViewPortWidth='1291'
            ViewPortHeight ='826'

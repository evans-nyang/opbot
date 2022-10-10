# import datetime

# import scrapy


# class CopiaSpider(scrapy.Spider):
#     name = 'copia'
#     start_urls = ['https://copia.co.ke/product-category/all/saleable/foodstuff/cooking-oils/']

#     def parse(self, response):
#         """
#             Find metadata information and add to dictionary
#             Args: 
#               response(dict): product id as a dictionary item
#             Returns: 
#               dict: nested dictionaries with indices
#             Raises:
#             Notes:
#               See https://docs.scrapy.org/en/latest/
#               and https://copia.co.ke/product-category/all/saleable/foodstuff/cooking-oils/
#               for more info
#         """
#         try:
#             print("Trying to fetch items from copia...")
#             articles = response.xpath("/html/body/div[2]/main/div/div[2]/div/div[2]/div")
#             newdata = {}
#             for i, art in enumerate(articles):
#                 if i < 200:
#                     newdata.update({i: self.parse_result(art)})
#             yield newdata
#         except Exception as err:
#             print("Encountered an exception during execution")
#             raise err
#         else:
#             print("Done successfully")

#     def parse_result(self, art) -> dict:
#         """
#             update crawling time, product id and name in dictionary
#             Args: 
#               response(dict): a nested dictionary 
#             Returns: 
#               dict: dictionaries comprising productid and crawling time
#         """
#         data = {}
#         mainn = art.xpath(".//div[@class='col-inner']")

#         data["crawledAt"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
#         data["productId"] = self.__safe_parsing(mainn.xpath(".//div[@class='product-small box']/div[2][@class='box-text box-text-products']/text()").get())

#         return data

#     def __safe_parsing(self, parsing) -> str:
#         """
#             assert if parsing object is of type str, extract str from selector item if not
#             Args:
#               parsing(str): article from the crawler
#             Returns:
#               str: data from tag as a string
#               Raises:
#               valueError: if instance is not str or Selector
#         """
#         try:
#             if isinstance(parsing, str):
#                 return parsing
#             elif isinstance(parsing, scrapy.Selector):
#                 parsing.get()
#         except Exception:
#             return None

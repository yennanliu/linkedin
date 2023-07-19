from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from linkedin.integrations.linkedin_api import extract_profile_id
from linkedin.integrations.selenium import get_by_xpath_or_none

"""
Variable holding where to search for first profiles to scrape.
"""
NETWORK_URL = "https://www.linkedin.com/mynetwork/invite-connect/connections/"


class RandomSpider(CrawlSpider):
    name = "random"
    allowed_domains = ("linkedin.com",)
    start_urls = [
        NETWORK_URL,
    ]

    rules = (
        # Extract links matching a single user
        Rule(
            LinkExtractor(
                allow=("https:\/\/.*\/in\/\w*\/$",),
                deny=("https:\/\/.*\/in\/edit\/.*",),
            ),
            callback=extract_profile_id,
            follow=True,
        ),
    )

    def wait_page_completion(self, driver):
        """
        Abstract function, used to customize how the specific spider have to wait for page completion.
        Blank by default
        :param driver:
        :return:
        """
        # waiting links to other users are shown so the crawl can continue
        get_by_xpath_or_none(driver, "//*[@id='global-nav']/div", wait_timeout=5)
        get_by_xpath_or_none(
            driver, "//*/li[contains(@class, 'mn-connection-card')]", wait_timeout=3
        )

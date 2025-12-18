"""
Intelligence-focused crawler for AI module enhancement
"""
import requests
from bs4 import BeautifulSoup
import time
from loguru import logger

class IntelligenceCrawler:
    def __init__(self, sources=None):
        self.sources = sources or [
            "https://cve.mitre.org/cve/data_feeds.html",
            "https://attack.mitre.org/",
            "https://www.alienvault.com/open-threat-exchange",
            "https://threatpost.com/category/vulnerabilities/"
        ]
        self.session = requests.Session()
        logger.info("Intelligence Crawler initialized")
    
    def start_crawling(self, intel_queue, bounty_queue, lesson_queue):
        """Main crawling loop for intelligence gathering"""
        logger.info("Intelligence crawler started")
        while True:
            for source in self.sources:
                try:
                    data = self.crawl_source(source)
                    intel_queue.put(data)
                    logger.info(f"Crawled: {source} - {len(data.get('items', []))} items")
                except Exception as e:
                    logger.error(f"Failed to crawl {source}: {e}")
                time.sleep(30)  # Be respectful
    
    def crawl_source(self, url):
        """Crawl specific intelligence source"""
        response = self.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract intelligence data (customize per source)
        items = []
        for link in soup.find_all('a', href=True):
            if any(keyword in link.text.lower() for keyword in ['cve', 'vulnerability', 'exploit', 'threat']):
                items.append({
                    'title': link.text.strip(),
                    'url': link['href'],
                    'source': url,
                    'timestamp': time.time()
                })
        
        return {
            'type': 'intelligence',
            'source': url,
            'items': items[:20],  # Limit to 20 items per source
            'crawled_at': datetime.now().isoformat()
        }

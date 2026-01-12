"""
Bug bounty program vulnerability crawler
"""
import requests
import json
from loguru import logger

class BountyCrawler:
    def __init__(self):
        self.bounty_sources = [
            "https://hackerone.com/bug-bounty-programs",
            "https://www.openbugbounty.org/feed/",
            "https://cve.mitre.org/cve/data_feeds.html"
        ]
        self.vulnerabilities = []
        logger.info("Bounty Crawler initialized")
    
    def start_crawling(self, intel_queue, bounty_queue, lesson_queue):
        """Crawl for bug bounty and vulnerability data"""
        logger.info("Bounty crawler started")
        while True:
            for source in self.bounty_sources:
                try:
                    vulns = self.crawl_vulnerabilities(source)
                    for vuln in vulns:
                        bounty_queue.put({
                            'type': 'vulnerability',
                            'source': source,
                            'vulnerability': vuln,
                            'bounty_potential': self.assess_bounty_value(vuln),
                            'disclosure_date': datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.error(f"Failed to crawl {source}: {e}")
                time.sleep(45)
    
    def crawl_vulnerabilities(self, url):
        """Crawl specific vulnerability sources"""
        vulns = []
        
        if 'hackerone' in url:
            # Parse HackerOne programs
            vulns.extend(self.parse_hackerone(url))
        elif 'openbugbounty' in url:
            # Parse OpenBugBounty feed
            vulns.extend(self.parse_openbugbounty(url))
        
        return vulns
    
    def assess_bounty_value(self, vulnerability):
        """Assess potential bounty value"""
        score = 0
        if 'critical' in vulnerability.get('severity', '').lower():
            score += 1000
        if 'remote' in vulnerability.get('type', '').lower():
            score += 500
        if 'code execution' in vulnerability.get('impact', '').lower():
            score += 1500
        
        return min(score, 5000)  # Cap at $5000 for estimation

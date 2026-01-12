#!/usr/bin/env python3
"""
OMEGA Web Crawler System
Implements surface, deep, and dark web crawling for threat intelligence
"""

import json
import time
import random
import hashlib
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
from queue import Queue, PriorityQueue
from urllib.parse import urlparse


class WebLayer(Enum):
    """Web layers for crawling"""
    SURFACE = "surface"      # Standard web, accessible via search engines
    DEEP = "deep"            # Dynamic content, requires interaction
    DARK = "dark"            # Onion services, requires Tor
    THREAT_INTEL = "threat_intel"  # Threat intelligence feeds


class CrawlerType(Enum):
    """Types of crawlers"""
    IOC_HARVESTER = "ioc_harvester"      # Extracts IOCs
    THREAT_MONITOR = "threat_monitor"    # Monitors for threats
    DATA_MINER = "data_miner"            # Extracts structured data


class IOCType(Enum):
    """Types of Indicators of Compromise"""
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"


class WebCrawler:
    """Base web crawler class"""
    
    def __init__(self, crawler_id: str, crawler_type: CrawlerType, 
                 web_layer: WebLayer, max_depth: int = 3):
        self.crawler_id = crawler_id
        self.crawler_type = crawler_type
        self.web_layer = web_layer
        self.max_depth = max_depth
        self.visited_urls: Set[str] = set()
        self.iocs_found: List[Dict[str, Any]] = []
        self.status = "IDLE"
        self.stats = {
            "urls_crawled": 0,
            "iocs_found": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat()
        }
    
    def crawl(self, start_urls: List[str]) -> List[Dict[str, Any]]:
        """Start crawling from given URLs"""
        self.status = "CRAWLING"
        print(f"🕸️ {self.crawler_id}: Starting crawl on {self.web_layer.value} layer")
        
        # Simulate crawling
        iocs = []
        for url in start_urls[:3]:  # Limit for simulation
            time.sleep(0.5)
            found_iocs = self._extract_iocs_from_url(url)
            if found_iocs:
                iocs.extend(found_iocs)
                self.iocs_found.extend(found_iocs)
            
            self.visited_urls.add(url)
            self.stats["urls_crawled"] += 1
            self.stats["iocs_found"] += len(found_iocs)
        
        self.status = "COMPLETED"
        print(f"✅ {self.crawler_id}: Crawl completed")
        
        return iocs
    
    def _extract_iocs_from_url(self, url: str) -> List[Dict[str, Any]]:
        """Extract IOCs from URL content (simulated)"""
        iocs = []
        
        # Simulate finding IOCs
        for i in range(random.randint(1, 3)):
            ioc_type = random.choice(list(IOCType))
            
            ioc = {
                "id": f"IOC-{hashlib.md5(f'{url}-{i}'.encode()).hexdigest()[:8]}",
                "type": ioc_type.value,
                "value": self._generate_ioc_value(ioc_type),
                "source_url": url,
                "layer": self.web_layer.value,
                "crawler_id": self.crawler_id,
                "confidence": random.randint(60, 95),
                "timestamp": datetime.now().isoformat()
            }
            
            iocs.append(ioc)
        
        return iocs
    
    def _generate_ioc_value(self, ioc_type: IOCType) -> str:
        """Generate a simulated IOC value"""
        if ioc_type == IOCType.IP_ADDRESS:
            return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        elif ioc_type == IOCType.DOMAIN:
            domains = ["malicious-example.com", "phishingsite.net"]
            return random.choice(domains)
        elif ioc_type == IOCType.URL:
            return f"https://{random.choice(['evil', 'malware'])}.com/payload.exe"
        else:  # HASH
            return hashlib.md5(str(time.time()).encode()).hexdigest()


class CrawlerOrchestrator:
    """Orchestrates multiple crawlers"""
    
    def __init__(self, orchestrator_id: str = "CRAWLER-ORCH-01"):
        self.orchestrator_id = orchestrator_id
        self.crawlers: Dict[str, WebCrawler] = {}
    
    def deploy_crawler(self, crawler_id: str, crawler_type: CrawlerType, 
                       web_layer: WebLayer) -> WebCrawler:
        """Deploy a new crawler"""
        crawler = WebCrawler(crawler_id, crawler_type, web_layer)
        self.crawlers[crawler_id] = crawler
        print(f"🚀 Deployed {crawler_id} for {web_layer.value} layer")
        return crawler
    
    def execute_crawl(self, crawler_id: str, start_urls: List[str]) -> List[Dict[str, Any]]:
        """Execute a crawl"""
        if crawler_id not in self.crawlers:
            print(f"⚠️ Crawler {crawler_id} not found")
            return []
        
        return self.crawlers[crawler_id].crawl(start_urls)


def test_web_crawler_system():
    """Test the web crawler system"""
    print("\n" + "="*60)
    print("🕸️ TESTING OMEGA WEB CRAWLER SYSTEM")
    print("="*60)
    
    # Create orchestrator
    orchestrator = CrawlerOrchestrator("OMEGA-CRAWLER-MAIN")
    
    # Deploy crawlers
    print("\n1. Deploying crawlers...")
    
    crawler1 = orchestrator.deploy_crawler(
        "SURFACE-CRAWLER-001",
        CrawlerType.IOC_HARVESTER,
        WebLayer.SURFACE
    )
    
    crawler2 = orchestrator.deploy_crawler(
        "THREAT-INTEL-CRAWLER-001",
        CrawlerType.THREAT_MONITOR,
        WebLayer.THREAT_INTEL
    )
    
    # Execute crawls
    print("\n2. Executing crawls...")
    
    surface_urls = ["https://threatintel.example.com", "https://cybersecuritynews.com"]
    iocs1 = orchestrator.execute_crawl("SURFACE-CRAWLER-001", surface_urls)
    
    threat_urls = ["https://otx.alienvault.com/api/v1/pulses/subscribed"]
    iocs2 = orchestrator.execute_crawl("THREAT-INTEL-CRAWLER-001", threat_urls)
    
    # Display results
    print("\n3. Results:")
    all_iocs = iocs1 + iocs2
    print(f"   Total IOCs collected: {len(all_iocs)}")
    
    for i, ioc in enumerate(all_iocs[:3]):
        print(f"   {i+1}. [{ioc.get('layer')}] {ioc.get('type')}: {ioc.get('value')}")
    
    print("\n" + "="*60)
    print("✅ WEB CRAWLER SYSTEM TEST COMPLETE")
    print("="*60)
    
    return True


if __name__ == "__main__":
    print("🕸️ OMEGA WEB CRAWLER SYSTEM")
    print("="*60)
    test_web_crawler_system()

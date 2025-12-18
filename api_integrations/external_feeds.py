"""
JAIDA API Integration Service - Real-time data from security feeds.
"""
import os
import requests
import json
from datetime import datetime
from loguru import logger

class ExternalFeedIntegrator:
    def __init__(self):
        self.feeds = {
            'alienvault_otx': {
                'url': 'https://otx.alienvault.com/api/v1/pulses/subscribed',
                'headers': {'X-OTX-API-KEY': os.getenv('OTX_KEY', '')}
            },
            'mitre_attack': {
                'url': 'https://cti-taxii.mitre.org/taxii/',
                'auth': (os.getenv('TAXII_USER', ''), os.getenv('TAXII_PASS', ''))
            }
        }
        logger.info("External Feed Integrator initialized")

    def fetch_otx_pulses(self):
        """Fetch recent threat pulses from AlienVault OTX."""
        config = self.feeds['alienvault_otx']
        if not config['headers']['X-OTX-API-KEY']:
            logger.warning("OTX_KEY not set. Get free key at https://otx.alienvault.com")
            return []

        try:
            response = requests.get(config['url'], headers=config['headers'], timeout=30)
            if response.status_code == 200:
                pulses = response.json().get('results', [])[:5]  # Get 5 most recent
                logger.info(f"Fetched {len(pulses)} pulses from OTX")
                return self._normalize_otx_data(pulses)
        except Exception as e:
            logger.error(f"Failed to fetch OTX: {e}")
        return []

    def _normalize_otx_data(self, pulses):
        """Convert OTX pulses to JAIDA common format."""
        normalized = []
        for pulse in pulses:
            normalized.append({
                "jaida_id": f"OTX_{pulse.get('id', 'unknown')}",
                "title": pulse.get('name', 'No title'),
                "description": pulse.get('description', '')[:200],
                "indicators": pulse.get('indicators', []),
                "source": "alienvault_otx",
                "ingestion_time": datetime.now().isoformat(),
                "raw_data": pulse  # Keep original for reference
            })
        return normalized

    def test_integration(self):
        """Test all configured feeds."""
        results = {}
        for feed_name in self.feeds:
            if feed_name == 'alienvault_otx':
                results[feed_name] = self.fetch_otx_pulses()
        return results

if __name__ == "__main__":
    print("[*] Testing JAIDA API Integrations...")
    integrator = ExternalFeedIntegrator()

    # Test with OTX (will work if OTX_KEY env var is set)
    test_results = integrator.test_integration()

    for feed, data in test_results.items():
        print(f"\n📡 {feed.upper()}: {len(data)} items fetched")
        if data:
            print(f"Sample: {data[0]['title'][:50]}...")

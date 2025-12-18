"""
JAIDA Multi-Agent Crawler Orchestrator
Coordinates specialized crawlers for intelligence, lessons, and bug bounty
"""
import threading
import queue
import json
from datetime import datetime
from loguru import logger

class JAIDACrawlerOrchestrator:
    def __init__(self):
        self.crawlers = {}
        self.intel_queue = queue.Queue()
        self.bounty_queue = queue.Queue()
        self.lesson_queue = queue.Queue()
        self.active = False
        logger.info("JAIDA Crawler Orchestrator initialized")
    
    def register_crawler(self, name, crawler_instance):
        """Register specialized crawler agents"""
        self.crawlers[name] = crawler_instance
        logger.info(f"Registered crawler: {name}")
    
    def start_all(self):
        """Start all registered crawlers in separate threads"""
        self.active = True
        for name, crawler in self.crawlers.items():
            thread = threading.Thread(
                target=crawler.start_crawling,
                args=(self.intel_queue, self.bounty_queue, self.lesson_queue),
                daemon=True,
                name=f"crawler_{name}"
            )
            thread.start()
            logger.info(f"Started crawler thread: {name}")
        return True
    
    def monitor_queues(self):
        """Monitor and process data from crawler queues"""
        while self.active:
            # Process intelligence data
            if not self.intel_queue.empty():
                intel = self.intel_queue.get()
                self.process_intelligence(intel)
            
            # Process bounty data
            if not self.bounty_queue.empty():
                bounty = self.bounty_queue.get()
                self.process_bounty(bounty)
            
            # Process lesson data
            if not self.lesson_queue.empty():
                lesson = self.lesson_queue.get()
                self.process_lesson(lesson)
    
    def process_intelligence(self, data):
        """Process raw intelligence for AI module"""
        logger.info(f"Processing intelligence: {data.get('type', 'unknown')}")
        # Save to AI training data
        with open('intelligence_database.json', 'a') as f:
            f.write(json.dumps(data) + '\n')
        return True

# Singleton orchestrator
ORCHESTRATOR = JAIDACrawlerOrchestrator()

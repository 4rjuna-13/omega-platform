"""
Crawler management and coordination
"""
from crawler_orchestrator import ORCHESTRATOR
from intelligence_crawler import IntelligenceCrawler
from lesson_crawler import LessonCrawler
from bounty_crawler import BountyCrawler
import threading

def setup_crawlers():
    """Setup all crawler agents"""
    # Initialize crawlers
    intel_crawler = IntelligenceCrawler()
    lesson_crawler = LessonCrawler()
    bounty_crawler = BountyCrawler()
    
    # Register crawlers
    ORCHESTRATOR.register_crawler('intelligence', intel_crawler)
    ORCHESTRATOR.register_crawler('lessons', lesson_crawler)
    ORCHESTRATOR.register_crawler('bounty', bounty_crawler)
    
    return ORCHESTRATOR

def start_crawler_system():
    """Start the complete crawler system"""
    orchestrator = setup_crawlers()
    
    # Start crawlers
    orchestrator.start_all()
    
    # Start queue monitoring in separate thread
    monitor_thread = threading.Thread(
        target=orchestrator.monitor_queues,
        daemon=True,
        name="queue_monitor"
    )
    monitor_thread.start()
    
    print("✅ JAIDA Multi-Agent Crawler System Started")
    print(f"📊 Active Crawlers: {len(orchestrator.crawlers)}")
    print("🔍 Monitoring: Intelligence, Lessons, Bug Bounty")
    
    return orchestrator

if __name__ == "__main__":
    start_crawler_system()
    # Keep main thread alive
    import time
    while True:
        time.sleep(60)

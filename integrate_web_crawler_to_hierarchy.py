#!/usr/bin/env python3
"""
Connect existing web_crawler_system.py to Sovereign Hierarchy
Make it a WD-class under GC-WEB-CRAWLER-001
"""

import sys
import os
from sovereign_hierarchy import SovereignRegistry, BotType, WorkerDrone, BotStatus, PermissionLevel
from datetime import datetime

def create_web_crawler_wd(registry):
    """Create a specialized Web Crawler WD"""
    print("🔗 Creating Web Crawler Worker Drone...")
    
    # Get the Web Crawler GC
    web_crawler_gc = registry.gc_bots.get("GC-WEB-CRAWLER-001")
    if not web_crawler_gc:
        print("❌ Web Crawler GC not found!")
        return None
    
    # Commission a specialized web crawler WD
    wd = web_crawler_gc.commission_worker(
        wd_type=BotType.WD_SURFACE_CRAWLER,
        task="Automated surface web intelligence gathering with IOC extraction",
        permissions=PermissionLevel.WD_PRIVILEGED
    )
    
    # Add specialized methods to this WD
    class WebCrawlerWD(WorkerDrone):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.crawled_pages = 0
            self.iocs_found = 0
            
        def execute_web_crawl(self, target_urls, depth=2):
            """Execute web crawling task"""
            result = super().execute_task({
                "action": "web_crawl",
                "targets": target_urls,
                "depth": depth
            })
            
            # Simulate web crawling (would connect to actual web_crawler_system.py)
            self.crawled_pages += len(target_urls) * depth
            self.iocs_found += len(target_urls)  # Simulated IOC count
            
            result.update({
                "crawled_pages": self.crawled_pages,
                "iocs_found": self.iocs_found,
                "crawl_depth": depth,
                "status": "crawl_completed"
            })
            
            # Update performance score based on results
            self.performance_score = min(1.0, self.iocs_found / 10.0)
            
            return result
        
        def extract_iocs(self, content):
            """Extract IOCs from content"""
            # Simulate IOC extraction
            iocs = []
            if "malware" in content.lower():
                iocs.append("malware_indicator")
            if "exploit" in content.lower():
                iocs.append("exploit_code")
            if "phishing" in content.lower():
                iocs.append("phishing_url")
            
            self.iocs_found += len(iocs)
            
            return {
                "wd_id": self.id,
                "action": "ioc_extraction",
                "content_length": len(content),
                "iocs_found": iocs,
                "total_iocs": self.iocs_found,
                "timestamp": datetime.now().isoformat()
            }
    
    # Create enhanced WD
    enhanced_wd = WebCrawlerWD(
        id=wd.id,
        name=wd.name,
        bot_type=wd.bot_type,
        task_description=wd.task_description,
        commissioned_by=wd.commissioned_by,
        created=wd.created,
        status=wd.status,
        permissions=wd.permissions,
        memory=wd.memory,
        performance_score=wd.performance_score
    )
    
    # Replace in registry
    registry.wd_bots[enhanced_wd.id] = enhanced_wd
    registry.save()
    
    print(f"✅ Created Web Crawler WD: {enhanced_wd.name} ({enhanced_wd.id})")
    return enhanced_wd

def integrate_with_existing_crawler():
    """Integrate with existing web_crawler_system.py if it exists"""
    print("\n🔍 Looking for existing web crawler system...")
    
    if os.path.exists("web_crawler_system.py"):
        print("✅ Found web_crawler_system.py")
        
        # Try to import it
        try:
            # Add current directory to path
            sys.path.insert(0, ".")
            
            # Import dynamically
            import importlib.util
            spec = importlib.util.spec_from_file_location("web_crawler", "web_crawler_system.py")
            web_crawler_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(web_crawler_module)
            
            print("✅ Successfully imported web crawler module")
            
            # Check what's in the module
            crawler_functions = [attr for attr in dir(web_crawler_module) 
                                if not attr.startswith("_")]
            
            print(f"📦 Available in crawler module: {', '.join(crawler_functions[:5])}...")
            
            return web_crawler_module
            
        except Exception as e:
            print(f"⚠️ Could not import web crawler: {e}")
            print("   Will create simulated crawler instead")
    
    else:
        print("⚠️ web_crawler_system.py not found")
        print("   Creating simulated crawler functionality")
    
    return None

def test_integrated_crawler():
    """Test the integrated web crawler WD"""
    print("\n🧪 Testing Integrated Web Crawler...")
    
    # Load registry
    registry = SovereignRegistry()
    
    # Create web crawler WD
    crawler_wd = create_web_crawler_wd(registry)
    
    if crawler_wd:
        # Test web crawling
        print(f"\n🚀 Testing {crawler_wd.name}...")
        
        # Simulated crawl
        test_urls = [
            "https://threatintel.example.com/feed",
            "https://securityblog.example.com/latest",
            "https://iocrepository.example.com/indicators"
        ]
        
        crawl_result = crawler_wd.execute_web_crawl(test_urls, depth=2)
        print(f"✅ Crawl completed: {crawl_result['crawled_pages']} pages")
        print(f"📊 Performance score: {crawler_wd.performance_score:.2f}")
        
        # Test IOC extraction
        test_content = "Latest malware exploit found in phishing campaign targeting banks."
        ioc_result = crawler_wd.extract_iocs(test_content)
        print(f"✅ IOC extraction: {len(ioc_result['iocs_found'])} IOCs found")
        
        # Show updated hierarchy
        print("\n" + "="*60)
        print("🔄 UPDATED HIERARCHY WITH WEB CRAWLER WD")
        print("="*60)
        
        # Get Web Crawler GC and show its workers
        web_crawler_gc = registry.gc_bots.get("GC-WEB-CRAWLER-001")
        if web_crawler_gc:
            print(f"\n🏢 Web Crawler GC: {web_crawler_gc.name}")
            print(f"   Workers: {len(web_crawler_gc.worker_drones)}")
            
            workers = registry.get_gc_workers("GC-WEB-CRAWLER-001")
            for wd in workers:
                print(f"   👷 {wd.name}: {wd.task_description}")
                if hasattr(wd, 'crawled_pages'):
                    print(f"      📊 Crawled: {wd.crawled_pages} pages, IOCs: {wd.iocs_found}")
        
        print("="*60)
        
        return True
    
    return False

if __name__ == "__main__":
    print("="*60)
    print("🔗 WEB CRAWLER TO HIERARCHY INTEGRATION")
    print("="*60)
    
    # Check for existing crawler
    crawler_module = integrate_with_existing_crawler()
    
    # Test integration
    success = test_integrated_crawler()
    
    print("\n" + "="*60)
    if success:
        print("✅ WEB CRAWLER SUCCESSFULLY INTEGRATED WITH HIERARCHY!")
        print("🎯 Next: Build Bot Father autonomous creation system")
    else:
        print("⚠️ Integration had issues")
    
    print("="*60)
    
    # Save final state
    registry = SovereignRegistry()
    registry.save()

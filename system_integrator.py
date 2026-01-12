"""
JAIDA Complete System Integrator
Connects crawlers, bug bounty, and Kali tools into unified platform
"""
from crawlers.manage_crawlers import start_crawler_system
from bug_bounty.bounty_manager import BountyManager
from kali_tools.kali_integration import KaliToolsIntegration
from training_engine.content_generator import TrainingGenerator
import threading
from loguru import logger

class JAIDACompleteSystem:
    def __init__(self):
        self.crawler_orchestrator = None
        self.bounty_manager = BountyManager()
        self.kali_integration = KaliToolsIntegration()
        self.training_generator = TrainingGenerator()
        self.running = False
        logger.info("JAIDA Complete System initialized")
    
    def start(self):
        """Start all system components"""
        self.running = True
        
        # Start crawler system
        self.crawler_orchestrator = start_crawler_system()
        
        # Start intelligence processing thread
        intel_thread = threading.Thread(
            target=self.process_intelligence_loop,
            daemon=True,
            name="intelligence_processor"
        )
        intel_thread.start()
        
        # Start auto-bounty creation thread
        bounty_thread = threading.Thread(
            target=self.auto_bounty_creation,
            daemon=True,
            name="auto_bounty"
        )
        bounty_thread.start()
        
        logger.info("✅ JAIDA Complete System Started")
        print("\n" + "="*70)
        print("🚀 JAIDA OMEGA PLATFORM - FULLY INTEGRATED SYSTEM")
        print("="*70)
        print(f"📊 Crawlers: {len(self.crawler_orchestrator.crawlers)} agents running")
        print(f"🐛 Bug Bounty: {len(self.bounty_manager.bounties.get('active', []))} active bounties")
        print(f"⚔️ Kali Tools: {sum(1 for v in self.kali_integration.tools_available.values() if v)} available")
        print(f"📚 Training: Ready to generate lessons")
        print("="*70)
    
    def process_intelligence_loop(self):
        """Continuous intelligence processing loop"""
        while self.running:
            try:
                # Read from intelligence database
                with open('intelligence_database.json', 'r') as f:
                    lines = f.readlines()[-100:]  # Last 100 entries
                
                for line in lines:
                    data = json.loads(line.strip())
                    
                    # Feed to training generator
                    if data.get('type') == 'intelligence':
                        self.training_generator.update_from_crawled_intel([data])
                    
                    # Auto-create training content
                    if len(lines) % 10 == 0:  # Every 10 new entries
                        lesson = self.training_generator.generate_lesson()
                        logger.info(f"Auto-generated lesson: {lesson['title']}")
                
            except Exception as e:
                logger.error(f"Intelligence processing error: {e}")
            
            time.sleep(60)  # Check every minute
    
    def auto_bounty_creation(self):
        """Automatically create bounties from crawled vulnerabilities"""
        while self.running:
            try:
                # Read crawled vulnerabilities
                with open('intelligence_database.json', 'r') as f:
                    lines = f.readlines()
                
                # Filter for vulnerabilities
                vuln_entries = []
                for line in lines[-50:]:  # Last 50 entries
                    data = json.loads(line.strip())
                    if 'vulnerability' in str(data).lower():
                        vuln_entries.append(data)
                
                # Create bounties for new vulnerabilities
                for vuln in vuln_entries[-5:]:  # Last 5 vulnerabilities
                    bounty_id = self.bounty_manager.generate_bounty_from_crawl(vuln)
                    if bounty_id:
                        logger.info(f"Auto-created bounty: {bounty_id}")
                
            except Exception as e:
                logger.error(f"Auto-bounty creation error: {e}")
            
            time.sleep(300)  # Check every 5 minutes
    
    def run_security_assessment(self, target):
        """Run complete security assessment using integrated tools"""
        print(f"\n⚔️ Running security assessment on: {target}")
        
        # Kali tools scan
        report_file = self.kali_integration.generate_security_report(target)
        
        # Generate training from findings
        lesson = self.training_generator.generate_lesson(
            principle="Integrity",  # or auto-detect from scan
            user_level=3
        )
        
        # Auto-create bounty if critical findings
        if "critical" in str(lesson).lower():
            self.bounty_manager.create_bounty(
                vulnerability=f"Critical findings on {target}",
                reward_range=(1000, 5000),
                description=f"Automatically generated from security scan of {target}",
                scope=[target]
            )
        
        return {
            'report': report_file,
            'lesson_generated': lesson['title'],
            'bounty_created': 'critical' in str(lesson).lower()
        }
    
    def show_system_status(self):
        """Display current system status"""
        status = {
            'Crawlers Active': self.running,
            'Active Bounties': len(self.bounty_manager.bounties.get('active', [])),
            'Available Kali Tools': sum(1 for v in self.kali_integration.tools_available.values() if v),
            'Training Lessons Generated': len(self.training_generator.scenario_library.get('generated_lessons', [])),
            'Intelligence Items': self.count_intelligence_items()
        }
        
        print("\n📈 SYSTEM STATUS")
        print("="*40)
        for key, value in status.items():
            print(f"{key}: {value}")
    
    def count_intelligence_items(self):
        """Count intelligence database entries"""
        try:
            with open('intelligence_database.json', 'r') as f:
                return len(f.readlines())
        except FileNotFoundError:
            return 0

# Command-line interface
if __name__ == "__main__":
    jaida = JAIDACompleteSystem()
    jaida.start()
    
    # Interactive menu
    while True:
        print("\n" + "="*50)
        print("🔧 JAIDA SYSTEM CONTROLS")
        print("="*50)
        print("1. System Status")
        print("2. Run Security Assessment")
        print("3. Generate Training Lesson")
        print("4. View Active Bounties")
        print("5. Exit")
        
        choice = input("\nSelect option: ")
        
        if choice == '1':
            jaida.show_system_status()
        elif choice == '2':
            target = input("Enter target (domain/IP): ").strip()
            if target:
                jaida.run_security_assessment(target)
        elif choice == '3':
            lesson = jaida.training_generator.generate_lesson()
            print(f"Generated: {lesson['title']}")
        elif choice == '4':
            from bug_bounty.bounty_dashboard import BountyDashboard
            dashboard = BountyDashboard()
            dashboard.show_active_bounties()
        elif choice == '5':
            print("Shutting down JAIDA system...")
            jaida.running = False
            break
        else:
            print("Invalid option")

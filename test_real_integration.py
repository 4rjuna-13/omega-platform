#!/usr/bin/env python3
"""
Test suite for JAIDA-OMEGA-SAIOS real integration
"""

import unittest
import tempfile
import os
import json
import yaml
import sqlite3
from datetime import datetime
import time

# Add src to path
import sys
sys.path.insert(0, 'src')

class TestRealIntegration(unittest.TestCase):
    """Test real integration components"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temp directory for test data
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.test_dir, 'data', 'web_crawler', 'intel'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'data', 'omega_nexus', 'alerts'), exist_ok=True)
        
        # Create test config
        self.config_path = os.path.join(self.test_dir, 'test_config.yaml')
        self.create_test_config()
        
        # Set environment
        os.environ['JAIDA_TEST_MODE'] = '1'
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_config(self):
        """Create test configuration"""
        config = {
            'alert_sources': {
                'omega_nexus_api': {'enabled': False},
                'web_crawler': {'enabled': False},
                'file_monitor': {'enabled': False},
                'demo_mode': {'enabled': True, 'alert_interval': 1}
            },
            'processing': {
                'alert_threshold': 0.5,
                'filter_low_confidence': False
            },
            'demo_mode': {'enabled': True}
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f)
    
    def test_alert_processor_initialization(self):
        """Test alert processor initialization"""
        from integration.real.alert_processor import RealAlertProcessor
        
        processor = RealAlertProcessor(self.config_path)
        
        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.config)
        self.assertEqual(processor.config['demo_mode']['enabled'], True)
    
    def test_alert_generation(self):
        """Test alert generation and processing"""
        from integration.real.alert_processor import RealAlertProcessor
        
        processor = RealAlertProcessor(self.config_path)
        
        # Create a test alert
        test_alert = {
            'alert_id': 'TEST-001',
            'source': 'test',
            'alert_type': 'test_alert',
            'severity': 8,
            'confidence': 0.9,
            'description': 'Test alert for integration',
            'timestamp': datetime.now().isoformat(),
            'raw_data': {'test': True}
        }
        
        # Test processing decision
        should_forward = processor._should_forward_to_autonomous(test_alert)
        self.assertTrue(should_forward)
        
        # Test low confidence alert
        low_alert = test_alert.copy()
        low_alert['confidence'] = 0.3
        should_forward_low = processor._should_forward_to_autonomous(low_alert)
        
        # With threshold 0.5, should not forward
        self.assertFalse(should_forward_low)

def run_integration_demo():
    """Run a quick integration demo"""
    print("\n" + "="*60)
    print("🧪 JAIDA-OMEGA-SAIOS REAL INTEGRATION DEMO")
    print("="*60)
    
    try:
        # Simple demo without complex imports
        print("\n1. Creating test alert processor...")
        
        # Import and create processor
        import sys
        sys.path.insert(0, 'src')
        from integration.real.alert_processor import RealAlertProcessor
        
        processor = RealAlertProcessor()
        
        print("2. Starting processor for 20 seconds...")
        processor.start()
        
        print("3. Monitoring progress...")
        for i in range(4):
            time.sleep(5)
            stats = processor.get_statistics()
            alerts = stats['statistics']['alerts_processed']
            print(f"   Progress: {(i+1)*5}s - Alerts processed: {alerts}")
        
        print("4. Stopping processor...")
        processor.stop()
        
        print("\n✅ Demo completed successfully")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("="*60)

if __name__ == "__main__":
    # Check if we should run demo
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        run_integration_demo()
    else:
        # Run tests
        print("Running integration tests...")
        unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
        
        # Also run a quick functionality check
        print("\n" + "="*60)
        print("🔍 Quick Functionality Check")
        print("="*60)
        
        try:
            # Check if modules exist
            import importlib
            
            modules_to_check = [
                'src.integration.real.alert_processor',
                'omega_nexus_real_integration'
            ]
            
            for module_name in modules_to_check:
                try:
                    importlib.import_module(module_name.replace('/', '.').replace('.py', ''))
                    print(f"✅ {module_name}")
                except ImportError:
                    print(f"❌ {module_name} (not found)")
            
            # Check database
            if os.path.exists('data/sovereign.db'):
                print("✅ Database exists")
            else:
                print("⚠️  Database not found")
            
            print("\n✅ Quick check complete")
            
        except Exception as e:
            print(f"❌ Check failed: {e}")

#!/usr/bin/env python3
"""
Basic tests for JAIDA-Omega-SAIOS
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestImports(unittest.TestCase):
    """Test that all modules can be imported"""
    
    def test_core_imports(self):
        """Test core module imports"""
        try:
            import core.jaida_core
            import core.config_manager
            import core.production_logger
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_adapter_imports(self):
        """Test adapter imports"""
        try:
            import adapters.real_data_adapter
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_database(self):
        """Test database connection"""
        import sqlite3
        try:
            conn = sqlite3.connect('data/sovereign_data.db')
            conn.close()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Database test failed: {e}")

if __name__ == '__main__':
    unittest.main()

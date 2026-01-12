#!/usr/bin/env python3
"""
Module Launcher - Runs lessons and labs from the curriculum.
"""
import sys
import importlib.util
from loguru import logger

def launch_module(module_id, user_level=1):
    """Launch any module by ID - the universal one-liner for content delivery."""
    from tutorial_mode.curriculum import get_module
    
    module_info = get_module(module_id)
    
    if not module_info:
        logger.error(f"Module not found: {module_id}")
        return False
    
    print(f"\n🚀 Launching: {module_info['name']}")
    print("="*60)
    
    # Determine module type and launch accordingly
    module_type = module_info.get('type', 'lesson')
    
    if module_type == 'lesson':
        # Import and run lesson module
        try:
            if module_info.get('file'):
                # Dynamic import
                spec = importlib.util.spec_from_file_location(
                    module_id, 
                    f"tutorial_mode/{module_info['file']}"
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_id] = module
                spec.loader.exec_module(module)
                
                # Find and run the main class
                if hasattr(module, 'CIATriadLesson'):
                    lesson = module.CIATriadLesson(user_level=user_level)
                    return lesson.run_lesson()
                elif hasattr(module, 'run_lesson'):
                    return module.run_lesson()
            else:
                print(f"⚠️  Module file not specified: {module_id}")
        except Exception as e:
            logger.error(f"Failed to launch lesson {module_id}: {e}")
            return False
    
    elif module_type == 'lab':
        # Import and run lab module
        try:
            if module_info.get('file'):
                spec = importlib.util.spec_from_file_location(
                    module_id,
                    f"tutorial_mode/{module_info['file']}"
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_id] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, 'CIASandboxLab'):
                    lab = module.CIASandboxLab()
                    return lab.run_lab()
                elif hasattr(module, 'run_lab'):
                    return module.run_lab()
            else:
                print(f"⚠️  Lab file not specified: {module_id}")
        except Exception as e:
            logger.error(f"Failed to launch lab {module_id}: {e}")
            return False
    
    return True

# Command-line interface for testing
if __name__ == "__main__":
    if len(sys.argv) > 1:
        module_id = sys.argv[1]
        user_level = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        launch_module(module_id, user_level)
    else:
        print("Usage: python module_launcher.py <module_id> [user_level]")
        print("\nAvailable modules from curriculum:")
        from tutorial_mode.curriculum import CURRICULUM
        for level, data in CURRICULUM.items():
            print(f"\nLevel {level}: {data['name']}")
            for module in data.get('modules', []):
                print(f"  • {module['id']} - {module['name']} ({module.get('type', 'unknown')})")

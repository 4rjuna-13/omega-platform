"""
Simple Phase 2G Integration for Omega v4
This adds the beginner tutorial system without breaking existing functionality
"""

import sys
import os

# Add current directory to path
sys.path.append('.')
sys.path.append('./tutorial_system')

def add_phase_2g_to_omega():
    """Add Phase 2G functionality to Omega v4"""
    
    try:
        # Read the current omega_v4_tutorial_final.py
        with open('omega_v4_tutorial_final.py', 'r') as f:
            content = f.read()
        
        # Check if Phase 2G is already added
        if 'PHASE_2G_AVAILABLE' in content:
            print("Phase 2G already integrated")
            return True
        
        # Find the class definition and add imports
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # Add Phase 2G imports after tutorial imports
            if 'from tutorial_integration import TutorialIntegration' in line:
                new_lines.append('')
                new_lines.append('# PHASE 2G IMPORTS')
                new_lines.append('try:')
                new_lines.append('    from tutorial_system import TutorialSystem')
                new_lines.append('    PHASE_2G_AVAILABLE = True')
                new_lines.append('except ImportError:')
                new_lines.append('    PHASE_2G_AVAILABLE = False')
                new_lines.append('')
            
            # Add Phase 2G initialization in __init__
            if 'print("Omega v4 Tutorial System Initialized")' in line:
                new_lines.append('        ')
                new_lines.append('        # Initialize Phase 2G if available')
                new_lines.append('        if PHASE_2G_AVAILABLE:')
                new_lines.append('            self.tutorial_system = TutorialSystem(self.tutorial_engine)')
        
        # Write back
        with open('omega_v4_tutorial_final.py', 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ Phase 2G successfully integrated into Omega v4")
        return True
        
    except Exception as e:
        print(f"❌ Error integrating Phase 2G: {e}")
        return False

# Also create a standalone Phase 2G launcher
cat > launch_phase_2g.py << 'EOF2'
"""
Standalone Phase 2G Launcher
For testing the beginner tutorial system
"""

import sys
sys.path.append('.')
sys.path.append('./tutorial_system')

def launch_phase_2g():
    print("\n" + "="*60)
    print("🚀 PROJECT OMEGA - PHASE 2G STANDALONE LAUNCHER")
    print("="*60)
    print("\nMarketing: 'The First All-in-One, Open-Source")
    print("Security Training Platform'")
    
    try:
        from tutorial_system import TutorialSystem
        from tutorial_engine import TutorialEngine
        
        # Initialize
        engine = TutorialEngine()
        phase_2g = TutorialSystem(engine)
        
        # Launch tutorial mode
        print("\n" + "="*60)
        print("🎯 BEGINNER TUTORIAL MODE")
        print("="*60)
        
        success = phase_2g.launch_tutorial_mode()
        
        if success:
            print("\n" + "="*60)
            print("✅ PHASE 2G COMPLETE!")
            print("="*60)
            print("\nYou can now:")
            print("1. Integrate with Omega v4")
            print("2. Test the full platform")
            print("3. Prepare for launch marketing")
        else:
            print("\n⚠️  Tutorial completed with issues")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    launch_phase_2g()
EOF2

# Make the integration script executable
chmod +x integrate_phase_2g_simple.py

print("Integration script created")

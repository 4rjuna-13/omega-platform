#!/usr/bin/env python3
"""
Create a patched version of omega_v3_integrated.py with Tutorial Engine
"""

import sys

# Read the original file
with open('omega_v3_integrated.py', 'r') as f:
    lines = f.readlines()

# Find where to add imports
import_section_end = 0
for i, line in enumerate(lines):
    if 'import' in line and 'flask' in line.lower():
        import_section_end = i + 1

# Find OmegaServer class
server_class_start = 0
for i, line in enumerate(lines):
    if 'class OmegaServer' in line:
        server_class_start = i
        break

# Find __init__ method
init_method_start = 0
for i in range(server_class_start, len(lines)):
    if 'def __init__' in lines[i]:
        init_method_start = i
        break

# Find setup_routes method
setup_routes_start = 0
for i in range(server_class_start, len(lines)):
    if 'def setup_routes' in lines[i]:
        setup_routes_start = i
        break

print("=== Analysis of omega_v3_integrated.py ===")
print(f"Import section ends around line: {import_section_end}")
print(f"OmegaServer class starts at line: {server_class_start}")
print(f"__init__ method starts at line: {init_method_start}")
print(f"setup_routes method starts at line: {setup_routes_start}")

# Create the patched version
print("\n=== Creating patched version: omega_v4_tutorial.py ===")

# Start building new file
new_lines = []

# Add imports
for i in range(len(lines)):
    new_lines.append(lines[i])
    if i == import_section_end:
        new_lines.append('\n# Tutorial Engine - Phase 2G\n')
        new_lines.append('from tutorial_engine import TutorialEngine\n')
        new_lines.append('import tutorial_api\n')
        new_lines.append('import tutorial_integration\n')

# Convert to string to find where to add in __init__
content = ''.join(new_lines)

# Now create the actual patched file differently
# Let me just show what needs to be added

print("\n📝 MANUAL INTEGRATION INSTRUCTIONS:")
print("\n1. Add these imports at the top (after other imports):")
print("""
# Tutorial Engine - Phase 2G
from tutorial_engine import TutorialEngine
import tutorial_api
import tutorial_integration
""")

print("\n2. In OmegaServer.__init__() method, find where other engines are initialized")
print("   (look for lines with 'self.deception_engine' or 'self.response_engine')")
print("   Add after those lines:")
print("""
        # Tutorial Engine (Phase 2G)
        self.tutorial_engine = TutorialEngine(self)
        print("[SYSTEM] Tutorial Engine ready")
        
        # Integrate with command processor
        tutorial_integration.integrate_tutorial_with_commands(self, self.tutorial_engine)
""")

print("\n3. In setup_routes() method, add at the end:")
print("""
        # Setup tutorial API
        tutorial_api.setup_tutorial_api(self.app, self.tutorial_engine)
""")

print("\n4. Save the file and test with:")
print("   python3 omega_v3_integrated.py")
print("\n5. Users can now type 'tutorial start welcome' to begin!")

# Actually create a patched version
print("\n=== Creating omega_v4_tutorial.py ===")

# Read the entire file
with open('omega_v3_integrated.py', 'r') as f:
    content = f.read()

# Add imports
imports_to_add = '''# Tutorial Engine - Phase 2G
from tutorial_engine import TutorialEngine
import tutorial_api
import tutorial_integration

'''

# Find where to add imports (after the last import)
import_pos = content.find('from flask_socketio import SocketIO')
if import_pos == -1:
    import_pos = content.find('import flask')
    
if import_pos != -1:
    # Find the end of this import line
    end_of_line = content.find('\n', import_pos)
    # Insert our imports after this line
    content = content[:end_of_line+1] + imports_to_add + content[end_of_line+1:]

# Add tutorial engine initialization
# Look for response engine initialization
response_init_pos = content.find('self.response_engine = AutonomousResponse(self)')
if response_init_pos == -1:
    response_init_pos = content.find('self.deception_engine = DeceptionEngine(self)')

if response_init_pos != -1:
    # Find the end of initialization section
    end_of_section = content.find('\n\n', response_init_pos)
    if end_of_section == -1:
        end_of_section = content.find('\n        ', response_init_pos + 100)
    
    tutorial_init = '''        # Tutorial Engine (Phase 2G)
        self.tutorial_engine = TutorialEngine(self)
        print("[SYSTEM] Tutorial Engine ready")
        
        # Integrate with command processor
        tutorial_integration.integrate_tutorial_with_commands(self, self.tutorial_engine)
        
'''
    content = content[:end_of_section] + tutorial_init + content[end_of_section:]

# Add API routes setup
routes_pos = content.find('def setup_routes')
if routes_pos != -1:
    # Find the end of the method (look for next def at same indentation)
    method_end = content.find('\n    def ', routes_pos + 50)
    if method_end == -1:
        method_end = len(content)
    
    # Add before the method ends
    api_setup = '''        # Setup tutorial API
        tutorial_api.setup_tutorial_api(self.app, self.tutorial_engine)
'''
    content = content[:method_end] + api_setup + content[method_end:]

# Write the patched version
with open('omega_v4_tutorial.py', 'w') as f:
    f.write(content)

print("✅ Created omega_v4_tutorial.py - Omega v4.0 with Tutorial Engine!")
print("\nTo run: python3 omega_v4_tutorial.py")
print("Then type 'tutorial start welcome' to test!")


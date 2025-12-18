#!/bin/bash
# Integrate AutonomousOps with OmegaNexus

# Backup current file
cp omega_nexus.py omega_nexus_backup_phase3.py

# Add AutonomousOps integration
python3 -c "
import re

with open('omega_nexus.py', 'r') as f:
    content = f.read()

# Add autonomous ops import in __init__ after SovereignDB
init_pattern = r'print\(\"  ✅ Integrated: sovereign_db -> Persistent data layer\"\)'
init_replacement = '''print(\"  ✅ Integrated: sovereign_db -> Persistent data layer\")
        
        # Add AutonomousOps integration
        try:
            from autonomous_ops import integrate_autonomous_ops
            self.autonomous_ops = integrate_autonomous_ops(self)
        except ImportError as e:
            print(f\"  ⚠️  AutonomousOps not available: {e}\")
            self.autonomous_ops = None'''

content = re.sub(init_pattern, init_replacement, content)

# Add autonomous command
if 'def _cmd_dbstatus' in content:
    # Add after dbstatus command
    insert_point = content.find('def _cmd_dbstatus')
    end_func = content.find('def ', insert_point + 1)
    
    autonomous_cmd = '''
    def _cmd_autonomous(self, args: List[str]) -> bool:
        """Run autonomous operations cycle"""
        if not self.autonomous_ops:
            print(\"❌ AutonomousOps not available\")
            return False
            
        print(\"\\n🤖 Starting autonomous operations cycle...\")
        
        try:
            report = self.autonomous_ops.run_full_autonomous_cycle()
            
            # Log the operation
            if self.db and hasattr(self.db, 'log_operation'):
                self.db.log_operation(
                    command=\"AUTONOMOUS_CYCLE\",
                    issuer=\"OMEGA_NEXUS\",
                    result=f\"Autonomous cycle completed: {report['cycle_id']}\"
                )
            
            print(f\"✅ Autonomous cycle {report['cycle_id']} completed\")
            return True
        except Exception as e:
            print(f\"❌ Autonomous cycle failed: {e}\")
            import traceback
            traceback.print_exc()
            return False'''
    
    content = content[:end_func] + autonomous_cmd + content[end_func:]

# Add to commands dictionary
if '\"dbstatus\": self._cmd_dbstatus' in content:
    content = content.replace('\"dbstatus\": self._cmd_dbstatus',
                             '\"dbstatus\": self._cmd_dbstatus,\n            \"autonomous\": self._cmd_autonomous')

with open('omega_nexus_phase3.py', 'w') as f:
    f.write(content)

print(\"✅ AutonomousOps integration added to omega_nexus_phase3.py\")
"

# Replace the file
mv omega_nexus_phase3.py omega_nexus.py

echo "🎯 AutonomousOps integration complete!"

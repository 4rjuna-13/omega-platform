"""
MITRE ATT&CK Matrix Visualization for Omega Platform
"""
import json
from typing import Dict, List
from collections import defaultdict

class AttackMatrix:
    def __init__(self, mitre_module=None):
        self.tactics = [
            'Reconnaissance', 'Resource Development', 'Initial Access',
            'Execution', 'Persistence', 'Privilege Escalation',
            'Defense Evasion', 'Credential Access', 'Discovery',
            'Lateral Movement', 'Collection', 'Command and Control',
            'Exfiltration', 'Impact'
        ]
        
        # Sample technique mappings if no MITRE module provided
        self.technique_mappings = {
            'T1566': ['Initial Access'],
            'T1486': ['Impact'],
            'T1190': ['Initial Access'],
            'T1059': ['Execution'],
            'T1210': ['Lateral Movement'],
            'T1490': ['Impact'],
            'T1566.001': ['Initial Access']
        }
        
        self.mitre = mitre_module
    
    def generate_matrix(self, scenarios: List[Dict]) -> Dict:
        """Generate ATT&CK coverage matrix for scenarios"""
        coverage = {}
        
        # Initialize coverage matrix
        for tactic in self.tactics:
            coverage[tactic] = {}
        
        # Count technique usage in scenarios
        for scenario in scenarios:
            techniques = scenario.get('mitre_techniques', [])
            for tech_id in techniques:
                tactics = self._get_tactics_for_technique(tech_id)
                for tactic in tactics:
                    if tactic in coverage:
                        coverage[tactic][tech_id] = coverage[tactic].get(tech_id, 0) + 1
        
        return coverage
    
    def _get_tactics_for_technique(self, technique_id: str) -> List[str]:
        """Get tactics for a technique"""
        if self.mitre and hasattr(self.mitre, 'get_technique'):
            tech = self.mitre.get_technique(technique_id)
            if tech and 'tactics' in tech:
                return tech['tactics']
        
        # Fallback to our mapping
        return self.technique_mappings.get(technique_id, ['Unknown'])
    
    def get_coverage_stats(self, scenarios: List[Dict]) -> Dict:
        """Get coverage statistics"""
        matrix = self.generate_matrix(scenarios)
        
        total_techniques_covered = 0
        tactic_coverage = {}
        
        for tactic, techniques in matrix.items():
            covered = len([t for t in techniques.values() if t > 0])
            total = len(techniques) if techniques else 1  # Avoid division by zero
            tactic_coverage[tactic] = {
                'covered': covered,
                'total': total,
                'percentage': (covered / total * 100) if total > 0 else 0
            }
            total_techniques_covered += covered
        
        # Get unique techniques across all scenarios
        all_techniques = set()
        for scenario in scenarios:
            all_techniques.update(scenario.get('mitre_techniques', []))
        
        return {
            'total_scenarios': len(scenarios),
            'unique_techniques': len(all_techniques),
            'tactic_coverage': tactic_coverage,
            'coverage_matrix': matrix,
            'all_techniques': list(all_techniques)
        }
    
    def generate_visualization_data(self, scenarios: List[Dict]) -> Dict:
        """Generate data for visualization"""
        stats = self.get_coverage_stats(scenarios)
        
        # Prepare data for heatmap
        heatmap_data = []
        for tactic in self.tactics:
            row = []
            tactic_techs = stats['coverage_matrix'].get(tactic, {})
            
            # For visualization, we'll use the count as intensity
            max_count = max(tactic_techs.values()) if tactic_techs else 1
            
            for tech_id, count in tactic_techs.items():
                intensity = count / max_count if max_count > 0 else 0
                row.append({
                    'technique': tech_id,
                    'count': count,
                    'intensity': intensity,
                    'color': self._get_color_for_intensity(intensity)
                })
            
            heatmap_data.append({
                'tactic': tactic,
                'techniques': row,
                'total_coverage': len([t for t in tactic_techs.values() if t > 0])
            })
        
        # Identify gaps
        all_known_techniques = list(self.technique_mappings.keys())
        used_techniques = set()
        for scenario in scenarios:
            used_techniques.update(scenario.get('mitre_techniques', []))
        
        unused_techniques = [t for t in all_known_techniques if t not in used_techniques]
        
        return {
            'heatmap': heatmap_data,
            'stats': {
                'total_tactics': len(self.tactics),
                'tactics_covered': len([t for t in stats['tactic_coverage'].values() if t['covered'] > 0]),
                'techniques_covered': len(used_techniques),
                'coverage_gaps': unused_techniques[:10],  # Top 10 gaps
                'coverage_percentage': (len(used_techniques) / len(all_known_techniques) * 100) if all_known_techniques else 0
            },
            'tactics': self.tactics
        }
    
    def _get_color_for_intensity(self, intensity: float) -> str:
        """Get color for heatmap intensity"""
        if intensity == 0:
            return '#f0f0f0'  # Light gray for no coverage
        elif intensity < 0.3:
            return '#ffcccc'  # Light red
        elif intensity < 0.6:
            return '#ff6666'  # Medium red
        else:
            return '#ff0000'  # Bright red
    
    def get_recommendations(self, scenarios: List[Dict]) -> List[Dict]:
        """Get recommendations based on coverage gaps"""
        stats = self.get_coverage_stats(scenarios)
        
        recommendations = []
        
        # Check for tactic gaps
        for tactic, coverage in stats['tactic_coverage'].items():
            if coverage['covered'] == 0:
                recommendations.append({
                    'type': 'tactic_gap',
                    'priority': 'high',
                    'tactic': tactic,
                    'message': f'No coverage for {tactic} tactic',
                    'suggestion': f'Add scenarios covering {tactic} techniques'
                })
            elif coverage['percentage'] < 30:
                recommendations.append({
                    'type': 'low_coverage',
                    'priority': 'medium',
                    'tactic': tactic,
                    'coverage': f'{coverage["percentage"]:.1f}%',
                    'message': f'Low coverage for {tactic} tactic',
                    'suggestion': f'Add more scenarios to improve {tactic} coverage'
                })
        
        # Check for critical technique gaps
        critical_techniques = ['T1190', 'T1059', 'T1078', 'T1566', 'T1486']
        all_techniques = set()
        for scenario in scenarios:
            all_techniques.update(scenario.get('mitre_techniques', []))
        
        missing_critical = [t for t in critical_techniques if t not in all_techniques]
        
        for tech in missing_critical:
            recommendations.append({
                'type': 'critical_technique_gap',
                'priority': 'high',
                'technique': tech,
                'message': f'Missing coverage for critical technique {tech}',
                'suggestion': 'Import or create scenarios covering this technique'
            })
        
        return recommendations[:5]  # Return top 5 recommendations

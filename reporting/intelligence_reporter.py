"""
JAIDA Automated Intelligence Reporter
Generates PDF reports from analyzed threat data using ReportLab[citation:3][citation:5].
"""
import sqlite3
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from loguru import logger
import matplotlib.pyplot as plt
import io

class IntelligenceReporter:
    def __init__(self, db_path='sovereign_data.db'):
        self.db_path = db_path
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'CustomStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        logger.info("Intelligence Reporter initialized")
    
    def fetch_recent_analyses(self, limit=10):
        """Fetch recent analyses from database for reporting."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT timestamp, pulse_name, classification, cia_impact_json, 
               jaida_actions_json, lesson_title 
        FROM otx_analyzed_intel 
        ORDER BY timestamp DESC 
        LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        analyses = []
        for row in rows:
            analyses.append({
                'timestamp': row[0],
                'pulse_name': row[1],
                'classification': row[2],
                'cia_impact': json.loads(row[3]),
                'jaida_actions': json.loads(row[4]),
                'lesson_title': row[5]
            })
        
        return analyses
    
    def generate_cia_chart_image(self, analyses):
        """Generate a simple chart of CIA impact scores."""
        if not analyses:
            return None
        
        # Prepare data for chart
        principles = ['Confidentiality', 'Integrity', 'Availability']
        scores = {p: 0 for p in principles}
        count = 0
        
        for analysis in analyses:
            cia = analysis.get('cia_impact', {})
            for principle in principles:
                scores[principle] += cia.get(principle, 0)
            count += 1
        
        if count > 0:
            avg_scores = [scores[p] / count for p in principles]
        else:
            avg_scores = [0, 0, 0]
        
        # Create plot
        plt.figure(figsize=(6, 4))
        bars = plt.bar(principles, avg_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('Average CIA Triad Impact Scores', fontweight='bold')
        plt.ylabel('Score (1-10)')
        plt.ylim(0, 10)
        
        # Add value labels on bars
        for bar, score in zip(bars, avg_scores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{score:.1f}', ha='center', va='bottom')
        
        # Save to bytes buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150)
        plt.close()
        buf.seek(0)
        
        return buf
    
    def create_daily_intelligence_report(self):
        """Generate a comprehensive daily intelligence report."""
        report_date = datetime.now().strftime('%Y-%m-%d')
        filename = f'reports/daily_intelligence_report_{report_date}.pdf'
        
        # Ensure reports directory exists
        import os
        os.makedirs('reports', exist_ok=True)
        
        # Create document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=24,
            textColor=colors.HexColor('#2C3E50')
        )
        story.append(Paragraph(f"JAIDA Daily Intelligence Report", title_style))
        story.append(Paragraph(f"Date: {report_date}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Fetch data
        analyses = self.fetch_recent_analyses(limit=10)
        
        if not analyses:
            story.append(Paragraph("No intelligence data available for reporting.", self.styles['Normal']))
        else:
            # Executive Summary
            story.append(Paragraph("Executive Summary", self.styles['Heading1']))
            summary_text = f"""
            This report summarizes {len(analyses)} recent threat intelligence analyses 
            processed by the JAIDA platform. Key findings include threat classifications, 
            CIA Triad impact assessments, and generated training materials.
            """
            story.append(Paragraph(summary_text, self.custom_style))
            story.append(Spacer(1, 12))
            
            # CIA Impact Chart
            chart_buf = self.generate_cia_chart_image(analyses)
            if chart_buf:
                story.append(Paragraph("CIA Triad Impact Analysis", self.styles['Heading2']))
                img = Image(chart_buf, width=4.5*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 12))
            
            # Detailed Analysis Table
            story.append(Paragraph("Threat Analysis Details", self.styles['Heading2']))
            
            table_data = [['Time', 'Threat', 'Classification', 'CIA Impact', 'Generated Lesson']]
            
            for analysis in analyses[:5]:  # Show top 5
                cia = analysis['cia_impact']
                cia_summary = f"C:{cia.get('Confidentiality', 0)} I:{cia.get('Integrity', 0)} A:{cia.get('Availability', 0)}"
                
                table_data.append([
                    analysis['timestamp'][11:19],  # Time only
                    analysis['pulse_name'][:30] + ('...' if len(analysis['pulse_name']) > 30 else ''),
                    analysis['classification'][:25],
                    cia_summary,
                    analysis['lesson_title'][:40] + ('...' if len(analysis['lesson_title']) > 40 else '')
                ])
            
            table = Table(table_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 1*inch, 1.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(table)
            story.append(Spacer(1, 15))
            
            # Recommended Actions
            story.append(Paragraph("Recommended Platform Actions", self.styles['Heading2']))
            
            if analyses:
                latest_actions = analyses[0]['jaida_actions']
                actions_text = f"""
                Based on the latest analysis ({analyses[0]['pulse_name']}):
                
                1. **Autonomous Response**: {latest_actions.get('autonomous_response', 'None specified')}
                
                2. **Training Development**: {latest_actions.get('training_lesson', 'None specified')}
                
                These actions have been queued for automated execution by the JAIDA platform.
                """
                story.append(Paragraph(actions_text, self.custom_style))
        
        # Build PDF
        doc.build(story)
        logger.info(f"Generated report: {filename}")
        return filename

if __name__ == "__main__":
    print("[*] Generating Daily Intelligence Report...")
    reporter = IntelligenceReporter()
    report_file = reporter.create_daily_intelligence_report()
    print(f"✅ Report generated: {report_file}")

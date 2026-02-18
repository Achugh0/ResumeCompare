import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

class PDFReportGenerator:
    def __init__(self, config):
        self.config = config
        self.output_folder = config.get("DOWNLOADS_FOLDER", "downloads")

    def generate_report(self, analysis, matrix):
        """Generates a PDF report from the analysis data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Resume_Analysis_Report_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Styles
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        
        # Custom Style for Recommendation
        rec_style = ParagraphStyle(
            'Recommendation',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.whitesmoke,
            backColor=colors.darkblue,
            alignment=1, # Center
            spaceAfter=20,
            allowWidows=0
        )

        # Title
        story.append(Paragraph("Resume Analysis Report", title_style))
        story.append(Spacer(1, 12))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Paragraph(analysis.get("summary", "No summary available."), normal_style))
        story.append(Spacer(1, 20))

        # Overall Score & Recommendation
        overall_score = analysis.get("overall_score", 0)
        rec = analysis.get("recommendation", "N/A")
        
        score_text = f"<b>Overall Score: {overall_score}/100</b>  |  Recommendation: {rec}"
        
        # Color coding recommendation
        if overall_score >= 85:
            rec_color = colors.darkgreen
        elif overall_score >= 70:
            rec_color = colors.orange
        else:
            rec_color = colors.firebrick
            
        rec_param = Paragraph(score_text, ParagraphStyle(
            'Rec', parent=normal_style, fontSize=14, textColor=rec_color, spaceAfter=20, alignment=1, fontName='Helvetica-Bold'
        ))
        story.append(rec_param)
        story.append(Spacer(1, 12))

        # Detailed Analysis Table
        story.append(Paragraph("Detailed Analysis", heading_style))
        
        table_data = [["Parameter", "Score", "Weight", "Weighted", "Rationale"]]
        
        for item in matrix:
            row = [
                Paragraph(item["parameter"], normal_style),
                item["score"],
                item["weight"],
                item["weighted_score"],
                Paragraph(item["rationale"], normal_style)
            ]
            table_data.append(row)

        table = Table(table_data, colWidths=[120, 50, 50, 60, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))

        # Strengths & Improvements
        col_width = 250
        
        # Helper to create bullet lists
        def create_list(title, items):
            content = [Paragraph(f"<b>{title}</b>", heading_style)]
            for item in items:
                content.append(Paragraph(f"• {item}", normal_style))
            return content

        strengths = create_list("Key Strengths", analysis.get("strengths", []))
        improvements = create_list("Areas for Improvement", analysis.get("improvements", []))

        # Side by side lists (using Table for layout)
        list_table = Table([[strengths, improvements]], colWidths=[col_width, col_width])
        list_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(list_table)
        
        doc.build(story)
        return filename

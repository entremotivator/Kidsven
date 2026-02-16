import streamlit as st
from typing import List, Dict
import os
from openai import OpenAI
from datetime import datetime
import json
from io import BytesIO

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="KidVentures Learning Assessment",
    page_icon="🎓",
    layout="wide"
)

# ---------------- Initialize Session State ----------------
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY', '')

# ---------------- PDF Generation Functions ----------------

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for page numbers and headers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        page_num = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(7.5*inch, 0.5*inch, page_num)
        self.drawString(1*inch, 0.5*inch, "© 2024 KidVentures Learning")

def create_learning_style_chart(scores: Dict) -> Drawing:
    """Create a pie chart for learning styles"""
    drawing = Drawing(400, 200)
    
    data = [scores.get('visual', 0), scores.get('auditory', 0), scores.get('kinesthetic', 0)]
    total = sum(data)
    
    if total > 0:
        pie = Pie()
        pie.x = 100
        pie.y = 25
        pie.width = 150
        pie.height = 150
        pie.data = data
        pie.labels = [f'Visual\n{data[0]}/6', f'Auditory\n{data[1]}/6', f'Kinesthetic\n{data[2]}/6']
        pie.slices.strokeWidth = 0.5
        pie.slices[0].fillColor = colors.HexColor('#667eea')
        pie.slices[1].fillColor = colors.HexColor('#764ba2')
        pie.slices[2].fillColor = colors.HexColor('#f093fb')
        
        drawing.add(pie)
    
    return drawing

def create_dimension_bar_chart(dimension_scores: Dict) -> Drawing:
    """Create a bar chart for dimension scores"""
    drawing = Drawing(400, 200)
    
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = [list(dimension_scores.values())]
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 6
    bc.valueAxis.valueStep = 1
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = list(dimension_scores.keys())
    
    bc.bars[0].fillColor = colors.HexColor('#667eea')
    
    drawing.add(bc)
    
    return drawing

def calculate_dimension_scores(answers: Dict) -> Dict:
    """Calculate scores for each dimension"""
    scores = {
        'visual': 0,
        'auditory': 0,
        'kinesthetic': 0,
    }
    
    # Learning styles (questions 1-6)
    learning_map = {
        'q1': ['written', 'spoken', 'physical'],
        'q2': ['diagram', 'read', 'handling'],
        'q3': ['drawing', 'talking', 'gesturing'],
        'q4': ['visualize', 'sound', 'write'],
        'q5': ['messy', 'noise', 'sit still'],
        'q6': ['illustr', 'captivat', 'interact']
    }
    
    for q_key, keywords in learning_map.items():
        answer = answers.get(q_key, '').lower()
        if keywords[0] in answer or 'visual' in answer or 'picture' in answer:
            scores['visual'] += 1
        elif keywords[1] in answer or 'audi' in answer or 'hear' in answer:
            scores['auditory'] += 1
        elif keywords[2] in answer or 'kines' in answer or 'doing' in answer or 'build' in answer or 'texture' in answer:
            scores['kinesthetic'] += 1
    
    return scores

def generate_pdf_report(analysis: str, answers: Dict, timestamp: str, model: str) -> BytesIO:
    """Generate a comprehensive PDF report"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.HexColor('#667eea'),
        borderPadding=5,
        backColor=colors.HexColor('#f0f0ff')
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        fontSize=11,
        backColor=colors.HexColor('#fff3cd'),
        borderWidth=1,
        borderColor=colors.HexColor('#ffc107'),
        borderPadding=10,
        spaceAfter=10,
        spaceBefore=10
    )
    
    recommendation_style = ParagraphStyle(
        'Recommendation',
        parent=styles['BodyText'],
        fontSize=11,
        backColor=colors.HexColor('#e7f3ff'),
        borderWidth=1,
        borderColor=colors.HexColor('#2196F3'),
        borderPadding=10,
        leftIndent=20,
        spaceAfter=8
    )
    
    # Container for the story
    story = []
    
    # ========== COVER PAGE ==========
    
    # Logo/Header
    story.append(Spacer(1, 0.5*inch))
    
    title = Paragraph("KidVentures Learning", title_style)
    story.append(title)
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#764ba2'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    story.append(Paragraph("Comprehensive Learning Profile Assessment", subtitle_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Decorative line
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#667eea')))
    story.append(Spacer(1, 0.3*inch))
    
    # Report info box
    info_data = [
        ['Report Generated:', timestamp],
        ['AI Model:', model],
        ['Analysis Type:', 'Five-Dimension Comprehensive Profile'],
        ['Report Version:', '2.5']
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#667eea')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f0f0ff')]),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Mission statement
    mission_text = """
    <i>"At KidVentures Learning, we believe every child is uniquely created by God with specific gifts, 
    talents, and a divine purpose. This comprehensive assessment reveals your child's learning profile 
    across five critical dimensions, empowering you to support their educational journey with 
    confidence and biblical wisdom."</i>
    """
    story.append(Paragraph(mission_text, body_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Contact info
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph("📧 info@kidventureslearning.com | 📞 (404) 631-6320 | 🌐 www.kidventureslearning.com", contact_style))
    
    story.append(PageBreak())
    
    # ========== TABLE OF CONTENTS ==========
    
    story.append(Paragraph("Table of Contents", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    toc_data = [
        ['Section', 'Page'],
        ['Executive Summary', '3'],
        ['Learning Style Analysis', '4'],
        ['Cognitive Strengths Profile', '5'],
        ['Developmental Orientation', '6'],
        ['Social-Emotional Landscape', '7'],
        ['Biblical Identity & Purpose', '8'],
        ['Personalized Recommendations', '9'],
        ['Assessment Responses', '11'],
        ['Next Steps & Resources', '12']
    ]
    
    toc_table = Table(toc_data, colWidths=[4*inch, 1.5*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())
    
    # ========== LEARNING STYLE VISUALIZATION ==========
    
    story.append(Paragraph("Learning Style Distribution", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Calculate scores
    scores = calculate_dimension_scores(answers)
    
    # Add pie chart
    chart = create_learning_style_chart(scores)
    story.append(chart)
    story.append(Spacer(1, 0.2*inch))
    
    # Interpretation
    total = sum(scores.values())
    if total > 0:
        visual_pct = (scores['visual'] / 6) * 100
        auditory_pct = (scores['auditory'] / 6) * 100
        kinesthetic_pct = (scores['kinesthetic'] / 6) * 100
        
        interpretation = f"""
        <b>Learning Style Breakdown:</b><br/>
        • Visual Learning: {visual_pct:.0f}% ({scores['visual']}/6 indicators)<br/>
        • Auditory Learning: {auditory_pct:.0f}% ({scores['auditory']}/6 indicators)<br/>
        • Kinesthetic Learning: {kinesthetic_pct:.0f}% ({scores['kinesthetic']}/6 indicators)<br/><br/>
        
        This distribution reveals your child's preferred ways of receiving and processing information.
        """
        story.append(Paragraph(interpretation, body_style))
    
    story.append(PageBreak())
    
    # ========== AI ANALYSIS SECTIONS ==========
    
    story.append(Paragraph("Comprehensive AI Analysis", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Parse and format the analysis
    analysis_sections = analysis.split('\n\n')
    
    for section in analysis_sections:
        if not section.strip():
            continue
            
        # Check if it's a heading (starts with ## or #)
        if section.strip().startswith('##'):
            # Remove ## and format as heading
            heading_text = section.strip().replace('##', '').replace('🎯', '').replace('📚', '').replace('🧠', '').replace('💝', '').replace('✝️', '').replace('🚀', '').replace('🌟', '').strip()
            story.append(Paragraph(heading_text, heading2_style))
        elif section.strip().startswith('#'):
            heading_text = section.strip().replace('#', '').strip()
            story.append(Paragraph(heading_text, heading1_style))
        else:
            # Check for special formatting markers
            if section.strip().startswith('**') or '**KEY INSIGHT:**' in section:
                story.append(Paragraph(section.replace('**', ''), highlight_style))
            elif section.strip().startswith('•') or section.strip().startswith('-') or section.strip().startswith('1.'):
                # List items
                story.append(Paragraph(section, body_style))
            else:
                # Regular paragraph
                story.append(Paragraph(section, body_style))
        
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # ========== DETAILED RESPONSES ==========
    
    story.append(Paragraph("Complete Assessment Responses", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Group responses by dimension
    dimensions = {
        'Learning Style Preferences': ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'],
        'Developmental Orientation': ['q7', 'q8', 'q9', 'q10', 'q11', 'q12'],
        'Cognitive Strengths': ['q13', 'q14', 'q15', 'q16', 'q17', 'q18'],
        'Social-Emotional Profile': ['q19', 'q20', 'q21', 'q22', 'q23', 'q24'],
        'Biblical Identity Markers': ['q25', 'q26', 'q27', 'q28', 'q29', 'q30']
    }
    
    question_texts = {
        'q1': 'My child tends to remember things best after...',
        'q2': 'When assembling a new toy, they are most likely to...',
        'q3': 'Express themselves and their ideas through...',
        'q4': 'When spelling a new word, they often...',
        'q5': 'Most distracted in classroom by...',
        'q6': 'Enjoy books that have...',
        'q7': 'Organizes the plan and makes sure everyone knows their role',
        'q8': 'Comes up with imaginative and original ideas',
        'q9': 'Focuses on making sure everyone feels included',
        'q10': 'Is eager to start building or making physical parts',
        'q11': 'Enjoys improving systems or processes',
        'q12': 'Would rather invent a new game than play by rules',
        'q13': 'Shows talent for solving logic puzzles or asking why questions',
        'q14': 'Reading, writing stories, or large vocabulary',
        'q15': 'Recognizing melodies, good sense of rhythm, or drawn to instruments',
        'q16': 'Navigating new places, reading maps, or enjoys drawing/painting',
        'q17': 'Understanding other people\'s feelings and cooperating in groups',
        'q18': 'Being in nature, caring for animals, or noticing natural details',
        'q19': 'Able to calmly express their feelings, even when upset',
        'q20': 'Prefers playing with one or two close friends rather than large group',
        'q21': 'Easily picks up on the moods and emotions of people around them',
        'q22': 'Can bounce back from disappointments or setbacks',
        'q23': 'Comfortable starting conversations with new children',
        'q24': 'Will stand up for others or try to mediate conflicts',
        'q25': 'Praised for their unique ideas and creative spirit (Created)',
        'q26': 'Given a special role or purpose that helps others (Called)',
        'q27': 'Recognized for a specific skill or talent developed (Capable)',
        'q28': 'Feeling like a valued member of family/team/church (Connected)',
        'q29': 'Encouraged to use personal gifts to bless someone else',
        'q30': 'Reminded that they are loved unconditionally'
    }
    
    for dimension, questions in dimensions.items():
        story.append(Paragraph(f"<b>{dimension}</b>", heading2_style))
        
        response_data = [['Question', 'Response']]
        for q_key in questions:
            q_text = question_texts.get(q_key, q_key)
            answer = answers.get(q_key, 'Not answered')
            response_data.append([q_text, answer])
        
        response_table = Table(response_data, colWidths=[3*inch, 2.5*inch])
        response_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(response_table)
        story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # ========== NEXT STEPS ==========
    
    story.append(Paragraph("Next Steps & Action Plan", heading1_style))
    story.append(Spacer(1, 0.2*inch))
    
    next_steps = """
    <b>Immediate Actions (This Week):</b><br/>
    ☐ Share this report with your child's teacher or educational team<br/>
    ☐ Discuss one key strength with your child to affirm their identity<br/>
    ☐ Implement one learning style recommendation in your home<br/>
    ☐ Create a dedicated study space that matches their learning preferences<br/><br/>
    
    <b>Short-term Goals (This Month):</b><br/>
    ☐ Schedule a family meeting to discuss the Biblical identity insights<br/>
    ☐ Adjust homework routines based on learning style recommendations<br/>
    ☐ Explore enrichment activities that align with cognitive strengths<br/>
    ☐ Connect with other parents of children with similar profiles<br/><br/>
    
    <b>Long-term Development (This Year):</b><br/>
    ☐ Track progress and note changes in learning preferences<br/>
    ☐ Schedule follow-up assessment in 6-12 months<br/>
    ☐ Build a portfolio of work that showcases their unique strengths<br/>
    ☐ Develop a personalized education plan with measurable goals<br/><br/>
    
    <b>Resources & Support:</b><br/>
    • <b>Consultation:</b> Schedule a 1-on-1 consultation with our learning specialists<br/>
    • <b>Workshops:</b> Attend our monthly parent workshops on learning styles<br/>
    • <b>Community:</b> Join our online community of KidVentures families<br/>
    • <b>Materials:</b> Access our library of learning resources tailored to your child's profile<br/>
    """
    
    story.append(Paragraph(next_steps, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Contact section
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#667eea')))
    story.append(Spacer(1, 0.2*inch))
    
    contact_box = """
    <b>Ready to Take the Next Step?</b><br/><br/>
    Contact KidVentures Learning today to discuss how we can support your child's unique learning journey.<br/><br/>
    📧 Email: info@kidventureslearning.com<br/>
    📞 Phone: (404) 631-6320<br/>
    🌐 Website: www.kidventureslearning.com<br/><br/>
    <i>Learning with Confidence. Leading with Purpose.</i>
    """
    
    story.append(Paragraph(contact_box, recommendation_style))
    
    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    
    buffer.seek(0)
    return buffer

# ---------------- Streamlit App Configuration ----------------

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 1rem;'>
        <h1 style='color: white; margin: 0;'>🎓</h1>
        <h3 style='color: white; margin: 0;'>KidVentures</h3>
        <p style='color: white; margin: 0; font-size: 0.9rem;'>Learning Profile Assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ AI Configuration")
    
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.openai_api_key,
        type="password",
        help="Enter your OpenAI API key for AI-powered analysis"
    )
    
    if api_key_input:
        st.session_state.openai_api_key = api_key_input
        st.success("✅ API Key configured")
    else:
        st.warning("⚠️ Please enter your OpenAI API key")
    
    model_choice = st.selectbox(
        "AI Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        index=0,
        help="GPT-4o recommended for best results"
    )
    
    analysis_depth = st.slider(
        "Analysis Detail",
        min_value=600,
        max_value=1500,
        value=1000,
        step=100,
        help="Higher = more detailed (800-1200 words)"
    )
    
    st.markdown("---")
    
    st.info("""
    **📄 PDF Report Includes:**
    
    ✅ Professional cover page
    ✅ Table of contents
    ✅ Visual charts & graphs
    ✅ Comprehensive AI analysis
    ✅ All assessment responses
    ✅ Action plan & next steps
    ✅ Page numbers & branding
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📞 Contact
    📧 info@kidventureslearning.com  
    🌐 kidventureslearning.com  
    📞 (404) 631-6320
    """)

# ========== MAIN APPLICATION ==========

st.title("🎓 KidVentures Learning Full Assessment")
st.markdown("""
**Learning with Confidence. Leading with Purpose.**

Complete this comprehensive 30-question assessment to receive a beautifully formatted PDF report 
with AI-powered insights, visual analytics, and personalized recommendations.
""")

# ---------------- Helper Functions ----------------
def render_radio_question(q_num: int, question: str, options: List[str], key: str):
    """Render a radio button question and return the selected answer."""
    return st.radio(f"**{q_num}.** {question}", options, key=key)

# ---------------- Assessment Form ----------------
with st.form("full_assessment"):
    answers = {}
    
    # All questions (abbreviated for length - use your original full text)
    st.subheader("📚 Dimension 1: Learning Style Preferences")
    answers['q1'] = render_radio_question(1, "My child tends to remember things best after...",
        ["Seeing them written down or in a picture", "Hearing them spoken aloud", "Doing a physical activity associated with them"], "q1")
    answers['q2'] = render_radio_question(2, "When assembling a new toy, they are most likely to...",
        ["Look carefully at the diagrams in the manual", "Ask someone to read the instructions to them", "Ignore the instructions and figure it out by handling the pieces"], "q2")
    answers['q3'] = render_radio_question(3, "Express themselves and their ideas through...",
        ["Drawing, doodling, or making visual aids", "Talking, telling stories, or singing songs", "Gesturing, acting things out, or building models"], "q3")
    answers['q4'] = render_radio_question(4, "When spelling a new word, they often...",
        ["Try to visualize what the word looks like", "Sound out the letters phonetically", "Write it down or trace the letters with their finger"], "q4")
    answers['q5'] = render_radio_question(5, "Most distracted in classroom by...",
        ["Messy or cluttered visual surroundings", "Noises and other people talking", "Having to sit still for long periods"], "q5")
    answers['q6'] = render_radio_question(6, "Enjoy books that have...",
        ["Lots of detailed illustrations or photographs", "A captivating narrator or read aloud with expression", "Interactive elements like flaps or textures to feel"], "q6")
    
    st.markdown("---")
    st.subheader("🎯 Dimension 2: Developmental Orientation Profile")
    answers['q7'] = render_radio_question(7, "When faced with a group project, my child organizes the plan and makes sure everyone knows their role.",
        ["Very often", "Sometimes", "Rarely"], "q7")
    answers['q8'] = render_radio_question(8, "Comes up with imaginative and original ideas for the project.",
        ["Very often", "Sometimes", "Rarely"], "q8")
    answers['q9'] = render_radio_question(9, "Focuses on making sure everyone feels included and is working together happily.",
        ["Very often", "Sometimes", "Rarely"], "q9")
    answers['q10'] = render_radio_question(10, "Is eager to start building or making the physical parts of the project.",
        ["Very often", "Sometimes", "Rarely"], "q10")
    answers['q11'] = render_radio_question(11, "Enjoys improving systems or processes to make work better.",
        ["Very often", "Sometimes", "Rarely"], "q11")
    answers['q12'] = render_radio_question(12, "Would rather invent a new game than play an existing one by the rules.",
        ["Very often", "Sometimes", "Rarely"], "q12")
    
    st.markdown("---")
    st.subheader("🧠 Dimension 3: Cognitive Strengths")
    answers['q13'] = render_radio_question(13, "My child shows a natural talent or passion for solving logic puzzles or asking 'why' questions.",
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"], "q13")
    answers['q14'] = render_radio_question(14, "Reading, writing stories, or has a large vocabulary for their age.",
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"], "q14")
    answers['q15'] = render_radio_question(15, "Recognizing melodies, has a good sense of rhythm, or drawn to musical instruments.",
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"], "q15")
    answers['q16'] = render_radio_question(16, "Navigating new places, reading maps, or enjoys activities like drawing, painting, or sculpting.",
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"], "q16")
    answers['q17'] = render_radio_question(17, "Understanding other people's feelings and is good at cooperating in a group.",
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"], "q17")
    answers['q18'] = render_radio_question(18, "Being in nature, caring for animals, or noticing details in the natural world.",
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"], "q18")
    
    st.markdown("---")
    st.subheader("💝 Dimension 4: Social-Emotional Profile")
    answers['q19'] = render_radio_question(19, "Able to calmly express their feelings, even when upset.",
        ["Usually", "Sometimes", "Rarely"], "q19")
    answers['q20'] = render_radio_question(20, "Prefers playing with one or two close friends rather than a large group.",
        ["Usually", "Sometimes", "Rarely"], "q20")
    answers['q21'] = render_radio_question(21, "Easily picks up on the moods and emotions of people around them.",
        ["Usually", "Sometimes", "Rarely"], "q21")
    answers['q22'] = render_radio_question(22, "Can bounce back from disappointments or setbacks in a reasonable amount of time.",
        ["Usually", "Sometimes", "Rarely"], "q22")
    answers['q23'] = render_radio_question(23, "Comfortable starting conversations with new children or joining a group already at play.",
        ["Usually", "Sometimes", "Rarely"], "q23")
    answers['q24'] = render_radio_question(24, "Will stand up for others or try to mediate when there is conflict between friends.",
        ["Usually", "Sometimes", "Rarely"], "q24")
    
    st.markdown("---")
    st.subheader("✝️ Dimension 5: Biblical Identity Markers")
    answers['q25'] = render_radio_question(25, "Praised for their unique ideas and creative spirit (Created).",
        ["Strongly agree", "Agree", "Disagree"], "q25")
    answers['q26'] = render_radio_question(26, "Given a special role or purpose that helps others (Called).",
        ["Strongly agree", "Agree", "Disagree"], "q26")
    answers['q27'] = render_radio_question(27, "Recognized for a specific skill or talent they have developed (Capable).",
        ["Strongly agree", "Agree", "Disagree"], "q27")
    answers['q28'] = render_radio_question(28, "Feeling like a valued member of family, team, or church group (Connected).",
        ["Strongly agree", "Agree", "Disagree"], "q28")
    answers['q29'] = render_radio_question(29, "Encouraged to use personal gifts to bless someone else (Called/Capable).",
        ["Strongly agree", "Agree", "Disagree"], "q29")
    answers['q30'] = render_radio_question(30, "Reminded that they are loved unconditionally (Created/Connected).",
        ["Strongly agree", "Agree", "Disagree"], "q30")
    
    st.markdown("---")
    submitted = st.form_submit_button("🚀 Generate Professional PDF Report", use_container_width=True)

# ---------------- Process Submission ----------------
if submitted:
    if not all(answers.values()):
        st.error("⚠️ Please answer all 30 questions before generating the report.")
    elif not st.session_state.openai_api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar.")
    else:
        with st.spinner("🤖 Generating comprehensive AI analysis and formatting professional PDF report... This may take 30-60 seconds."):
            try:
                # Generate AI analysis
                client = OpenAI(api_key=st.session_state.openai_api_key)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                user_responses = "\n".join([f"{k}: {v}" for k, v in answers.items()])
                
                system_prompt = """You are Dr. Emily Richardson, a renowned child development specialist with 20+ years of experience in educational psychology, learning theory, and faith-based education.

Create a comprehensive, warm, and insightful learning profile analysis."""

                user_prompt = f"""Analyze these assessment responses and create a detailed learning profile.

RESPONSES:
{user_responses}

Provide analysis with these sections (use ## for section headers):

## Executive Summary
2-3 sentences capturing the essence of this child's profile.

## Primary Learning Style
Identify Visual/Auditory/Kinesthetic with evidence and percentages.

## Cognitive Strengths Profile
Top 2-3 multiple intelligences with specific examples.

## Developmental Orientation
Leadership, creativity, collaboration, problem-solving approach.

## Social-Emotional Landscape
Emotional regulation, social preferences, empathy, resilience.

## Biblical Identity & Purpose
How they embody Created, Called, Capable, Connected.

## Personalized Recommendations

### For Parents (5-6 strategies)
Specific daily practices, environment setup, communication approaches.

### For Educators (3-4 strategies)
Classroom accommodations, assessment methods, group work.

### Potential Challenges & Solutions (2-3)
Areas of struggle with proactive solutions.

## Closing Affirmation
Powerful, personalized affirmation of this child's value and potential.

Use warm, encouraging language. Be specific based on actual responses. Length: 900-1200 words."""

                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=analysis_depth,
                    temperature=0.7
                )
                
                analysis = response.choices[0].message.content
                
                # Generate PDF
                pdf_buffer = generate_pdf_report(analysis, answers, timestamp, model_choice)
                
                st.success("✅ Professional PDF Report Generated!")
                
                # Display download button
                st.download_button(
                    label="📥 Download Professional PDF Report",
                    data=pdf_buffer,
                    file_name=f"KidVentures_Learning_Profile_{timestamp.replace(':', '-').replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # Preview
                with st.expander("📖 Preview Analysis Content"):
                    st.markdown(analysis)
                
                # Scores
                scores = calculate_dimension_scores(answers)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Visual Learning", f"{scores['visual']}/6")
                with col2:
                    st.metric("Auditory Learning", f"{scores['auditory']}/6")
                with col3:
                    st.metric("Kinesthetic Learning", f"{scores['kinesthetic']}/6")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Please check your API key and try again.")

st.markdown("---")
st.caption("© 2024 KidVentures Learning | Powered by OpenAI | Professional PDF Reports")

import streamlit as st
from typing import List
import os
from openai import OpenAI

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="KidVentures Learning Assessment",
    page_icon="🎓",
    layout="wide"
)

# ---------------- Sidebar with OpenAI Configuration ----------------
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/4A90E2/ffffff?text=KidVentures+Learning", use_container_width=True)
    
    st.header("🤖 AI Assessment Analyzer")
    
    st.markdown("""
    ### Welcome to KidVentures Learning!
    
    Our **AI-powered assessment** provides deep insights into your child's:
    
    - 📚 **Learning Style Preferences** - How they absorb information best
    - 🎯 **Developmental Orientation** - Their natural leadership and creative tendencies
    - 🧠 **Cognitive Strengths** - Multiple intelligence profiles
    - 💝 **Social-Emotional Profile** - How they relate to others
    - ✝️ **Biblical Identity** - Their God-given purpose and calling
    
    ---
    """)
    
    # OpenAI API Configuration
    st.subheader("⚙️ AI Configuration")
    
    # Check for API key in environment or session state
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = os.getenv('OPENAI_API_KEY', '')
    
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.openai_api_key,
        type="password",
        help="Enter your OpenAI API key to generate personalized AI analysis"
    )
    
    if api_key_input:
        st.session_state.openai_api_key = api_key_input
        st.success("✅ API Key configured")
    else:
        st.warning("⚠️ Please enter your OpenAI API key to enable AI analysis")
    
    # Model selection
    model_choice = st.selectbox(
        "AI Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        index=0,
        help="Select the OpenAI model for analysis. GPT-4o provides the most detailed insights."
    )
    
    # Analysis depth
    analysis_depth = st.slider(
        "Analysis Depth",
        min_value=300,
        max_value=1000,
        value=600,
        step=100,
        help="Maximum tokens for AI response (higher = more detailed)"
    )
    
    st.markdown("---")
    
    st.info("""
    **How it works:**
    1. Complete all assessment questions
    2. Click "Generate AI Analysis"
    3. Receive a comprehensive, personalized profile
    4. Download your full report
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📞 Contact Us
    📧 info@kidventureslearning.com  
    🌐 [www.kidventureslearning.com](http://www.kidventureslearning.com)  
    📞 (404) 631-6320
    """)
    
    st.caption("Powered by OpenAI GPT-4 • Version 2.0")

# ---------------- Main Page Title ----------------
st.title("🎓 KidVentures Learning Full Assessment")
st.markdown("""
**Learning with Confidence. Leading with Purpose.**

Welcome! This comprehensive assessment will help us understand your child's unique learning profile across five key dimensions. 
Your responses will be analyzed by advanced AI to provide personalized insights and recommendations.
""")

# ---------------- Helper Function ----------------
def render_radio_question(q_num: int, question: str, options: List[str], key: str):
    """Render a radio button question and return the selected answer."""
    return st.radio(f"**{q_num}.** {question}", options, key=key)

# ---------------- Assessment Form ----------------
with st.form("full_assessment"):
    st.header("📋 Assessment Questions")
    st.markdown("""
    Please answer each question thoughtfully. There are no right or wrong answers – 
    we're simply learning about what makes your child unique!
    """)

    answers = {}

    # ---------- Dimension 1: Learning Style ----------
    st.markdown("---")
    st.subheader("📚 Dimension 1: Learning Style Preferences")
    st.caption("Understanding how your child best absorbs and processes information")
    
    answers['learning_1'] = render_radio_question(
        1, 
        "My child tends to remember things best after...", 
        [
            "Seeing them written down or in a picture",
            "Hearing them spoken aloud",
            "Doing a physical activity associated with them"
        ],
        "q1"
    )
    
    answers['learning_2'] = render_radio_question(
        2, 
        "When assembling a new toy, they are most likely to...", 
        [
            "Look carefully at the diagrams in the manual",
            "Ask someone to read the instructions to them",
            "Ignore the instructions and figure it out by handling the pieces"
        ],
        "q2"
    )
    
    answers['learning_3'] = render_radio_question(
        3, 
        "Express themselves and their ideas through...", 
        [
            "Drawing, doodling, or making visual aids",
            "Talking, telling stories, or singing songs",
            "Gesturing, acting things out, or building models"
        ],
        "q3"
    )
    
    answers['learning_4'] = render_radio_question(
        4, 
        "When spelling a new word, they often...", 
        [
            "Try to visualize what the word looks like",
            "Sound out the letters phonetically",
            "Write it down or trace the letters with their finger"
        ],
        "q4"
    )
    
    answers['learning_5'] = render_radio_question(
        5, 
        "Most distracted in classroom by...", 
        [
            "Messy or cluttered visual surroundings",
            "Noises and other people talking",
            "Having to sit still for long periods"
        ],
        "q5"
    )
    
    answers['learning_6'] = render_radio_question(
        6, 
        "Enjoy books that have...", 
        [
            "Lots of detailed illustrations or photographs",
            "A captivating narrator or read aloud with expression",
            "Interactive elements like flaps or textures to feel"
        ],
        "q6"
    )

    # ---------- Dimension 2: Developmental Orientation ----------
    st.markdown("---")
    st.subheader("🎯 Dimension 2: Developmental Orientation Profile")
    st.caption("Identifying natural tendencies in leadership, creativity, and collaboration")
    
    answers['dev_7'] = render_radio_question(
        7, 
        "When faced with a group project, my child organizes the plan and makes sure everyone knows their role.", 
        ["Very often", "Sometimes", "Rarely"],
        "q7"
    )
    
    answers['dev_8'] = render_radio_question(
        8, 
        "Comes up with imaginative and original ideas for the project.", 
        ["Very often", "Sometimes", "Rarely"],
        "q8"
    )
    
    answers['dev_9'] = render_radio_question(
        9, 
        "Focuses on making sure everyone feels included and is working together happily.", 
        ["Very often", "Sometimes", "Rarely"],
        "q9"
    )
    
    answers['dev_10'] = render_radio_question(
        10, 
        "Is eager to start building or making the physical parts of the project.", 
        ["Very often", "Sometimes", "Rarely"],
        "q10"
    )
    
    answers['dev_11'] = render_radio_question(
        11, 
        "Enjoys improving systems or processes to make work better.", 
        ["Very often", "Sometimes", "Rarely"],
        "q11"
    )
    
    answers['dev_12'] = render_radio_question(
        12, 
        "Would rather invent a new game than play an existing one by the rules.", 
        ["Very often", "Sometimes", "Rarely"],
        "q12"
    )

    # ---------- Dimension 3: Cognitive Strengths ----------
    st.markdown("---")
    st.subheader("🧠 Dimension 3: Cognitive Strengths")
    st.caption("Discovering multiple intelligence patterns and natural aptitudes")
    
    answers['cog_13'] = render_radio_question(
        13, 
        "My child shows a natural talent or passion for solving logic puzzles or asking 'why' questions.", 
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"],
        "q13"
    )
    
    answers['cog_14'] = render_radio_question(
        14, 
        "Reading, writing stories, or has a large vocabulary for their age.", 
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"],
        "q14"
    )
    
    answers['cog_15'] = render_radio_question(
        15, 
        "Recognizing melodies, has a good sense of rhythm, or drawn to musical instruments.", 
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"],
        "q15"
    )
    
    answers['cog_16'] = render_radio_question(
        16, 
        "Navigating new places, reading maps, or enjoys activities like drawing, painting, or sculpting.", 
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"],
        "q16"
    )
    
    answers['cog_17'] = render_radio_question(
        17, 
        "Understanding other people's feelings and is good at cooperating in a group.", 
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"],
        "q17"
    )
    
    answers['cog_18'] = render_radio_question(
        18, 
        "Being in nature, caring for animals, or noticing details in the natural world.", 
        ["Describes my child well", "Describes my child somewhat", "Does not describe my child"],
        "q18"
    )

    # ---------- Dimension 4: Social-Emotional Profile ----------
    st.markdown("---")
    st.subheader("💝 Dimension 4: Social-Emotional Profile")
    st.caption("Understanding emotional awareness and social interaction patterns")
    
    answers['soc_19'] = render_radio_question(
        19, 
        "Able to calmly express their feelings, even when upset.", 
        ["Usually", "Sometimes", "Rarely"],
        "q19"
    )
    
    answers['soc_20'] = render_radio_question(
        20, 
        "Prefers playing with one or two close friends rather than a large group.", 
        ["Usually", "Sometimes", "Rarely"],
        "q20"
    )
    
    answers['soc_21'] = render_radio_question(
        21, 
        "Easily picks up on the moods and emotions of people around them.", 
        ["Usually", "Sometimes", "Rarely"],
        "q21"
    )
    
    answers['soc_22'] = render_radio_question(
        22, 
        "Can bounce back from disappointments or setbacks in a reasonable amount of time.", 
        ["Usually", "Sometimes", "Rarely"],
        "q22"
    )
    
    answers['soc_23'] = render_radio_question(
        23, 
        "Comfortable starting conversations with new children or joining a group already at play.", 
        ["Usually", "Sometimes", "Rarely"],
        "q23"
    )
    
    answers['soc_24'] = render_radio_question(
        24, 
        "Will stand up for others or try to mediate when there is conflict between friends.", 
        ["Usually", "Sometimes", "Rarely"],
        "q24"
    )

    # ---------- Dimension 5: Biblical Identity Markers ----------
    st.markdown("---")
    st.subheader("✝️ Dimension 5: Biblical Identity Markers")
    st.caption("Recognizing God-given identity through Created, Called, Capable, and Connected")
    
    answers['bib_25'] = render_radio_question(
        25, 
        "Praised for their unique ideas and creative spirit (Created).", 
        ["Strongly agree", "Agree", "Disagree"],
        "q25"
    )
    
    answers['bib_26'] = render_radio_question(
        26, 
        "Given a special role or purpose that helps others (Called).", 
        ["Strongly agree", "Agree", "Disagree"],
        "q26"
    )
    
    answers['bib_27'] = render_radio_question(
        27, 
        "Recognized for a specific skill or talent they have developed (Capable).", 
        ["Strongly agree", "Agree", "Disagree"],
        "q27"
    )
    
    answers['bib_28'] = render_radio_question(
        28, 
        "Feeling like a valued member of family, team, or church group (Connected).", 
        ["Strongly agree", "Agree", "Disagree"],
        "q28"
    )
    
    answers['bib_29'] = render_radio_question(
        29, 
        "Encouraged to use personal gifts to bless someone else (Called/Capable).", 
        ["Strongly agree", "Agree", "Disagree"],
        "q29"
    )
    
    answers['bib_30'] = render_radio_question(
        30, 
        "Reminded that they are loved unconditionally (Created/Connected).", 
        ["Strongly agree", "Agree", "Disagree"],
        "q30"
    )

    st.markdown("---")
    submitted = st.form_submit_button("🚀 Generate AI-Powered Analysis", use_container_width=True)

# ---------------- AI-Powered Analysis ----------------
if submitted:
    # Check if all questions are answered
    if not all(answers.values()):
        st.error("⚠️ Please answer all questions before generating the analysis.")
    elif not st.session_state.openai_api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar to generate AI analysis.")
    else:
        st.markdown("---")
        st.header("🎯 Your Child's Comprehensive Learning Profile")
        
        with st.spinner("🤖 Our AI is analyzing your child's responses across all five dimensions... This may take 15-30 seconds."):
            try:
                # Initialize OpenAI client
                client = OpenAI(api_key=st.session_state.openai_api_key)
                
                # Prepare detailed prompt for OpenAI
                user_responses = "\n".join([f"{k}: {v}" for k, v in answers.items()])
                
                system_prompt = """You are an expert child development specialist and educational psychologist with deep knowledge of:
- Learning style theories (Visual, Auditory, Kinesthetic)
- Multiple intelligences (Gardner's theory)
- Social-emotional development
- Biblical identity formation and faith-based education
- Personalized learning strategies

Your task is to analyze assessment responses and create a comprehensive, warm, and insightful learning profile for a child."""

                user_prompt = f"""Based on the following assessment responses from a parent about their child, create a comprehensive and personalized learning profile analysis.

ASSESSMENT RESPONSES:
{user_responses}

Please provide a detailed analysis that includes:

1. **PRIMARY LEARNING STYLE**: Identify whether the child is primarily Visual, Auditory, or Kinesthetic, with specific evidence from their responses.

2. **COGNITIVE STRENGTHS**: Highlight their strongest intelligences (linguistic, logical-mathematical, musical, spatial, interpersonal, naturalistic) with concrete examples.

3. **DEVELOPMENTAL ORIENTATION**: Describe their natural tendencies in leadership, creativity, collaboration, and innovation.

4. **SOCIAL-EMOTIONAL PROFILE**: Analyze their emotional regulation, social preferences, empathy, resilience, and conflict resolution abilities.

5. **BIBLICAL IDENTITY**: Discuss how they demonstrate being Created, Called, Capable, and Connected in their unique design.

6. **ACTIONABLE RECOMMENDATIONS**: Provide 4-5 specific, practical strategies for parents and educators to support this child's learning and growth.

Write in a warm, encouraging tone that celebrates the child's unique strengths while providing genuine insights. Make it personal and specific based on the actual responses, not generic. The parent should feel seen and understood. Length: 500-800 words."""

                # Call OpenAI API
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=analysis_depth,
                    temperature=0.7
                )
                
                # Extract the analysis
                analysis = response.choices[0].message.content
                
                # Display the analysis
                st.success("✅ Analysis Complete!")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 Full Analysis", "📥 Download Report", "💡 Quick Tips"])
                
                with tab1:
                    st.markdown(analysis)
                    
                    # Display response summary
                    with st.expander("📋 View Your Responses"):
                        for key, value in answers.items():
                            st.write(f"**{key}:** {value}")
                
                with tab2:
                    st.subheader("Download Your Full Report")
                    
                    # Create downloadable report
                    report_content = f"""
KidVentures Learning - Comprehensive Assessment Report
{'=' * 60}

CHILD LEARNING PROFILE ANALYSIS
Generated: {st.session_state.get('timestamp', 'Today')}

{analysis}

{'=' * 60}
DETAILED RESPONSES:

{user_responses}

{'=' * 60}
For more information:
📧 info@kidventureslearning.com
🌐 www.kidventureslearning.com
📞 (404) 631-6320

Learning with Confidence. Leading with Purpose.
"""
                    
                    st.download_button(
                        label="📥 Download Full Report (TXT)",
                        data=report_content,
                        file_name="kidventures_learning_profile.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    st.info("""
                    💡 **Next Steps:**
                    - Share this report with your child's teachers
                    - Use the recommendations to create a personalized learning plan
                    - Schedule a follow-up consultation with KidVentures Learning
                    """)
                
                with tab3:
                    st.subheader("🎯 Quick Action Items")
                    st.markdown("""
                    Based on your child's profile, here are immediate steps you can take:
                    
                    1. **This Week**: Try one new learning activity that matches their primary learning style
                    2. **This Month**: Create a home environment that supports their strongest intelligences
                    3. **Ongoing**: Use the social-emotional insights to support their friendships and confidence
                    4. **Family Discussion**: Share the Biblical Identity insights to affirm their God-given purpose
                    
                    **📞 Ready for More?**
                    Schedule a personalized consultation to create a customized learning roadmap for your child.
                    """)
                
            except Exception as e:
                st.error(f"❌ Error generating analysis: {str(e)}")
                st.info("Please check your API key and try again. If the problem persists, contact support.")

# ---------------- Call to Action (when not submitted) ----------------
if not submitted:
    st.markdown("---")
    st.info("""
    ### 🎯 Ready to Begin?
    
    Complete all 30 questions above and click "Generate AI-Powered Analysis" to receive:
    - ✅ Comprehensive learning style analysis
    - ✅ Cognitive strengths breakdown
    - ✅ Social-emotional insights
    - ✅ Biblical identity affirmation
    - ✅ Personalized recommendations
    - ✅ Downloadable full report
    
    **Investment in Your Child's Future:** This assessment typically takes 10-15 minutes to complete.
    """)

# ---------------- Footer ----------------
st.markdown("---")
st.caption("© 2024 KidVentures Learning | Powered by OpenAI GPT-4 | All Rights Reserved")

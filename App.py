import streamlit as st
from typing import List

# ---------------- Sidebar ----------------
st.sidebar.header("Youth Assessment AI Analyzer")
st.sidebar.info(
    "After completing the full assessment, this AI analyzer will provide a personalized one-paragraph summary of your child's learning style and strengths. Powered by OpenAI."
)

# ---------------- Page Title ----------------
st.title("KidVentures Learning Full Assessment")
st.markdown("""
📧 info@kidventureslearning.com  
🌐 [www.kidventureslearning.com](http://www.kidventureslearning.com)  
📞 (404) 631-6320  

**Learning with Confidence. Leading with Purpose.**
""")

# ---------------- Helper Function ----------------
def render_radio_question(q_num: int, question: str, options: List[str]):
    """Render a radio button question and return the selected answer."""
    return st.radio(f"{q_num}. {question}", options)

# ---------------- Assessment Form ----------------
with st.form("full_assessment"):
    st.header("Instructions")
    st.markdown("""
Thank you for choosing to unlock your child’s full potential!  
Please answer thoughtfully to help us build an in-depth profile of your child's unique strengths and learning style.
    """)

    answers = {}

    # ---------- Dimension 1: Learning Style ----------
    st.subheader("Dimension 1: Learning Style Preferences")
    answers['learning_1'] = render_radio_question(1, "My child tends to remember things best after...", [
        "Seeing them written down or in a picture",
        "Hearing them spoken aloud",
        "Doing a physical activity associated with them"
    ])
    answers['learning_2'] = render_radio_question(2, "When assembling a new toy, they are most likely to...", [
        "Look carefully at the diagrams in the manual",
        "Ask someone to read the instructions to them",
        "Ignore the instructions and figure it out by handling the pieces"
    ])
    answers['learning_3'] = render_radio_question(3, "Express themselves and their ideas through...", [
        "Drawing, doodling, or making visual aids",
        "Talking, telling stories, or singing songs",
        "Gesturing, acting things out, or building models"
    ])
    answers['learning_4'] = render_radio_question(4, "When spelling a new word, they often...", [
        "Try to visualize what the word looks like",
        "Sound out the letters phonetically",
        "Write it down or trace the letters with their finger"
    ])
    answers['learning_5'] = render_radio_question(5, "Most distracted in classroom by...", [
        "Messy or cluttered visual surroundings",
        "Noises and other people talking",
        "Having to sit still for long periods"
    ])
    answers['learning_6'] = render_radio_question(6, "Enjoy books that have...", [
        "Lots of detailed illustrations or photographs",
        "A captivating narrator or read aloud with expression",
        "Interactive elements like flaps or textures to feel"
    ])

    # ---------- Dimension 2: Developmental Orientation ----------
    st.subheader("Dimension 2: Developmental Orientation Profile")
    answers['dev_7'] = render_radio_question(7, "When faced with a group project, my child organizes the plan and makes sure everyone knows their role.", ["Very often", "Sometimes", "Rarely"])
    answers['dev_8'] = render_radio_question(8, "Comes up with imaginative and original ideas for the project.", ["Very often", "Sometimes", "Rarely"])
    answers['dev_9'] = render_radio_question(9, "Focuses on making sure everyone feels included and is working together happily.", ["Very often", "Sometimes", "Rarely"])
    answers['dev_10'] = render_radio_question(10, "Is eager to start building or making the physical parts of the project.", ["Very often", "Sometimes", "Rarely"])
    answers['dev_11'] = render_radio_question(11, "Enjoys improving systems or processes to make work better.", ["Very often", "Sometimes", "Rarely"])
    answers['dev_12'] = render_radio_question(12, "Would rather invent a new game than play an existing one by the rules.", ["Very often", "Sometimes", "Rarely"])

    # ---------- Dimension 3: Cognitive Strengths ----------
    st.subheader("Dimension 3: Cognitive Strengths")
    answers['cog_13'] = render_radio_question(13, "My child shows a natural talent or passion for solving logic puzzles or asking 'why' questions.", ["Describes my child well", "Describes my child somewhat", "Does not describe my child"])
    answers['cog_14'] = render_radio_question(14, "Reading, writing stories, or has a large vocabulary for their age.", ["Describes my child well", "Describes my child somewhat", "Does not describe my child"])
    answers['cog_15'] = render_radio_question(15, "Recognizing melodies, has a good sense of rhythm, or drawn to musical instruments.", ["Describes my child well", "Describes my child somewhat", "Does not describe my child"])
    answers['cog_16'] = render_radio_question(16, "Navigating new places, reading maps, or enjoys activities like drawing, painting, or sculpting.", ["Describes my child well", "Describes my child somewhat", "Does not describe my child"])
    answers['cog_17'] = render_radio_question(17, "Understanding other people’s feelings and is good at cooperating in a group.", ["Describes my child well", "Describes my child somewhat", "Does not describe my child"])
    answers['cog_18'] = render_radio_question(18, "Being in nature, caring for animals, or noticing details in the natural world.", ["Describes my child well", "Describes my child somewhat", "Does not describe my child"])

    # ---------- Dimension 4: Social-Emotional Profile ----------
    st.subheader("Dimension 4: Social-Emotional Profile")
    answers['soc_19'] = render_radio_question(19, "Able to calmly express their feelings, even when upset.", ["Usually", "Sometimes", "Rarely"])
    answers['soc_20'] = render_radio_question(20, "Prefers playing with one or two close friends rather than a large group.", ["Usually", "Sometimes", "Rarely"])
    answers['soc_21'] = render_radio_question(21, "Easily picks up on the moods and emotions of people around them.", ["Usually", "Sometimes", "Rarely"])
    answers['soc_22'] = render_radio_question(22, "Can bounce back from disappointments or setbacks in a reasonable amount of time.", ["Usually", "Sometimes", "Rarely"])
    answers['soc_23'] = render_radio_question(23, "Comfortable starting conversations with new children or joining a group already at play.", ["Usually", "Sometimes", "Rarely"])
    answers['soc_24'] = render_radio_question(24, "Will stand up for others or try to mediate when there is conflict between friends.", ["Usually", "Sometimes", "Rarely"])

    # ---------- Dimension 5: Biblical Identity Markers ----------
    st.subheader("Dimension 5: Biblical Identity Markers")
    answers['bib_25'] = render_radio_question(25, "Praised for their unique ideas and creative spirit (Created).", ["Strongly agree", "Agree", "Disagree"])
    answers['bib_26'] = render_radio_question(26, "Given a special role or purpose that helps others (Called).", ["Strongly agree", "Agree", "Disagree"])
    answers['bib_27'] = render_radio_question(27, "Recognized for a specific skill or talent they have developed (Capable).", ["Strongly agree", "Agree", "Disagree"])
    answers['bib_28'] = render_radio_question(28, "Feeling like a valued member of family, team, or church group (Connected).", ["Strongly agree", "Agree", "Disagree"])
    answers['bib_29'] = render_radio_question(29, "Encouraged to use personal gifts to bless someone else (Called/Capable).", ["Strongly agree", "Agree", "Disagree"])
    answers['bib_30'] = render_radio_question(30, "Reminded that they are loved unconditionally (Created/Connected).", ["Strongly agree", "Agree", "Disagree"])

    submitted = st.form_submit_button("Generate Full AI-Powered Analysis")

# ---------------- AI-Powered Teaser ----------------
if submitted:
    st.header("Your Child's Full Learning Profile - AI Summary")

    # Concatenate answers into a text block for OpenAI
    user_responses = "\n".join([f"{k}: {v}" for k, v in answers.items()])

    # ---------------- Placeholder for OpenAI API Call ----------------
    # You can replace this with a call to OpenAI's API to generate a one-paragraph summary
    # Example:
    # import openai
    # response = openai.Completion.create(
    #     model="gpt-4",
    #     prompt=f"Generate a one-paragraph insightful summary for a child's learning profile based on these responses:\n{user_responses}",
    #     max_tokens=250
    # )
    # summary = response.choices[0].text.strip()

    # Placeholder summary
    summary = (
        "Based on your answers, your child demonstrates a unique combination of learning preferences, "
        "cognitive strengths, social-emotional tendencies, and a grounded biblical identity. "
        "They appear to thrive in environments where their creativity, curiosity, and interpersonal skills are supported. "
        "This analysis highlights areas where they excel and opportunities to nurture growth, providing actionable insights "
        "to empower their learning journey and personal development."
    )

    st.success(summary)

    # ---------------- Call to Action ----------------
    st.subheader("Next Steps")
    st.markdown("""
Unlock the full, interactive report to receive:
- A comprehensive breakdown of all five dimensions.
- Personalized strategies for learning and development.
- Faith-based guidance through the Biblical Identity section.

[**Purchase Full Assessment Now for $XX.XX**](#)
""")

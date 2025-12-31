import os
from app.utils import Utils, VectorStoreUtils
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableMap
import google.generativeai as genai
from dotenv import load_dotenv
import re
# Load environment variables
load_dotenv('C:/Agentic/codellm/.env')
# Configure Google AI API 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# Text splitting
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.create_documents([text])

def analyze_resume(uploaded_file, job_requirements, job_id):
    resume_text = Utils.extract_text_from_resume(uploaded_file)
    with st.expander("View Resume Text"):
        st.text(resume_text)
 
    chain = get_chain()
    analysis = chain.invoke({
                "job_requirements": job_requirements,
                "resume_text": resume_text
            })
    return (analysis, resume_text)

def get_chain():
    
    llm = Utils.get_google_llm(GOOGLE_API_KEY)

    prompt_template = PromptTemplate(
                input_variables=["job_requirements", "resume_text"],
                template="""
                You are an expert HR and recruitment specialist. Analyze the resume below against the job requirements.

                Job Requirements:
                {job_requirements}

                Resume:
                {resume_text}

                Provide a structured analysis of how well the resume matches the job requirements. 
                At the end, clearly state a "Suitability Score" as a percentage (0-100%) based on how well the resume aligns with the job.
                Format: Suitability Score: XX%
                """
            )
    chain = (
         RunnableMap({
            "job_requirements": RunnableLambda(lambda x: x),
            "resume_text": RunnableLambda(lambda x: x),})
            | prompt_template
            | llm
            | StrOutputParser()
    )
    return chain
    
# Extract percentage score from analysis text
# Extract percentage score from analysis text
def extract_suitability_score(text):
    match = re.search(r"Suitability Score: (\d{1,3})%", text)
    if match:
        return int(match.group(1))
    return None

def main():
    st.title("Resume Analyzer")
    st.write("Upload your resume and get insights!")

    # Layout with two columns and one for job requirements and one for resume upload
    # set the variables for future use
    col1, col2 = st.columns(2)
    with col1:
        st.header("Job Requirements")
        job_id = st.text_input("Enter Job ID", "job_001")
        job_requirements = st.text_area("Job Requirements", "Enter the job requirements here...", height=300)

    with col2:
        st.header("Resume Upload")
        uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"])

    analysis = None
    if st.button("Analyze Resume") and uploaded_file is not None and job_requirements.strip() != "":
        with st.spinner("Analyzing..."):
            analysis, _ = analyze_resume(uploaded_file, job_requirements, job_id)
            st.header("AI Analysis")
            st.markdown(analysis)
            suitability_score = extract_suitability_score(analysis)
            if suitability_score is not None:
                    st.metric(label="Resume Suitability Score", value=f"{suitability_score}%")
            else:
                st.warning("Analysis Done.")
            Chroma_vectorstore_utils = VectorStoreUtils(app_name="resume_analyzer")
            doc_metadata = {
                    "candidate": os.path.splitext(uploaded_file.name)[0],
                    "job_id": job_id,
                    "source": "resume_analysis"
                }
            Chroma_vectorstore_utils.store_resume_analysis(analysis, doc_metadata)
            st.success("Analysis stored in vector database.")



if __name__ == "__main__":
    main()
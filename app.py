# Install required packages
!pip install crewai gradio PyPDF2 openai

import os
import gradio as gr
from crewai import Agent, Task, Crew, Process
from PyPDF2 import PdfReader
import openai

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "Enter your open api key"

# Custom Document Extraction Tool
def extract_document_text(file_path: str) -> str:
    """Extracts text from legal documents (PDFs and TXT files)"""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        elif file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return "Unsupported file format. Please upload PDF or TXT."
    except Exception as e:
        return f"Error extracting document: {str(e)}"

# Define Agents
document_extractor_agent = Agent(
    role='Document Extractor',
    goal='Extract text from legal documents',
    backstory='Specializes in parsing legal documents and extracting raw text content',
    verbose=True,
    allow_delegation=False
)

clause_analyzer_agent = Agent(
    role='Clause Analyzer',
    goal='Identify and summarize important legal clauses',
    backstory='Expert in legal terminology with experience analyzing contracts',
    verbose=True,
    allow_delegation=False
)

risk_detector_agent = Agent(
    role='Risk Detector',
    goal='Flag potentially risky clauses and explain the risks',
    backstory='Specializes in identifying legal risks and liabilities in contracts',
    verbose=True,
    allow_delegation=False
)

# Gradio UI with improved layout
def analyze_document(file):
    if file is None:
        return "Please upload a legal document", "", ""

    # Handle file input correctly for Gradio
    try:
        # If file is a string (file path), use it directly
        if isinstance(file, str):
            file_path = file
        # If file is a dictionary (newer Gradio versions)
        elif isinstance(file, dict):
            file_path = file['name']
        # If file is a tuple (older Gradio versions)
        elif isinstance(file, tuple):
            file_path = file[0]
        else:
            return "Unsupported file format", "", ""

        # Extract text from the document
        document_text = extract_document_text(file_path)

        # Create separate tasks for each analysis type
        extract_task = Task(
            description=f'Extract text from the uploaded legal document:\n\n{document_text[:8000]}',
            expected_output='Raw text content of the document',
            agent=document_extractor_agent
        )

        summary_task = Task(
            description='Provide a comprehensive summary of the legal document including key parties, subject matter, duration, and main obligations.',
            expected_output='A clear summary of the document',
            agent=clause_analyzer_agent,
            context=[extract_task]
        )

        clauses_task = Task(
            description='Identify and analyze all important clauses in the document including payment terms, confidentiality, termination, liability, and any other significant provisions.',
            expected_output='Detailed analysis of all important clauses',
            agent=clause_analyzer_agent,
            context=[extract_task]
        )

        risks_task = Task(
            description='Identify and flag all potentially risky clauses with explanations of the risks and potential consequences.',
            expected_output='List of risky clauses with risk level and explanations',
            agent=risk_detector_agent,
            context=[extract_task]
        )

        # Create separate crews for each analysis type
        summary_crew = Crew(
            agents=[document_extractor_agent, clause_analyzer_agent],
            tasks=[extract_task, summary_task],
            verbose=True,
            process=Process.sequential
        )

        clauses_crew = Crew(
            agents=[document_extractor_agent, clause_analyzer_agent],
            tasks=[extract_task, clauses_task],
            verbose=True,
            process=Process.sequential
        )

        risks_crew = Crew(
            agents=[document_extractor_agent, risk_detector_agent],
            tasks=[extract_task, risks_task],
            verbose=True,
            process=Process.sequential
        )

        # Run each crew separately
        summary_output = str(summary_crew.kickoff())
        clauses_output = str(clauses_crew.kickoff())
        risks_output = str(risks_crew.kickoff())

        # Clean up the outputs
        document_summary = summary_output.replace("Raw text content of the document", "").strip()
        clause_analysis = clauses_output.replace("Raw text content of the document", "").strip()
        risk_analysis = risks_output.replace("Raw text content of the document", "").strip()

        # Ensure we have content in each section
        if not document_summary:
            document_summary = "No summary available"
        if not clause_analysis:
            clause_analysis = "No clause analysis available"
        if not risk_analysis:
            risk_analysis = "No risk analysis available"

        return document_summary, clause_analysis, risk_analysis

    except Exception as e:
        return f"Error processing document: {str(e)}", "", ""

# Create a more professional UI with gr.Blocks
with gr.Blocks(theme=gr.themes.Soft(), title="Smart Legal Advisor") as demo:
    gr.Markdown("# Smart Legal Advisor")
    gr.Markdown("Upload a legal contract to get a comprehensive analysis of important clauses and potential risks")

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload Legal Document (PDF or TXT)", file_types=[".pdf", ".txt"])
            analyze_btn = gr.Button("Analyze Document", variant="primary")

    with gr.Row():
        with gr.Column():
            with gr.Tabs():
                with gr.TabItem("📄 Document Summary"):
                    summary_output = gr.Markdown(label="Document Summary")
                with gr.TabItem("📋 Clause Analysis"):
                    clauses_output = gr.Markdown(label="Clause Analysis")
                with gr.TabItem("⚠️ Risk Analysis"):
                    risks_output = gr.Markdown(label="Risk Analysis")

    # Set up the button click event
    analyze_btn.click(
        fn=analyze_document,
        inputs=file_input,
        outputs=[summary_output, clauses_output, risks_output]
    )

# Launch the interface
demo.launch(debug=True)

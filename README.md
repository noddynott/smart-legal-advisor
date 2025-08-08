# smart-legal-advisor
AI-powered tool for analyzing legal contracts using CrewAI and Gradio

## Features

- Document extraction from PDF and TXT files
- Clause analysis and summarization
- Risk detection and explanation
- User-friendly interface with separate output sections

## Tech Stack

- CrewAI: For orchestrating specialized AI agents
- OpenAI: For natural language processing
- Gradio: For the web interface
- PyPDF2: For PDF text extraction

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smart-legal-advisor.git
   cd smart-legal-advisor
 
  ## Install the required packages
  pip install -r requirements.txt

  ## Set your OpenAI API key as an environment variable:
  export OPENAI_API_KEY="your-api-key-here"

  ## Run the application
python app.py
Open the provided local URL in your browser

## Usage
Upload a legal document (PDF or TXT).
Click "Analyze Document".
View the results in the three tabs:
Document Summary
Clause Analysis
Risk Analysis

## Project Structure
smart-legal-advisor/
├── app.py                 # Main application script
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## MIT License

Copyright (c) 2023 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


import streamlit as st
import PyPDF2
from langchain_openai import AzureChatOpenAI  # Updated import


st.title("Document Q&A ChatBot")
st.write("Upload a PDF document and ask any questions based on its content.")

# Initialize the Azure OpenAI LLM
llm = AzureChatOpenAI(
    openai_api_version="2024-02-15-preview",
    azure_deployment="FTIDemoGPT",
    temperature=0,
    azure_endpoint="https://ftidemo.openai.azure.com/",
    api_key="d0ec4fa7a1be4b2aa81696cbfe414ad7"
)

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# Function to create the prompt and get the response
# Function to create the prompt and get the response
# Function to create the prompt and get the response
def get_llm_response(document_text, user_query):
    prompt_template = """
    You are an expert in answering questions based on the provided document. 
    The document is passed below:

    Document: {document_text}

    You must only refer to this document when answering the following question:

    Question: {user_query}
    
    Answer:
    """

    # Fill in the prompt with the actual document and question
    prompt = prompt_template.format(document_text=document_text, user_query=user_query)

    # Generate response from LLM using invoke
    response = llm.invoke(prompt)  # Updated method
    
    # Extract the 'content' directly from the response object
    answer = response.content
    
    return answer



# Streamlit UI for uploading PDF and asking questions
def main():

    # Upload document
    uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        document_text = extract_text_from_pdf(uploaded_file)
        st.write("Document successfully uploaded and processed!")

        # User input for asking questions
        user_query = st.text_input("Ask a question about the document:")

        if st.button("Get Answer"):
            if user_query:
                # Generate the LLM response
                answer = get_llm_response(document_text, user_query)
                st.write("Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question to get an answer.")
    else:
        st.info("Please upload a PDF document to start.")

if __name__ == "__main__":
    main()

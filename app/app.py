import streamlit as st
import os
import tempfile
from markitdown import MarkItDown

def parse_document(uploaded_file):
    """Parse uploaded document using MarkItDown"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Initialize MarkItDown and parse document
        md = MarkItDown()
        result = md.convert(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return result.text_content
    
    except Exception as e:
        st.error(f"Error parsing document: {str(e)}")
        return None

def main():
    st.title("Document Analysis with MarkItDown & MLC LLM")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_document" not in st.session_state:
        st.session_state.current_document = None
    
    # File upload section
    st.write("### Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['pdf', 'docx', 'doc']
    )
    
    if uploaded_file is not None:
        with st.spinner("Converting document..."):
            content = parse_document(uploaded_file)
            
            if content:
                st.write("### Document Preview")
                with st.expander("Show document content", expanded=True):
                    st.markdown(content)
                
                # Store content in session state
                st.session_state.current_document = content
                
                # Add system message about successful parsing
                if not st.session_state.messages:
                    st.session_state.messages.append({
                        "role": "system",
                        "content": f"Document '{uploaded_file.name}' has been successfully converted. You can now ask questions about it."
                    })
    
    # Chat interface
    st.write("### Chat with Document")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about the document"):
        # Check if a document has been uploaded
        if not st.session_state.current_document:
            st.warning("Please upload a document first.")
            return
            
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare context from document
        context = st.session_state.current_document
        
        # Create full prompt with context
        full_prompt = f"""Context: {context}

Question: {prompt}

Provide a detailed answer based on the context above. If the question cannot be answered using only the provided context, please say so."""
        
        try:
            # Placeholder for MLC LLM integration
            # For testing purposes, you can replace this with a simple response
            response = "This is a placeholder response. MLC LLM integration will be added later."
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
            
            # Add to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()
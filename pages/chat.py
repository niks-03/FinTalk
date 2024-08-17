#import necessary libraries
import streamlit as st
import tempfile
import logging
import os
######### ############ ########### ########## #############
from streamlit_extras.switch_page_button import switch_page

########## ############ ########### ########### #########
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.agents.agent_toolkits import (VectorStoreToolkit,VectorStoreInfo)
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
#-----------------------------------------------
from langchain.agents import create_react_agent,AgentExecutor
from langchain import hub
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import (BaseChatMessageHistory,InMemoryChatMessageHistory,)
from langchain_core.runnables.history import RunnableWithMessageHistory
#----------------------------------------------

from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core import exceptions as google_exceptions
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from APIKEY import GOOGLE_API_KEY, GOOGLE_API_KEY2, GOOGLE_API_KEY3, GOOGLE_API_KEY4
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
import random
#==================----------------
from datetime import datetime
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/nikhil_db')
db = client['chatbot']
collection = db["conversations"]
interaction_time = datetime.now().strftime("%d-%m-%Y")

############ ############# ############# ############

########### ############ ############# ##############
    
def get_user(user_name):
    st.session_state.user_id = user_name
    print("user name stored")

def main():
    def store_response(query, response):
        # Find the document to update
        user_id = st.session_state.user_id
        user = {"user_id": user_id}

        new_conversation = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": response}
        ]

        update = {
            "$push": {
                "conversation": {
                    "$each": new_conversation
                }
            }
        }

        user_document = collection.find_one(user)
        if user_document:
            if user_document["time"]==interaction_time:
                collection.update_one(user, update)
                print("updated")
        else:
            collection.insert_one({"user_id":user_id, "time":interaction_time, "conversation":[]})
            collection.update_one(user, update)
            print("created")

    #Read and divide pdf data
    def process_pdf(file):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        loader = PyPDFLoader(file_path=tmp_file_path)
        pages = loader.load_and_split() 
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(pages)
        os.unlink(tmp_file_path)  # Delete the temporary file
        print("done process pdf")
        return chunks

    #store pdf data in chromadb
    def process_and_store_paragraphs(chunks):
        try:
            google_ef = HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v1")
            print("inside embed try ")
        except Exception as e:
            print("\n\nembedding fun",e,"\n\n")
        try:
            store = Chroma.from_documents(documents=chunks,
                                    embedding=google_ef,
                                    persist_directory="./chroma_db",
                                    collection_name="report_v1")

            print("inside store try ")
        except Exception as e:
            print("\n\nstore",e,"\n\n")
        print("done process and store para")
        return store, google_ef


    #get context from chromadb for query
    def get_context(store, google_ef, query):
        context = ""
        query_emb = google_ef.embed_query(query)
        result = store.similarity_search_by_vector_with_relevance_scores(query_emb, k=5)
        for doc, score in result:
            context += doc.page_content + "\n\n"
            context=context.replace('  ','')
        print("done get_context")
        return context

    #define tool for summarization
    def get_summarize_tool( llm, chunks):
        summarize_template = """You are a helpful AI assistant. Your task is to summarize the given text based on the following points:
                            1. What is the document about?
                            2. What does it contain?

                            Please provide a concise summary and also explain the second point briefly and its key terms in the final output .

                            Text to summarize:
                            {chunks}

                            Summary:
                            """
        
        summarize_prompt = PromptTemplate(
            input_variables=["chunks"],
            template=summarize_template
        )

        summarize_chain = summarize_prompt | llm

        def summarize_with_chain(query):
            return summarize_chain.invoke(chunks)

        summarize_tool = Tool.from_function(
                name="Summarize Document",
                func=summarize_with_chain,
                description="Use this tool when asked to summarize the document or provide an overview.")
        
        # vector_store_tools = toolkit.get_tools()
        # tools = vector_store_tools + [summarize_tool]

        return summarize_tool

    #get LLM response for query
    def get_llm_response(query, store, memory,reg_conv_memory, context, chunks):
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.3,
            top_p=0.85,
            top_k=40,
            n=1,
            max_retries=3,
            timeout=0.30,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH : HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE ,
                HarmCategory.HARM_CATEGORY_HARASSMENT : HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE}
            )
        

        st_callback = StreamlitCallbackHandler(st.container())

        #define tool for financial queries
        if store is not None:
            print("\n\n","INSIDE STORE RESPONSE","\n\n")

            vectorstoreinfo = VectorStoreInfo(name="financial_analysis",
                                        description="Comprehensive financial report analysis tool for banking and corporate finance",
                                        vectorstore=store)
            
            toolkit = VectorStoreToolkit(vectorstore_info=vectorstoreinfo,llm=llm)

            base_prompt = """You are a helpful financial analyst AI assistant. Your task is to answer questions based on the given context, which is derived from an uploaded document. If asked to explain, elaborate the terms in your final answer.
                    Always use the information provided in the context to answer the query. This context represents the content of the uploaded document.
                    
                    Answer the following questions as best you can. You have access to the following tools:
                    {tools}
                    
                    When answering queries:
                    1. Provide accurate and relevant information from the uploaded document.
                    2. Use financial terminology appropriately.
                    3. If asked for calculations or comparisons, double-check your math.
                    4. If the information is not in the uploaded document, clearly state that.
                    5. Offer concise but comprehensive answers, and ask if the user needs more details.
                    6. If applicable, mention any important caveats or contexts for the financial data.
                    7. While explaining terms, explain them in short way to minimize number of tokens.

                    Use the following format:

                    Question: the input question you must answer
                    Thought: you should always think about what to do and Do I need to use a tool? 
                    Action: the action to take, should be one of {tool_names}
                    
                    Final Answer: the final answer to the original input question

                    Begin!
                    Question: {input}
                    context:{context}
                    chat_history: {memory}
                    Thought:{agent_scratchpad}
                    """
            
            summarize_tool = get_summarize_tool(llm, chunks)
            tools = toolkit.get_tools()+ [summarize_tool]

            prompt = PromptTemplate.from_template(base_prompt,partial_variables={"context":context,"memory":memory.buffer})

            agent = create_react_agent(llm, tools, prompt=prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory,handle_parsing_errors=True)
            
            # print(memory.buffer)
            response = agent_executor.invoke({"input": query}, {"callbacks": [st_callback]})
            
            store_response(query, response["output"])
            return response["output"]




        #define tool for regular conversation 
        else:
            print("\n\n","INSIDE REGULAR RESPONSE","\n\n")

            def get_regconv_session_history(session_id: str) -> BaseChatMessageHistory:
                if session_id not in reg_conv_memory:
                    reg_conv_memory[session_id] = InMemoryChatMessageHistory()
                return reg_conv_memory[session_id]

            llm_chain = RunnableWithMessageHistory(llm, get_regconv_session_history)
            with st.spinner("Generating response..."):
                response = llm_chain.invoke([HumanMessage(content=query)],config={"configurable": {"session_id": "abc2"}},)
            
            store_response(query, response.content)
            return response.content
    #======================================================================

    #initialize states
    if 'chunks' not in st.session_state:
        st.session_state.chunks = None
    if 'store' not in st.session_state:
        st.session_state.store = None
    if 'google_ef' not in st.session_state:
        st.session_state.google_ef = None
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationBufferWindowMemory(k=10, return_messages=True, memory_key="chat_history")
    if "reg_conv_memory" not in st.session_state:    
        st.session_state.reg_conv_memory = {}
    if "messages" not in st.session_state:
        st.session_state.messages = [{'role': 'assistant', 'content': """Hello! 👋  Welcome to Your AI Financial Assistant! I'm here to help you analyze and understand your financial documents."""}]
    if "key" not in st.session_state:
        st.session_state.key = str(random.randint(1000, 1000000000))

    #======================================================================

    #Title
    # st.title("FinTalk")
    col1, col2 = st.columns([6,1])
    with col1:
        st.title("FinTalk")
    with col2:
        st.image("E:\\Nikhil\\Cognizant\\main3\\images\\logo.png")


    # Query input and processing
    query = st.chat_input("Enter your query")

    #=======================================================================
    options = st.radio("Data Usage", index=0,options=["Chat", "Visualize"], horizontal=True, label_visibility="collapsed")

    if options == "Visualize":
        switch_page("charts")

    #Get file from user
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=False, label_visibility='collapsed', key=st.session_state.key)

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        
    # Process uploaded file
    if uploaded_file is not None and st.session_state.store is None:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            st.session_state.chunks = process_pdf(uploaded_file)
            st.session_state.store, st.session_state.google_ef = process_and_store_paragraphs(st.session_state.chunks)
        st.success("File processed successfully!")
    #=======================================================================

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    #=======================================================================

    if query:

        #append query to the message session
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        #Get context from PDF
        if st.session_state.store is not None:
            context = get_context(st.session_state.store, st.session_state.google_ef, query)
        else:
            context = None
        
        #Get response from LLM
        try:
            response = get_llm_response(query, st.session_state.store, st.session_state.memory, st.session_state.reg_conv_memory,context, st.session_state.chunks)
        except google_exceptions.ResourceExhausted as e:
            st.error("API quota exceeded. Please try again later")
            logging.error(f"ResourceExhausted error: {e}")
            response = "Wait for atleast 1 minute to use Bot again!"
        
        #Write LLM response on APP
        with st.chat_message("assistant"):
            st.write(response)
        
        #ADD response to the messages session
        st.session_state.messages.append({"role": "assistant", "content": response})
        


    #remove all the sessions to clear memory
    if st.button(label="Clear File") and 'key' in st.session_state.keys():
        st.session_state.pop('key')
        st.session_state.store.delete_collection()
        st.session_state.store = None
        st.session_state.chunks = None
        st.session_state.memory = ConversationBufferWindowMemory(k=10, return_messages=True, memory_key="chat_history")
        st.rerun()

if __name__=="__main__":
    main()
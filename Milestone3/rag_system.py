# RAG (Retrieval-Augmented Generation) system for the AI-Based Smart File Assistant
import os
from config import Config
from pinecone_manager import get_user_pinecone_index
from embeddings import generate_embedding_miniLM
from database import get_db

# Try to import LangChain components for advanced RAG
try:
    from langchain_pinecone import PineconeVectorStore
    from langchain_openai import ChatOpenAI
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain.chains.retrieval import create_retrieval_chain
    from langchain.chains.history_aware_retriever import create_history_aware_retriever
    from langchain_community.chat_message_histories import SQLChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
    LANGCHAIN_AVAILABLE = True
    print("✅ LangChain RAG components loaded successfully")
except ImportError as e:
    print(f"⚠️  LangChain RAG not fully available: {e}")
    # Try alternative imports for newer versions
    try:
        from langchain_pinecone import PineconeVectorStore
        from langchain_openai import ChatOpenAI
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_community.chat_message_histories import SQLChatMessageHistory
        from langchain_core.runnables.history import RunnableWithMessageHistory
        LANGCHAIN_AVAILABLE = True
        print("✅ LangChain RAG components loaded successfully (alternative imports)")
    except ImportError as e2:
        print(f"⚠️  LangChain RAG not available: {e2}")
        LANGCHAIN_AVAILABLE = False

# Legal document prompt template (from Milestone2)
SYSTEM_TEMPLATE = """
You are LegaBot, a precise legal research assistant designed to help users find authoritative legal provisions, rules, and relevant case law. You must follow these guidelines strictly:

## PRIMARY RESPONSIBILITIES:
1. **Retrieve and Cite**: Always reference the most relevant statute sections, judgment excerpts, or legal provisions from the retrieved documents
2. **Provide Clear Summaries**: Offer concise, accurate legal summaries in 3-5 sentences
3. **Maintain Transparency**: Show exactly which document chunks were used in your response
4. **Handle Uncertainty Appropriately**: When uncertain, list relevant sections and recommend consulting qualified legal counsel

## RESPONSE FORMAT:
For every query, structure your response as follows:

**RELEVANT LEGAL PROVISIONS:**
- [Document Title] | [Section/Page] | [Date if available]
  Excerpt: [Direct quote from the source, maximum 2-3 sentences]

**LEGAL SUMMARY:**
[Provide a concise 3-5 sentence explanation based on the retrieved sources]

**CITATIONS & SOURCES:**
- Source 1: [Document name, section, page/chunk ID]
- Source 2: [Document name, section, page/chunk ID]
[List all sources used]

## MANDATORY DISCLAIMERS:
- Always include: "⚖️ **Legal Disclaimer**: This information is for research purposes only. I am not a licensed attorney, and this does not constitute legal advice. For matters affecting your legal rights, please consult a qualified attorney."
- When interpretation is required: "This matter may require legal interpretation that could affect your rights. Please consult a qualified attorney for personalized advice."
- For complex cases: "Given the complexity of this legal matter, I strongly recommend consulting with a legal professional who can review your specific circumstances."

## SPECIFIC INSTRUCTIONS:
1. **Quote Exactly**: Use direct quotes from statutes, codes (IPC, CrPC), and judgments
2. **Cite Precisely**: Include document title, section number, and chunk ID for each reference
3. **Stay Current**: If referring to legal provisions, mention the version or date when available
4. **Be Concise**: Keep summaries focused and actionable
5. **Handle Follow-ups**: Use previous conversation context to provide coherent, connected responses
6. **Acknowledge Limits**: If you cannot find relevant information, clearly state this and suggest alternative approaches

## TONE AND STYLE:
- Professional and authoritative, but accessible
- Use legal terminology correctly but explain complex terms
- Be direct and factual, avoiding speculation
- Maintain confidence in citing sources while being humble about interpretations

## QUERY TYPES TO HANDLE:
- Statutory interpretation questions
- Case law searches
- Legal procedure inquiries  
- Definitions of legal terms
- Penalty and punishment queries
- Rights and obligations questions
- Legal process explanations

Remember: Your primary role is to be a precise legal research tool that connects users with authoritative legal sources while maintaining clear boundaries about what constitutes legal advice.
"""

def query_user_documents(user_id, query_text, top_k=5):
    """Query user's specific documents using their Pinecone index"""
    try:
        print(f"🔍 Querying documents for user {user_id}: {query_text}")
        
        # Get user's Pinecone index
        index = get_user_pinecone_index(user_id)
        if not index:
            print(f"❌ No Pinecone index found for user {user_id}")
            return []
        
        # Generate embedding for the query
        query_embedding = generate_embedding_miniLM(query_text)
        if not query_embedding:
            print(f"❌ Failed to generate embedding for query: {query_text}")
            return []
        
        print(f"✅ Generated query embedding (dimension: {len(query_embedding)})")
        
        # Query Pinecone with user filter
        query_results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={"user_id": user_id}  # Only get this user's documents
        )
        
        print(f"📊 Pinecone returned {len(query_results.matches)} results")
        
        # Format results
        results = []
        for match in query_results.matches:
            if match.score > 0.1:  # Minimum relevance threshold
                result = {
                    'id': match.id,
                    'score': match.score,
                    'filename': match.metadata.get('filename', 'Unknown'),
                    'text': match.metadata.get('text', ''),
                    'chunk_index': match.metadata.get('chunk_index', 0),
                    'total_chunks': match.metadata.get('total_chunks', 1),
                    'user_id': match.metadata.get('user_id', user_id)
                }
                results.append(result)
                print(f"✅ Result {len(results)}: {result['filename']} (score: {result['score']:.3f})")
        
        print(f"🎯 Returning {len(results)} relevant results for user {user_id}")
        return results
        
    except Exception as e:
        print(f"❌ Error querying user documents: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def generate_rag_response(user_id, query_text, search_results):
    """Generate a proper RAG response using only the user's uploaded documents"""
    try:
        if not search_results:
            return {
                "answer": f"I couldn't find any relevant information about '{query_text}' in your uploaded documents. Please ensure you have uploaded documents related to your question, or try rephrasing your query with different keywords.",
                "sources": [],
                "disclaimer": "⚖️ **Information Disclaimer**: No relevant documents found for this query. Please upload relevant documents or rephrase your question."
            }
        
        # Use a reasonable threshold - accept results with decent relevance
        results_to_use = [r for r in search_results if r['score'] > 0.2][:5]  # Top 5 with score > 0.2
        
        if not results_to_use:
            return {
                "answer": f"I found some content in your documents, but it doesn't seem closely related to '{query_text}'. Please try rephrasing your question or upload more relevant documents.",
                "sources": [],
                "disclaimer": "⚖️ **Information Disclaimer**: Low relevance results found. Consider rephrasing your question."
            }
        
        # Prepare context from retrieved documents
        context_parts = []
        sources_used = []
        
        for i, result in enumerate(results_to_use, 1):
            filename = result['filename']
            score = result['score']
            text_content = result['text']
            
            context_parts.append(f"Document {i} ({filename}):\n{text_content}\n")
            
            sources_used.append({
                "filename": filename,
                "chunk_index": result['chunk_index'],
                "total_chunks": result['total_chunks'],
                "relevance_score": score
            })
        
        # Combine all context
        full_context = "\n".join(context_parts)
        
        # Generate AI response using OpenAI if available
        try:
            from openai import OpenAI
            if Config.OPENAI_API_KEY:
                client = OpenAI(api_key=Config.OPENAI_API_KEY)
                
                # Create a focused prompt for the specific query
                prompt = f"""You are LegaBot, a precise legal research assistant. Based on the following document excerpts, provide a comprehensive answer to the user's question.

User Question: {query_text}

Retrieved Document Context:
{full_context}

Instructions:
1. Provide a clear, specific answer based ONLY on the provided context
2. Use the EXACT format shown below
3. Keep the summary concise but comprehensive
4. List sources at the end

REQUIRED FORMAT:

**SUMMARY:**
[Provide a clear, comprehensive paragraph explaining the answer based on the context. Write in complete sentences and make it informative but concise.]

Sources:
📄 [Document name 1]
📄 [Document name 2]
"""
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a legal research assistant that provides accurate information based on provided legal documents."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                
                ai_answer = response.choices[0].message.content
                
                return {
                    "answer": ai_answer,
                    "sources": sources_used,
                    "disclaimer": f"AI-generated response based on your uploaded documents - {len(results_to_use)} relevant sections analyzed"
                }
                
        except Exception as e:
            print(f"⚠️  OpenAI generation failed: {e}, falling back to basic response")
        
        # Fallback to basic response if OpenAI fails
        response_parts = []
        
        # Summary section (like in the screenshot)
        response_parts.append("**SUMMARY:**")
        
        # Create a comprehensive summary paragraph
        if len(results_to_use) > 0:
            # Take the most relevant result and create a focused summary
            main_result = results_to_use[0]
            summary_text = main_result['text']
            
            # Try to extract the most relevant sentences
            sentences = summary_text.split('.')
            relevant_sentences = []
            query_words = query_text.lower().split()
            
            for sentence in sentences[:8]:  # Check more sentences for better context
                sentence_lower = sentence.lower()
                if any(word in sentence_lower for word in query_words):
                    relevant_sentences.append(sentence.strip())
            
            if relevant_sentences:
                # Create a comprehensive paragraph
                summary_paragraph = '. '.join(relevant_sentences[:4]) + '.'
                response_parts.append(summary_paragraph)
            else:
                # Use the main content but make it more readable
                clean_text = summary_text.replace('\n', ' ').replace('  ', ' ').strip()
                if len(clean_text) > 400:
                    clean_text = clean_text[:400] + "..."
                response_parts.append(clean_text)
        
        response_parts.append("")  # Empty line
        
        # Sources section (like in the screenshot)
        response_parts.append("Sources:")
        
        # List unique sources with document icon
        unique_sources = []
        for result in results_to_use:
            source_name = result['filename'].replace('.docx', '').replace('.pdf', '').replace('_', ' ')
            if source_name not in unique_sources:
                unique_sources.append(source_name)
        
        for source in unique_sources[:3]:  # Limit to 3 sources
            response_parts.append(f"📄 {source}")
        
        # Add a simple disclaimer at the end
        response_parts.append("")
        response_parts.append("*Information extracted from your uploaded documents for research purposes.*")
        
        final_response = "\n".join(response_parts)
        
        return {
            "answer": final_response,
            "sources": sources_used,
            "disclaimer": f"Document-based response from your uploaded files - {len(results_to_use)} relevant sections found"
        }
        
    except Exception as e:
        print(f"❌ Error generating RAG response: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "answer": "I encountered an error while processing your query. Please try again or contact support if the issue persists.",
            "sources": [],
            "disclaimer": "⚖️ **Error**: Unable to process query at this time."
        }

# Advanced RAG Chain Functions (LangChain-based)

def load_rag_chain(user_id):
    """Loads all the necessary components for the RAG chain for a specific user.
    This is cached to avoid reloading models and connections."""
    print("Loading RAG chain resources...")
    
    if not Config.PINECONE_API_KEY or not Config.OPENAI_API_KEY:
        raise ValueError("PINECONE_API_KEY and/or OPENAI_API_KEY not found in .env file")
    
    if not LANGCHAIN_AVAILABLE:
        print("⚠️  LangChain not available, falling back to basic RAG")
        return None
    
    try:
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Initialize LLM
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, streaming=False)
        
        # Get user's individual Pinecone index name
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT index_name FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result or not result[0]:
            print(f"❌ No Pinecone index found for user {user_id}")
            return None
        
        INDEX_NAME = result[0]
        print(f"🔍 Connecting to Pinecone index: {INDEX_NAME}")
        
        # Create vectorstore from existing index
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=INDEX_NAME,
            embedding=embeddings
        )
        print(f"✅ Connected to vectorstore successfully")
        
        # Create retriever
        retriever = vectorstore.as_retriever(k=5)
        print(f"✅ Created retriever with k=5")
        
        # Create history-aware retriever prompt
        rephrase_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a concise, standalone search query...")
        ])
        
        # Create history-aware retriever
        history_aware_retriever = create_history_aware_retriever(llm, retriever, rephrase_prompt)
        
        # Create final prompt template
        final_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_TEMPLATE + "\n\n**Context from retrieved documents:**\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
        
        # Create question-answer chain
        question_answer_chain = create_stuff_documents_chain(llm, final_prompt)
        
        # Create retrieval chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        
        print("RAG chain loaded successfully.")
        return rag_chain
        
    except Exception as e:
        print(f"❌ Error loading RAG chain: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def get_session_history(session_id: str):
    """Creates and returns an SQLChatMessageHistory object for a given session ID.
    This connects to the SQLite database for persistent chat history."""
    try:
        # Use the main application database for chat history
        connection_string = f"sqlite:///{Config.DB_NAME}"
        return SQLChatMessageHistory(session_id=session_id, connection_string=connection_string)
    except Exception as e:
        print(f"❌ Error creating session history: {str(e)}")
        return None

def get_conversational_rag_chain(user_id):
    """Get the conversational RAG chain with persistent memory for a user"""
    try:
        # Get the base RAG chain
        rag_chain = load_rag_chain(user_id)
        if not rag_chain:
            return None
        
        # Create the conversational chain with persistent, SQL-backed memory
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        
        return conversational_rag_chain
        
    except Exception as e:
        print(f"❌ Error creating conversational RAG chain: {str(e)}")
        return None

def query_with_advanced_rag(user_id, query_text):
    """Query using the advanced RAG chain with conversational memory"""
    try:
        if not LANGCHAIN_AVAILABLE:
            print("⚠️  Using basic RAG fallback")
            return query_with_basic_rag(user_id, query_text)
        
        # Get conversational RAG chain
        conversational_rag_chain = get_conversational_rag_chain(user_id)
        if not conversational_rag_chain:
            print("⚠️  Falling back to basic RAG")
            return query_with_basic_rag(user_id, query_text)
        
        # Create session ID for this user
        session_id = f"user_{user_id}_session"
        
        # Load existing history and display past messages (like in your code)
        try:
            history = get_session_history(session_id)
            if history:
                print(f"📚 Loaded {len(history.messages)} previous messages for user {user_id}")
        except Exception as e:
            print(f"⚠️  Could not load chat history: {e}")
        
        # Invoke the conversational RAG chain
        print(f"🔍 Querying with advanced RAG for user {user_id}: {query_text}")
        
        result = conversational_rag_chain.invoke(
            {"input": query_text},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Extract answer and sources
        answer = result.get("answer", "")
        context = result.get("context", [])
        
        # Format sources from context with better metadata
        sources = []
        for i, doc in enumerate(context):
            if hasattr(doc, 'metadata'):
                source_info = {
                    "filename": doc.metadata.get("filename", "Unknown"),
                    "chunk_index": doc.metadata.get("chunk_index", i),
                    "total_chunks": doc.metadata.get("total_chunks", 1),
                    "user_id": doc.metadata.get("user_id", user_id),
                    "relevance_score": 0.9,  # High relevance since it came from LangChain retrieval
                    "text": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                }
                sources.append(source_info)
        
        print(f"✅ Advanced RAG completed with {len(sources)} sources")
        
        return {
            "success": True,
            "answer": answer,
            "sources": sources,
            "total_results": len(sources),
            "method": "advanced_rag_with_history"
        }
        
    except Exception as e:
        print(f"❌ Error with advanced RAG: {str(e)}")
        import traceback
        traceback.print_exc()
        print("⚠️  Falling back to basic RAG")
        return query_with_basic_rag(user_id, query_text)

def query_with_basic_rag(user_id, query_text):
    """Fallback to basic RAG using the existing implementation"""
    try:
        # Use existing basic RAG implementation
        results = query_user_documents(user_id, query_text, top_k=5)
        rag_response = generate_rag_response(user_id, query_text, results)
        
        return {
            "success": True,
            "answer": rag_response.get("answer", ""),
            "sources": rag_response.get("sources", []),
            "total_results": len(results),
            "method": "basic_rag"
        }
        
    except Exception as e:
        print(f"❌ Error with basic RAG: {str(e)}")
        return {
            "success": False,
            "answer": "I encountered an error while processing your query. Please try again.",
            "sources": [],
            "total_results": 0,
            "method": "error"
        }
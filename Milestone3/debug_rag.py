#!/usr/bin/env python3
"""
Debug script to test RAG functionality
"""

import os
import sys
from database import get_db
from pinecone_manager import get_user_pinecone_index, check_user_pinecone_stats
from rag_system import query_user_documents, generate_rag_response

def debug_user_documents(user_id=1):
    """Debug function to check user documents and Pinecone data"""
    print(f"🔍 Debugging RAG for user {user_id}")
    
    # Check database for user documents
    print("\n📊 Checking database for user documents...")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, original_filename, file_size, upload_date, processing_stats
        FROM documents 
        WHERE user_id = ?
        ORDER BY upload_date DESC
    """, (user_id,))
    
    docs = cursor.fetchall()
    print(f"Found {len(docs)} documents in database:")
    for doc in docs:
        print(f"  - ID: {doc[0]}, File: {doc[1]}, Size: {doc[2]}, Date: {doc[3]}")
    
    # Check Pinecone index
    print(f"\n🔍 Checking Pinecone index for user {user_id}...")
    index = get_user_pinecone_index(user_id)
    if index:
        print("✅ Pinecone index found")
        stats = check_user_pinecone_stats(user_id)
        print(f"Pinecone stats: {stats}")
    else:
        print("❌ No Pinecone index found")
        return
    
    # Test query
    print(f"\n🔍 Testing query...")
    test_query = "what is indian penal code"
    print(f"Query: {test_query}")
    
    results = query_user_documents(user_id, test_query, top_k=3)
    print(f"Found {len(results)} results:")
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Score: {result['score']:.3f}")
        print(f"  Filename: {result['filename']}")
        print(f"  Text preview: {result['text'][:200]}...")
    
    # Test RAG response generation
    print(f"\n🤖 Testing RAG response generation...")
    rag_response = generate_rag_response(user_id, test_query, results)
    print(f"RAG Response:")
    print(f"Answer: {rag_response['answer'][:500]}...")
    print(f"Sources: {len(rag_response['sources'])}")
    
    conn.close()

if __name__ == "__main__":
    debug_user_documents()
# API routes for the AI-Based Smart File Assistant
import os
import json
from flask import request, jsonify, session
from werkzeug.utils import secure_filename
from auth import require_auth
from database import get_db, save_chat_message, get_user_chat_history
from document_processor import process_document_for_user
from rag_system import query_with_advanced_rag
from pinecone_manager import check_user_pinecone_stats
from config import Config, allowed_file

def register_api_routes(app):
    """Register API routes"""
    
    @app.route("/api/pinecone-stats")
    @require_auth
    def get_pinecone_stats():
        """Get Pinecone statistics for current user"""
        # Get user ID from session
        if "user_id" in session:
            user_id = session["user_id"]
        else:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            user_id = user["id"]
        
        stats = check_user_pinecone_stats(user_id)
        return jsonify(stats), 200

    @app.route("/api/upload", methods=["POST"])
    @require_auth
    def upload_file():
        """Handle file upload and processing"""
        try:
            print("🚀 Upload API called")
            
            # Get user ID from session
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
                user = cursor.fetchone()
                conn.close()
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                user_id = user["id"]
            
            print(f"📋 User ID: {user_id}")
            
            # Check if files were uploaded
            if 'files' not in request.files:
                print("❌ No files in request")
                return jsonify({"error": "No files uploaded"}), 400
            
            files = request.files.getlist('files')
            print(f"📁 Number of files received: {len(files)}")
            
            if not files or all(file.filename == '' for file in files):
                print("❌ No files selected")
                return jsonify({"error": "No files selected"}), 400
            
            # Ensure upload directory exists
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            
            uploaded_files = []
            processing_results = []
            
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    print(f"📄 Processing file: {file.filename}")
                    
                    # Secure the filename
                    filename = secure_filename(file.filename)
                    original_filename = file.filename
                    
                    # Create unique filename to avoid conflicts
                    import time
                    timestamp = int(time.time())
                    name, ext = os.path.splitext(filename)
                    unique_filename = f"{name}_{timestamp}{ext}"
                    
                    # Save file
                    file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
                    file.save(file_path)
                    
                    # Get file info
                    file_size = os.path.getsize(file_path)
                    file_type = filename.rsplit('.', 1)[1].lower()
                    
                    print(f"💾 File saved: {file_path} ({file_size} bytes)")
                    
                    # Process document for RAG
                    print(f"🔄 Starting document processing...")
                    processing_result = process_document_for_user(user_id, file_path, original_filename)
                    processing_results.append(processing_result)
                    
                    # Save to database
                    conn = get_db()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO documents (user_id, filename, original_filename, file_path, file_size, file_type, processing_stats)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, unique_filename, original_filename, file_path, file_size, file_type, json.dumps(processing_result)))
                    
                    doc_id = cursor.lastrowid
                    conn.commit()
                    conn.close()
                    
                    uploaded_files.append({
                        "id": doc_id,
                        "filename": unique_filename,
                        "original_filename": original_filename,
                        "file_size": file_size,
                        "file_type": file_type,
                        "processing_result": processing_result
                    })
                    
                    print(f"✅ File processed and saved to database: {original_filename}")
                else:
                    print(f"❌ Invalid file: {file.filename if file else 'None'}")
            
            if uploaded_files:
                successful_count = len([r for r in processing_results if r.get("success", False)])
                total_count = len(uploaded_files)
                
                return jsonify({
                    "message": f"Successfully uploaded and processed {successful_count}/{total_count} files",
                    "files": uploaded_files,
                    "processing_results": processing_results
                }), 200
            else:
                return jsonify({"error": "No valid files were uploaded"}), 400
                
        except Exception as e:
            print(f"❌ Upload error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Upload failed: {str(e)}"}), 500

    @app.route("/api/documents", methods=["GET"])
    @require_auth
    def get_user_documents():
        """Get list of user's uploaded documents"""
        try:
            # Get user ID from session
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
                user = cursor.fetchone()
                conn.close()
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                user_id = user["id"]
            
            # Get user's documents
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, filename, original_filename, file_path, file_size, file_type, upload_date, processing_stats
                FROM documents 
                WHERE user_id = ? 
                ORDER BY upload_date DESC
            """, (user_id,))
            
            documents = []
            for row in cursor.fetchall():
                # Parse processing stats
                processing_stats = None
                if row[7]:  # processing_stats column
                    try:
                        processing_stats = json.loads(row[7])
                    except:
                        processing_stats = None
                
                documents.append({
                    "id": row[0],
                    "filename": row[1],
                    "original_filename": row[2],
                    "file_path": row[3],
                    "file_size": row[4],
                    "file_type": row[5],
                    "upload_date": row[6],
                    "processing_stats": processing_stats
                })
            
            conn.close()
            
            return jsonify({
                "documents": documents,
                "total": len(documents)
            }), 200
            
        except Exception as e:
            print(f"❌ Error fetching documents: {str(e)}")
            return jsonify({"error": f"Failed to fetch documents: {str(e)}"}), 500

    @app.route("/api/documents/<int:doc_id>", methods=["DELETE"])
    @require_auth
    def delete_document(doc_id):
        """Delete a user's document"""
        try:
            # Get user ID from session
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
                user = cursor.fetchone()
                conn.close()
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                user_id = user["id"]
            
            # Get document info and verify ownership
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT file_path, user_id FROM documents WHERE id = ?", (doc_id,))
            doc = cursor.fetchone()
            
            if not doc:
                conn.close()
                return jsonify({"error": "Document not found"}), 404
            
            if doc[1] != user_id:
                conn.close()
                return jsonify({"error": "Access denied"}), 403
            
            file_path = doc[0]
            
            # Delete from database
            cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            conn.commit()
            conn.close()
            
            # Delete physical file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"🗑️  Deleted file: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not delete file {file_path}: {e}")
            
            return jsonify({"message": "Document deleted successfully"}), 200
            
        except Exception as e:
            print(f"❌ Error deleting document: {str(e)}")
            return jsonify({"error": f"Failed to delete document: {str(e)}"}), 500

    @app.route("/api/query", methods=["POST"])
    @require_auth
    def query_documents():
        """Query user's documents using advanced RAG chain with conversational memory"""
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "Query text is required"}), 400
            
            query_text = data['query'].strip()
            if not query_text:
                return jsonify({"error": "Query text cannot be empty"}), 400
            
            # Get user ID from session
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
                user = cursor.fetchone()
                conn.close()
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                user_id = user["id"]
            
            print(f"🔍 Query from user {user_id}: {query_text}")
            
            # Save user message to chat history
            save_chat_message(user_id, "user", query_text)
            
            # Query using advanced RAG system
            result = query_with_advanced_rag(user_id, query_text)
            
            if result["success"]:
                # Save bot response to chat history
                save_chat_message(user_id, "bot", result["answer"])
                
                return jsonify({
                    "answer": result["answer"],
                    "sources": result["sources"],
                    "total_results": result["total_results"],
                    "method": result["method"]
                }), 200
            else:
                return jsonify({
                    "error": "Failed to process query",
                    "answer": result["answer"]
                }), 500
                
        except Exception as e:
            print(f"❌ Query error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({"error": f"Query failed: {str(e)}"}), 500

    @app.route("/api/chat-history", methods=["GET"])
    @require_auth
    def get_chat_history_api():
        """Return the current user's stored chat history"""
        try:
            # Get user ID from session
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
                user = cursor.fetchone()
                conn.close()
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                user_id = user["id"]
            
            # Get chat history
            history = get_user_chat_history(user_id, limit=50)
            
            return jsonify({
                "history": history,
                "total": len(history)
            }), 200
            
        except Exception as e:
            print(f"❌ Error getting chat history: {str(e)}")
            return jsonify({"error": f"Failed to get chat history: {str(e)}"}), 500

    @app.route("/api/clear-chat-history", methods=["POST"])
    @require_auth
    def clear_chat_history():
        """Clear the current user's chat history"""
        try:
            # Get user ID from session
            if "user_id" in session:
                user_id = session["user_id"]
            else:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE first_name = ?", (session["user_name"],))
                user = cursor.fetchone()
                conn.close()
                
                if not user:
                    return jsonify({"error": "User not found"}), 404
                
                user_id = user["id"]
            
            # Clear chat history
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return jsonify({
                "message": f"Cleared {deleted_count} chat messages",
                "deleted_count": deleted_count
            }), 200
            
        except Exception as e:
            print(f"❌ Error clearing chat history: {str(e)}")
            return jsonify({"error": f"Failed to clear chat history: {str(e)}"}), 500

    # Admin routes
    @app.route("/admin/ensure-indexes")
    def admin_ensure_indexes():
        """Admin route to ensure all users have Pinecone indexes"""
        from pinecone_manager import ensure_all_users_have_indexes
        try:
            result = ensure_all_users_have_indexes()
            if result:
                return jsonify({"message": "Successfully ensured all users have Pinecone indexes"}), 200
            else:
                return jsonify({"error": "Failed to ensure indexes for some users"}), 500
        except Exception as e:
            return jsonify({"error": f"Admin operation failed: {str(e)}"}), 500

    @app.route("/admin/debug-documents")
    def debug_documents():
        """Debug route to check all documents in database"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, d.user_id, d.original_filename, d.file_size, d.upload_date, u.email
                FROM documents d
                LEFT JOIN users u ON d.user_id = u.id
                ORDER BY d.upload_date DESC
            """)
            
            documents = []
            for row in cursor.fetchall():
                documents.append({
                    "id": row[0],
                    "user_id": row[1],
                    "filename": row[2],
                    "file_size": row[3],
                    "upload_date": row[4],
                    "user_email": row[5]
                })
            
            conn.close()
            
            return jsonify({
                "documents": documents,
                "total": len(documents)
            }), 200
            
        except Exception as e:
            return jsonify({"error": f"Debug failed: {str(e)}"}), 500
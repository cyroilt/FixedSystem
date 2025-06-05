from flask import Flask, request, jsonify, send_from_directory, g, render_template, redirect, url_for, flash, session,send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime, timedelta
import uuid
import json
import atexit
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DATABASE'] = 'faculty.db'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'

jwt = JWTManager(app)
CORS(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database helper functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db_1(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_db(error):
    close_db_1(error)

def init_db():
    db = sqlite3.connect(app.config['DATABASE'])
    cursor = db.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            image_path TEXT,
            video_path TEXT,
            category_id INTEGER,
            author_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            views INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recording_tags (
            recording_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (recording_id, tag_id),
            FOREIGN KEY (recording_id) REFERENCES recordings (id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
        )
    ''')
    
    # Insert default categories
    default_categories = [
        "Учебная деятельность",
        "Научная деятельность", 
        "Служебная деятельность",
        "Работа с личным составом",
        "Спортивная деятельность"
    ]
    
    for cat_name in default_categories:
        cursor.execute('SELECT id FROM categories WHERE name = ?', (cat_name,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (cat_name,))
    
    # Insert default tags
    for tag_name in default_categories:
        cursor.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
    
    # Create default admin user
    cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@faculty.edu', admin_password, 'admin'))
    
    db.commit()
    db.close()

# Initialize database on startup
def create_tables():
    init_db()

with app.app_context():
    create_tables()

# Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'message': 'All fields are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400
        
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash) 
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        
        db.commit()
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'message': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            if not user['is_active']:
                return jsonify({'message': 'Account is deactivated'}), 403
            
            # Convert user ID to string for JWT subject
            user_id_str = str(user['id'])
            access_token = create_access_token(identity=user_id_str)
            
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at']
            }
            
            return jsonify({
                'access_token': access_token,
                'user': user_data
            })
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'message': 'Login failed'}), 500


# Recording Routes - Separate GET and POST

# GET all recordings
@app.route('/api/recordings', methods=['GET'])
def get_recordings():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build base query
        query = '''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
        '''
        params = []
        conditions = []
        
        # Add search condition
        if search:
            conditions.append('(r.title LIKE ? OR r.content LIKE ?)')
            params.extend([f'%{search}%', f'%{search}%'])
        
        # Add category filter
        if category:
            conditions.append('r.category_id = ?')
            params.append(category)
        
        # Add WHERE clause if conditions exist
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        # Add sorting
        valid_sort_fields = ['created_at', 'title', 'updated_at', 'views']
        if sort_by in valid_sort_fields:
            query += f' ORDER BY r.{sort_by}'
            if sort_order.lower() == 'desc':
                query += ' DESC'
            else:
                query += ' ASC'
        else:
            query += ' ORDER BY r.created_at DESC'
        
        # Get total count for pagination
        count_query = 'SELECT COUNT(*) as total FROM recordings r'
        if conditions:
            count_query += ' WHERE ' + ' AND '.join(conditions)
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Add pagination
        offset = (page - 1) * per_page
        query += f' LIMIT {per_page} OFFSET {offset}'
        
        cursor.execute(query, params)
        recordings = cursor.fetchall()
        
        # Get tags for each recording
        result_recordings = []
        for recording in recordings:
            cursor.execute('''
                SELECT t.id, t.name FROM tags t
                JOIN recording_tags rt ON t.id = rt.tag_id
                WHERE rt.recording_id = ?
            ''', (recording['id'],))
            tags = cursor.fetchall()
            
            result_recordings.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'video_path': recording['video_path'],
                'category': {
                    'id': recording['category_id'], 
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'author': {
                    'id': recording['author_id'], 
                    'username': recording['author_username']
                } if recording['author_id'] else None,
                'user_id': recording['author_id'],
                'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
                'created_at': recording['created_at'],
                'updated_at': recording['updated_at'],
                'views': recording['views']
            })
        
        return jsonify({
            'recordings': result_recordings,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        print(f"Get recordings error: {e}")
        return jsonify({'message': 'Failed to fetch recordings'}), 500

# POST create new recording
@app.route('/api/recordings/create', methods=["GET",'POST'])
@jwt_required()
def create_recording():
    print("breakpoint")
    try:
        current_user_id = get_jwt_identity()
        
        # Ensure current_user_id is a string for JWT
        if isinstance(current_user_id, (int, float)):
            current_user_id = str(current_user_id)
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Handle form data (multipart/form-data)
        title = request.form.get('title')
        content = request.form.get('content', '')
        category_id = request.form.get('category_id')
        tags_json = request.form.get('tags', '[]')
        
        if not title:
            return jsonify({'message': 'Title is required'}), 400
        
        # Parse tags
        try:
            tag_ids = json.loads(tags_json) if tags_json else []
        except json.JSONDecodeError:
            tag_ids = []
        
        # Handle file uploads
        image_path = None
        video_path = None
        
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(file_path)
                image_path = f"/uploads/{filename}"
        
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file and video_file.filename:
                filename = secure_filename(video_file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(file_path)
                video_path = f"/uploads/{filename}"
        
        # Insert recording - convert current_user_id back to int for database
        cursor.execute('''
            INSERT INTO recordings (title, content, category_id, author_id, image_path, video_path) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, category_id if category_id else None, int(current_user_id), image_path, video_path))
        
        recording_id = cursor.lastrowid
        
        # Add tags
        if tag_ids:
            for tag_data in tag_ids:
                if isinstance(tag_data, dict):
                    if tag_data.get('isNew'):
                        # Create new tag
                        cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag_data['name'],))
                        tag_id = cursor.lastrowid
                    else:
                        tag_id = tag_data['id']
                else:
                    tag_id = tag_data
                
                cursor.execute('''
                    INSERT OR IGNORE INTO recording_tags (recording_id, tag_id) 
                    VALUES (?, ?)
                ''', (recording_id, tag_id))
        
        db.commit()
        return jsonify({'message': 'Recording created successfully', 'id': recording_id}), 201
        
    except Exception as e:
        print(f"Create recording error: {e}")
        return jsonify({'message': 'Failed to create recording'}), 500


# GET single recording by ID
@app.route('/api/recordings/<int:recording_id>', methods=['GET'])
def get_recording(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get recording with related data
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
            WHERE r.id = ?
        ''', (recording_id,))
        
        recording = cursor.fetchone()
        
        if not recording:
            return jsonify({'message': 'Recording not found'}), 404
        
        # Get tags for this recording
        cursor.execute('''
            SELECT t.id, t.name FROM tags t
            JOIN recording_tags rt ON t.id = rt.tag_id
            WHERE rt.recording_id = ?
        ''', (recording_id,))
        tags = cursor.fetchall()
        
        # Increment view count
        cursor.execute('UPDATE recordings SET views = views + 1 WHERE id = ?', (recording_id,))
        db.commit()
        
        # Format response
        result = {
            'id': recording['id'],
            'title': recording['title'],
            'content': recording['content'],
            'image_path': recording['image_path'],
            'video_path': recording['video_path'],
            'category': {
                'id': recording['category_id'],
                'name': recording['category_name']
            } if recording['category_id'] else None,
            'user': {
                'id': recording['author_id'],
                'username': recording['author_username']
            } if recording['author_id'] else None,
            'user_id': recording['author_id'],
            'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
            'created_at': recording['created_at'],
            'updated_at': recording['updated_at'],
            'views': recording['views']
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get recording error: {e}")
        return jsonify({'message': 'Failed to fetch recording'}), 500

# PUT update recording
# Update all routes that use get_jwt_identity() to convert to int when needed
@app.route('/api/recordings/<int:recording_id>/update', methods=['PUT'])
@jwt_required()
def update_recording(recording_id):
    try:
        current_user_id = get_jwt_identity()
        # Convert to int for database operations
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Rest of the function remains the same...
        
    except Exception as e:
        print(f"Update recording error: {e}")
        return jsonify({'message': 'Failed to update recording'}), 500

@app.route('/api/recordings/<int:recording_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_recording(recording_id):
    try:
        current_user_id = get_jwt_identity()
        # Convert to int for database operations
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Rest of the function remains the same...
        
    except Exception as e:
        print(f"Delete recording error: {e}")
        return jsonify({'message': 'Failed to delete recording'}), 500

# GET latest recordings
@app.route('/api/recordings/latest', methods=['GET'])
def get_latest_recordings():
    try:
        db = get_db()
        cursor = db.cursor()
        
        limit = int(request.args.get('limit', 5))
        
        cursor.execute('''
            SELECT r.*, c.name as category_name, u.username as author_username
            FROM recordings r
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN users u ON r.author_id = u.id
            ORDER BY r.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        recordings = cursor.fetchall()
        
        result = []
        for recording in recordings:
            # Get tags for each recording
            cursor.execute('''
                SELECT t.id, t.name FROM tags t
                JOIN recording_tags rt ON t.id = rt.tag_id
                WHERE rt.recording_id = ?
            ''', (recording['id'],))
            tags = cursor.fetchall()
            
            result.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'video_path': recording['video_path'],
                'category': {
                    'id': recording['category_id'],
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'author': {
                    'id': recording['author_id'],
                    'username': recording['author_username']
                } if recording['author_id'] else None,
                'tags': [{'id': tag['id'], 'name': tag['name']} for tag in tags],
                'created_at': recording['created_at'],
                'views': recording['views']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get latest recordings error: {e}")
        return jsonify({'message': 'Failed to fetch latest recordings'}), 500

# GET related recordings
@app.route('/api/recordings/<int:recording_id>/related', methods=['GET'])
def get_related_recordings(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get current recording's category
        cursor.execute('SELECT category_id FROM recordings WHERE id = ?', (recording_id,))
        current_recording = cursor.fetchone()
        
        if not current_recording:
            return jsonify([])
        
        category_id = current_recording['category_id']
        limit = int(request.args.get('limit', 3))
        
        if category_id:
            # Get recordings from same category
            cursor.execute('''
                SELECT r.*, c.name as category_name, u.username as author_username
                FROM recordings r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN users u ON r.author_id = u.id
                WHERE r.category_id = ? AND r.id != ?
                ORDER BY r.created_at DESC
                LIMIT ?
            ''', (category_id, recording_id, limit))
        else:
            # Get latest recordings if no category
            cursor.execute('''
                SELECT r.*, c.name as category_name, u.username as author_username
                FROM recordings r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN users u ON r.author_id = u.id
                WHERE r.id != ?
                ORDER BY r.created_at DESC
                LIMIT ?
            ''', (recording_id, limit))
        
        recordings = cursor.fetchall()
        
        result = []
        for recording in recordings:
            result.append({
                'id': recording['id'],
                'title': recording['title'],
                'content': recording['content'],
                'image_path': recording['image_path'],
                'category': {
                    'id': recording['category_id'],
                    'name': recording['category_name']
                } if recording['category_id'] else None,
                'created_at': recording['created_at']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Get related recordings error: {e}")
        return jsonify([])

# Categories Routes
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY name')
        categories = [dict(row) for row in cursor.fetchall()]
        return jsonify(categories)
    except Exception as e:
        print(f"Get categories error: {e}")
        return jsonify({'message': 'Failed to fetch categories'}), 500

@app.route('/api/categories/create', methods=['POST'])
@jwt_required()
def create_category():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'message': 'Category name is required'}), 400
        
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        db.commit()
        
        return jsonify({'message': 'Category created successfully', 'id': cursor.lastrowid}), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Category already exists'}), 400
    except Exception as e:
        print(f"Create category error: {e}")
        return jsonify({'message': 'Failed to create category'}), 500

# Tags Routes
@app.route('/api/tags', methods=['GET'])
def get_tags():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tags ORDER BY name')
        tags = [dict(row) for row in cursor.fetchall()]
        return jsonify(tags)
    except Exception as e:
        print(f"Get tags error: {e}")
        return jsonify({'message': 'Failed to fetch tags'}), 500

@app.route('/api/tags/create', methods=['POST'])
@jwt_required()
def create_tag():
    try:
        current_user_id = get_jwt_identity()
        db = get_db()
        cursor = db.cursor()
        
        # Check user permissions
        cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
        user = cursor.fetchone()
        
        if not user or user['role'] not in ['admin', 'moderator']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'message': 'Tag name is required'}), 400
        
        cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
        db.commit()
        
        return jsonify({'message': 'Tag created successfully', 'id': cursor.lastrowid}), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Tag already exists'}), 400
    except Exception as e:
        print(f"Create tag error: {e}")
        return jsonify({'message': 'Failed to create tag'}), 500

# File serving route
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_file("../"+app.config['UPLOAD_FOLDER']+"/"+filename)

# Admin routes (keeping existing admin functionality)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND role IN ("admin", "moderator")', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['admin_user_id'] = user['id']
            session['admin_username'] = user['username']
            session['admin_role'] = user['role']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    cursor = db.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as total FROM users')
    total_users = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM recordings')
    total_recordings = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM users WHERE created_at >= date("now", "-30 days")')
    new_users_month = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM recordings WHERE created_at >= date("now", "-30 days")')
    new_recordings_month = cursor.fetchone()['total']
    
    stats = {
        'total_users': total_users,
        'total_recordings': total_recordings,
        'new_users_month': new_users_month,
        'new_recordings_month': new_recordings_month
    }
    
    # Get recent users
    cursor.execute('''
        SELECT * FROM users 
        ORDER BY created_at DESC 
        LIMIT 5
    ''')
    recent_users = cursor.fetchall()
    
    # Get recent recordings
    cursor.execute('''
        SELECT r.*, u.username as author
        FROM recordings r
        LEFT JOIN users u ON r.author_id = u.id
        ORDER BY r.created_at DESC 
        LIMIT 5
    ''')
    recent_recordings = cursor.fetchall()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_users=recent_users,
                         recent_recordings=recent_recordings)

@app.route('/admin/users')
@admin_required
def admin_users():
    db = get_db()
    cursor = db.cursor()
    
    # Get filters
    search = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Build query
    query = 'SELECT * FROM users'
    params = []
    conditions = []
    
    if search:
        conditions.append('(username LIKE ? OR email LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%'])
    
    if role_filter:
        conditions.append('role = ?')
        params.append(role_filter)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY created_at DESC'
    
    # Get total count
    count_query = 'SELECT COUNT(*) as total FROM users'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    # Add pagination
    offset = (page - 1) * per_page
    query += f' LIMIT {per_page} OFFSET {offset}'
    
    cursor.execute(query, params)
    users = cursor.fetchall()
    
    return render_template('admin/users.html', 
                         users=users, 
                         total=total,
                         search=search,
                         role_filter=role_filter,
                         page=page,
                         per_page=per_page,
                         total_pages=(total + per_page - 1) // per_page)

@app.route('/admin/recordings')
@admin_required
def admin_recordings():
    db = get_db()
    cursor = db.cursor()
    
    # Get filters
    search = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Build query
    query = '''
        SELECT r.*, c.name as category_name, u.username as author_username
        FROM recordings r
        LEFT JOIN categories c ON r.category_id = c.id
        LEFT JOIN users u ON r.author_id = u.id
    '''
    params = []
    conditions = []
    
    if search:
        conditions.append('(r.title LIKE ? OR r.content LIKE ?)')
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category_filter:
        conditions.append('r.category_id = ?')
        params.append(category_filter)
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY r.created_at DESC'
    
    # Get total count
    count_query = 'SELECT COUNT(*) as total FROM recordings r'
    if conditions:
        count_query += ' WHERE ' + ' AND '.join(conditions)
    
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    # Add pagination
    offset = (page - 1) * per_page
    query += f' LIMIT {per_page} OFFSET {offset}'
    
    cursor.execute(query, params)
    recordings = cursor.fetchall()
    
    # Get categories for filter
    cursor.execute('SELECT * FROM categories ORDER BY name')
    categories = cursor.fetchall()
    
    return render_template('admin/recordings.html', 
                         recordings=recordings, 
                         categories=categories,
                         total=total,
                         search=search,
                         category_filter=category_filter,
                         page=page,
                         per_page=per_page,
                         total_pages=(total + per_page - 1) // per_page)

@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    try:
        # Prevent admin from deactivating themselves
        if user_id == session.get('admin_user_id'):
            flash('You cannot deactivate your own account', 'error')
            return redirect(url_for('admin_users'))
        
        db = get_db()
        cursor = db.cursor()
        
        # Get current status
        cursor.execute('SELECT is_active FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            new_status = not user['is_active']
            cursor.execute('UPDATE users SET is_active = ? WHERE id = ?', (new_status, user_id))
            db.commit()
            
            status_text = 'activated' if new_status else 'deactivated'
            flash(f'User {status_text} successfully', 'success')
        else:
            flash('User not found', 'error')
            
    except Exception as e:
        print(f"Toggle user status error: {e}")
        flash('Failed to update user status', 'error')
    
    return redirect(url_for('admin_users'))
@app.route('/admin/recordings/<int:recording_id>/delete', methods=['POST'])
@admin_required
def admin_delete_recording(recording_id):
    db = get_db()
    cursor = db.cursor()
    
    # Get recording info
    cursor.execute('SELECT * FROM recordings WHERE id = ?', (recording_id,))
    recording = cursor.fetchone()
    
    if recording:
        # Delete associated files
        if recording['image_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                   recording['image_path'].replace('/uploads/', ''))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        if recording['video_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                   recording['video_path'].replace('/uploads/', ''))
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete recording
        cursor.execute('DELETE FROM recordings WHERE id = ?', (recording_id,))
        db.commit()
        
        flash('Recording deleted successfully!', 'success')
    else:
        flash('Recording not found!', 'error')
    
    return redirect(url_for('admin_recordings'))
@app.route('/admin/recordings/<int:recording_id>/details')
@admin_required
def get_recording_details(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT r.*, u.username as author, c.name as category
            FROM recordings r
            LEFT JOIN users u ON r.author_id = u.id
            LEFT JOIN categories c ON r.category_id = c.id
            WHERE r.id = ?
        ''', (recording_id,))
        
        recording = cursor.fetchone()
        
        if not recording:
            return jsonify({'success': False, 'message': 'Recording not found'}), 404
        
        return jsonify({
            'success': True,
            'recording': dict(recording)
        })
        
    except Exception as e:
        print(f"Get recording details error: {e}")
        return jsonify({'success': False, 'message': 'Failed to get recording details'}), 500

@app.route('/admin/recordings/<int:recording_id>/delete', methods=['POST'])
@admin_required
def delete_recording_admin(recording_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Get recording info for file cleanup
        cursor.execute('SELECT image_path, video_path FROM recordings WHERE id = ?', (recording_id,))
        recording = cursor.fetchone()
        
        if recording:
            # Delete associated files
            if recording['image_path']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['image_path']))
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            if recording['video_path']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(recording['video_path']))
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            # Delete recording tags
            cursor.execute('DELETE FROM recording_tags WHERE recording_id = ?', (recording_id,))
            
            # Delete recording
            cursor.execute('DELETE FROM recordings WHERE id = ?', (recording_id,))
            
            db.commit()
            flash('Recording deleted successfully', 'success')
        else:
            flash('Recording not found', 'error')
            
    except Exception as e:
        print(f"Delete recording error: {e}")
        flash('Failed to delete recording', 'error')
    
    return redirect(url_for('admin_recordings'))



# Error handlers
# Add these error handlers to your Flask app

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



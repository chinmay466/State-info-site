from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create states table
    c.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            capital TEXT,
            population INTEGER,
            area REAL,
            language TEXT,
            region TEXT,
            about TEXT
        )
    ''')

    # Insert default user if not exists
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'password123'))

    # Insert 28 Indian states if table empty
    c.execute('SELECT COUNT(*) FROM states')
    if c.fetchone()[0] == 0:
        states = [
            ('Andhra Pradesh', 'Amaravati', 49577103, 162968, 'Telugu', 'South', 'Andhra Pradesh is known for its rich culture and history.'),
            ('Arunachal Pradesh', 'Itanagar', 1383727, 83743, 'English', 'North-East', 'Arunachal Pradesh is famous for its biodiversity.'),
            ('Assam', 'Dispur', 31205576, 78438, 'Assamese', 'North-East', 'Assam is famous for tea and wildlife.'),
            ('Bihar', 'Patna', 104099452, 94163, 'Hindi', 'East', 'Bihar is known for historical sites and education centers.'),
            ('Chhattisgarh', 'Naya Raipur', 25545198, 135191, 'Hindi', 'Central', 'Chhattisgarh is rich in mineral resources.'),
            ('Goa', 'Panaji', 1458545, 3702, 'Konkani', 'West', 'Goa is famous for beaches and tourism.'),
            ('Gujarat', 'Gandhinagar', 60439692, 196024, 'Gujarati', 'West', 'Gujarat is known for its industry and heritage.'),
            ('Haryana', 'Chandigarh', 25351462, 44212, 'Hindi', 'North', 'Haryana is an agricultural hub.'),
            ('Himachal Pradesh', 'Shimla', 6864602, 55673, 'Hindi', 'North', 'Known for scenic beauty and tourism.'),
            ('Jharkhand', 'Ranchi', 32966238, 79714, 'Hindi', 'East', 'Jharkhand is rich in minerals.'),
            ('Karnataka', 'Bengaluru', 61095297, 191791, 'Kannada', 'South', 'Karnataka is the IT hub of India.'),
            ('Kerala', 'Thiruvananthapuram', 33406061, 38852, 'Malayalam', 'South', 'Kerala is famous for backwaters and tourism.'),
            ('Madhya Pradesh', 'Bhopal', 72626809, 308350, 'Hindi', 'Central', 'Known as the heart of India.'),
            ('Maharashtra', 'Mumbai', 112374333, 307713, 'Marathi', 'West', 'Maharashtra is home to Bollywood.'),
            ('Manipur', 'Imphal', 2855794, 22327, 'Manipuri', 'North-East', 'Known for its rich culture and dance.'),
            ('Meghalaya', 'Shillong', 2966889, 22429, 'English', 'North-East', 'Known as the abode of clouds.'),
            ('Mizoram', 'Aizawl', 1097206, 21081, 'Mizo', 'North-East', 'Known for scenic landscapes.'),
            ('Nagaland', 'Kohima', 1978502, 16579, 'English', 'North-East', 'Known for diverse tribes.'),
            ('Odisha', 'Bhubaneswar', 41974218, 155707, 'Odia', 'East', 'Known for temples and culture.'),
            ('Punjab', 'Chandigarh', 27743338, 50362, 'Punjabi', 'North', 'Known for agriculture and Sikh heritage.'),
            ('Rajasthan', 'Jaipur', 68548437, 342239, 'Hindi', 'West', 'Known for forts and desert.'),
            ('Sikkim', 'Gangtok', 610577, 7096, 'English', 'North-East', 'Known for mountains and biodiversity.'),
            ('Tamil Nadu', 'Chennai', 72147030, 130058, 'Tamil', 'South', 'Known for temples and culture.'),
            ('Telangana', 'Hyderabad', 35003674, 112077, 'Telugu', 'South', 'Known for IT and heritage.'),
            ('Tripura', 'Agartala', 3673917, 10491, 'Bengali', 'North-East', 'Known for palaces and culture.'),
            ('Uttar Pradesh', 'Lucknow', 199812341, 243286, 'Hindi', 'North', 'Most populous state in India.'),
            ('Uttarakhand', 'Dehradun', 10086292, 53483, 'Hindi', 'North', 'Known for Himalayan mountains.'),
            ('West Bengal', 'Kolkata', 91276115, 88752, 'Bengali', 'East', 'Known for culture and literature.')
        ]
        c.executemany('''
            INSERT INTO states (name, capital, population, area, language, region, about)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', states)

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    conn = get_db_connection()
    states = conn.execute('SELECT * FROM states').fetchall()
    conn.close()
    return render_template('home.html', states=states)

@app.route('/state/<int:state_id>')
@login_required
def state_detail(state_id):
    conn = get_db_connection()
    state = conn.execute('SELECT * FROM states WHERE id = ?', (state_id,)).fetchone()
    conn.close()
    if state is None:
        return "State not found", 404
    return render_template('state_detail.html', state=state)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)

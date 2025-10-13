from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Dummy user data
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "student1": {"password": "stud123", "role": "student"},
    "student2": {"password": "stud456", "role": "student"}
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]['password'] == password:
        session['user'] = username
        role = users[username]['role']
        
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    else:
        flash("Invalid username or password!", "danger")
        return redirect(url_for('home'))

@app.route('/admin')
def admindashboard():
    if 'user' in session and users[session['user']]['role'] == 'admin':
        return render_template('admin dashboard.html', user=session['user'])
    return redirect(url_for('home'))

@app.route('/student')
def studentdashboard():
    if 'user' in session and users[session['user']]['role'] == 'student':
        return render_template('student dashboard.html', user=session['user'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    flash("Thank you for visiting!", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

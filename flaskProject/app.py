from flask import Flask, render_template, request, session
import paramiko
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=2)  # Set session timeout to 2 minutes

# Store configurations and command history in-memory
configurations = [
    {"host": "example1.com", "username": "user1", "password": "pass1"},
    {"host": "example2.com", "username": "user2", "password": "pass2"},
]
command_history = []

@app.route('/')
def index():
    return render_template('index.html', configurations=configurations, command_history=command_history)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    host = request.form.get('host')
    username = request.form.get('username')
    password = request.form.get('password')
    command = request.form.get('command')

    # Set up SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if 'logged_in' not in session or not session['logged_in']:
        # Connect to the remote host only if not already logged in
        ssh.connect(host, username=username, password=password)
        session['logged_in'] = True
        session['login_time'] = datetime.now()

    # Execute the command
    stdin, stdout, stderr = ssh.exec_command(command)

    # Get the command output
    output = stdout.read().decode('utf-8')

    # Add the executed command to the command history
    command_history.append(command)

    # Close the SSH connection
    ssh.close()

    session['previous_command'] = command  # Save the command in the session

    return render_template('index.html', output=output, configurations=configurations, command_history=command_history)

if __name__ == '__main__':
    app.run(debug=True)

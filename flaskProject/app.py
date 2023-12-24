from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

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

    # Add the new configuration to the list
    configurations.append({"host": host, "username": username, "password": password})

    # Set up SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote host
    ssh.connect(host, username=username, password=password)

    # Execute the command
    stdin, stdout, stderr = ssh.exec_command(command)

    # Get the command output
    output = stdout.read().decode('utf-8')

    # Add the executed command to the command history
    command_history.append(command)

    # Close the SSH connection
    ssh.close()

    return render_template('index.html', output=output, configurations=configurations, command_history=command_history)

if __name__ == '__main__':
    app.run(debug=True)

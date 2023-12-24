from flask import Flask, render_template, request, redirect, url_for
import paramiko

app = Flask(__name__)

# Store configurations and command history in-memory
configurations = [
    {"host": "example1.com", "username": "user1", "password": "pass1"},
    {"host": "example2.com", "username": "user2", "password": "pass2"},
]
command_history = []

# ... (previous imports and configurations) ...

@app.route('/')
def index():
    return render_template('index.html', configurations=configurations, command_history=command_history)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    # ... (previous code) ...

    selected_command = request.form.get('previous_command')
    if selected_command:
        # If a previous command is selected, set it as the current command
        command = selected_command

    # ... (rest of the code) ...

    return render_template('index.html', output=output, configurations=configurations, command_history=command_history)

# ... (rest of the code) ...

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data storage in memory
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@gmail.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@gmail.com'}
    
]

# File to store data
data_file = 'users.txt'

# Helper function to write data to file
def write_to_file(data):
    with open(data_file, 'w') as f:
        for user in data:
            f.write(f"{user['id']},{user['name']},{user['email']}\n")

# Helper function to read data from file
def read_from_file():
    try:
        with open(data_file, 'r') as f:
            lines = f.readlines()
            users = []
            for line in lines:
                parts = line.strip().split(',')
                users.append({'id': int(parts[0]), 'name': parts[1], 'email': parts[2]})
            return users
    except FileNotFoundError:
        return []

# Home route


@app.route('/')
def index():
    return "Welcome to the User API!"

# get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = read_from_file()
    return jsonify(users)


# create a new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        'id': request.json['id'],
        'name': request.json['name'],
        'email': request.json['email']
    }
    users.append(new_user)
    write_to_file(users)
    return jsonify(new_user)

# get user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    users = read_from_file()
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})


# Delete user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = read_from_file()
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        users = [user for user in users if user['id'] != user_id]
        write_to_file(users)
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'message': 'User not found'})
    
@app.route('/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    users = read_from_file()
    user = next((user for users in user if user['id'] == user_id),None)
    if user:
        user['name'] = request.json.get('name', user['name'])
        user['email'] = request.json.get('email', user['email'])
        write_to_file(users)
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})
    

if __name__ == '__main__':
    app.run(debug=True)

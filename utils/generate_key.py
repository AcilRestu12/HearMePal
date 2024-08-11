import secrets

def generate_secret_key():
    # Generate a secret key
    secret_key = secrets.token_hex(16)  # 16 bytes key, can be adjusted as needed
    return secret_key

def update_env_file(secret_key):
    env_file = '.env'
    lines = []
    key_found = False

    # Read existing lines from the file
    try:
        with open(env_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        # If file does not exist, create a new one
        lines = []

    # Update or add the SECRET_KEY variable
    with open(env_file, 'w') as file:
        for line in lines:
            if line.startswith('SECRET_KEY='):
                file.write(f'SECRET_KEY={secret_key}\n')
                key_found = True
            else:
                file.write(line)
        
        if not key_found:
            file.write(f'SECRET_KEY={secret_key}\n')

if __name__ == '__main__':
    secret_key = generate_secret_key()
    update_env_file(secret_key)
    print(f'Secret key generated and updated in .env: {secret_key}')

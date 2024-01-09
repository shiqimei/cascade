import base64

def main():
    # Define the path to the .env file and the output yaml file.
    project = 'cascade-chat'
    env_file_path = './.env'
    output_yaml_path = './deployment-secret.yaml'

    # Read the .env file and extract the environment variables
    env_vars = {}
    with open(env_file_path, 'r') as file:
        for line in file:
            # Skip lines that are comments or empty
            if line.startswith('#') or not line.strip():
                continue
            # Extract the key-value pairs
            key, value = line.strip().split('=', 1)
            env_vars[key] = value

    # Convert the environment variables to base64 encoded strings
    for key in env_vars:
        value = env_vars[key].encode('utf-8')
        env_vars[key] = base64.b64encode(value).decode('utf-8')

    # Write the environment variables to the yaml file
    with open(output_yaml_path, 'w') as file:
        file.write('apiVersion: v1\n')
        file.write('kind: Secret\n')
        file.write('metadata:\n')
        file.write('  name: deployment-secret\n')
        file.write(f'  namespace: { project }\n')
        file.write('type: Opaque\n')
        file.write('data:\n')
        for key, value in env_vars.items():
            file.write(f'  {key}: {value}\n')

    print(f'Secrets written to {output_yaml_path}')

if __name__ == '__main__':
    main()
import sys

def set_env(mode):
    if mode not in ['dev', 'prod']:
        print("Invalid mode. Please use either dev or prod")
        sys.exit(1)

    # Open the .env file and read the contents
    with open('.env', 'r') as file:
        lines = file.readlines()

    # Find the line that starts with MODE=
    for i, line in enumerate(lines):
        if line.startswith('ENV='):
            lines[i] = f'ENV={mode}\n'
            break

    # Write the new contents to the .env file
    with open('.env', 'w') as file:
        file.writelines(lines)
        

    print(f"Mode set to {mode}.")

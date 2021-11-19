import os
def parse_folder_to_script():
    script = ''
    server_directory = os.path.dirname(os.getcwd()) + '/server'
    for filename in os.listdir(server_directory):
        with open(server_directory + "/" + filename) as file:
            script += "sudo touch %s\n" %filename
            script += "cat <<EOT >> " + filename + "\n" + file.read() + "EOT\n"
    print(script)

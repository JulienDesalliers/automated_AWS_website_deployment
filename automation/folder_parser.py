import os

#petite fonction qui permet de parser les files du serveur pour les cat dans l'instance EC2 par l'argument user_data
#idealement ca devrait etre fait par SCP :)

def parse_folder_to_script():
    script = ''
    server_directory = os.path.dirname(os.getcwd()) + '/server'
    for filename in os.listdir(server_directory):
        with open(server_directory + "/" + filename) as file:
            script += "sudo touch %s\n" %filename
            script += "cat <<EOT >> " + filename + "\n" + file.read() + "EOT\n"
    return script

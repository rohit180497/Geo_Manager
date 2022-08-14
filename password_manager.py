import os
import sys

import logging
from cryptography import fernet
from cryptography.fernet import Fernet
import keyring


class PasswordVault:

    def __init__(self) -> None:
        """
        Password vault helps to manage your password requirements in a secured encrypted manner

        """

        self.key_path = os.path.join(os.path.expanduser('~'), 'secret.key')

    def set_password(self, service, user, password) -> bool:
        '''
        Encrypts the password and stores in the operating systems credential vault    

        parameters  
        --------------
       service: str, service name by which you want to refer your credential
       user: str, username/login id for which you want to store the password
       password: str, password in plain text that is to be encrypted and stored in os credential vault

       returns
       ---------------
       bool: if the password is stored successfully or not
        '''
        is_success = False

        try:
            # generating the key if not found in provided key_path
            key = None

            if not os.path.exists(self.key_path):
                key = Fernet.generate_key()
                with open(self.key_path, 'wb') as file:
                    file.write(key)
            else:
                with open(self.key_path, 'r') as file:
                    file = file.read()

            # encryption level 1
            fernet = Fernet(key)
            encoded_password = fernet.encrypt(password.encode())

            # storing the encrypted key in OS password valult
            keyring.set_password(service, user, encoded_password)

            is_success = True
        except Exception as e:
            logging.error('Error storing the password: {}'.format(e))

        return is_success

    def get_password(self, service, user) -> str:
        '''
        retrieves the password from the os password vault and provides the usable vesion of password

        Parameters
        --------------
        service: str, service name for which you want to retreive your credential
        user: str, username/login id for which you want to fetch the password

        returns
        --------------
        password: str, decrypted password to be used by your service

        '''

        password = None

        try:
            # reading the user define key
            key = None
            with open(self.key_path, 'r') as file:
                key = file.read()
            fernet = Fernet(key)

            # retrieving the password from os password vault
            encrypted_password = eval(keyring.get_password(service, user))

            # decrypt the password
            password = fernet.decrypt(encrypted_password).decode()

        except Exception as e:
            logging.error('Error retrieving password: {}'.format(e))

        return password

    if __name__ == '__main__':
        args = sys.argv
        arglen = len(args)

        if arglen != 4:
            print('Error: Please provide service, username and password on prompt!')
        else:
            vault = PasswordVault()
            print('Your password is set in OS credential vault' if vault.set_password(args[1], args[2], args[3] else 'there was an error setting your password'))

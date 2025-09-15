
import os

from subprocess import Popen, PIPE


class GpgUtils:

    def __init__(self):
        
        self.gpg_cmd = "gpg2"
        self.gpg_extra_args = [
            "--quiet", "--yes", "--compress-algo=none", "--no-encrypt-to"
        ]


    def encrypt_to_file(self, encrypted_out_file_path, cleartext, gpg_id):

        cmd = [
            self.gpg_cmd,
            "-r", gpg_id,
            "-o", encrypted_out_file_path
        ]
        cmd.append("--encrypt")
        #cmd.extend(self.gpg_extra_args)

        os.makedirs(
            os.path.dirname(encrypted_out_file_path),
            0o700, exist_ok=True
        )
        p = Popen(cmd, stdin=PIPE)
        p.communicate(input=cleartext.encode())
        os.chmod(encrypted_out_file_path, 0o600)


    def decrypt_file(self, encrypted_file_path, gpg_id):

        cmd = [
            self.gpg_cmd, "--batch",
            "-r", gpg_id,
            "-d", encrypted_file_path
        ]
        #cmd.extend(self.gpg_extra_args)
        # env = {
        #     'GPG_TTY': os.ttyname(sys.stdout.fileno())
        # }
        decrypted = Popen(cmd, stdout=PIPE).communicate()[0]

        return decrypted.decode()

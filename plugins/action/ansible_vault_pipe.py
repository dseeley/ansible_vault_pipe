# Copyright 2022 Dougal Seeley <github@dougalseeley.com>
# BSD 3-Clause License

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible_collections.dseeley.ansible_vault_pipe.plugins.module_utils.vault_utils import vault_encrypt, vault_decrypt
from ansible.utils.display import Display

display = Display()

#################################
# An action plugin to perform vault encrypt/decrypt operations inside a playbook.  Can use either user-provided id/pass, or will otherwise try to use already-loaded vault secrets.
# parameters:
#   action: [encrypt|decrypt]
#   vaultid: The vault-id if this is (or will be) associated with one. (optional)
#   vaultpass: The vault password (the current password for action: decrypt, the desired for action: encrypt).  If this is not provided, will attempt to use the already-loaded secrets (command-line or vault script).
#   vaulttext: (decrypt-only) - the vault text to be decrypted
#   plaintext: (encrypt-only) - the plain text to be encrypted
#   multiline_out: (encrypt-only) - whether to break the encrypted ciphertext into 80-character lines (as ansible-vault encrypt does).  Default: false
#################################
#
# - name: Encrypt using user-provided vaultid and vaultpass
#   dseeley.ansible_vault_pipe.ansible_vault_pipe:
#     action: encrypt
#     vaultid: sandbox
#     vaultpass: asdf
#     plaintext: "sometext"
#   register: r__ansible_vault_encrypt
# - debug: msg={{r__ansible_vault_encrypt}}
#
# - name: Decrypt using user-provided vaultid and vaultpass
#   dseeley.ansible_vault_pipe.ansible_vault_pipe:
#     action: decrypt
#     vaultid: sandbox
#     vaultpass: asdf
#     vaulttext: "$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165"
#   register: r__ansible_vault_decrypt
# - debug: msg={{r__ansible_vault_decrypt}}
#
# - name: Encrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
#   dseeley.ansible_vault_pipe.ansible_vault_pipe:
#     action: encrypt
#     multiline_out: true
#     plaintext: "sometext"
#   register: r__ansible_vault_encrypt
# - debug: msg={{r__ansible_vault_encrypt}}
#
# - name: Decrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
#   dseeley.ansible_vault_pipe.ansible_vault_pipe:
#     action: decrypt
#     vaulttext: "$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165"
#   register: r__ansible_vault_decrypt
# - debug: msg={{r__ansible_vault_decrypt}}
#################################

class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp is deprecated

        args = self._task.args
        vaultpass = args.get("vaultpass")
        vaultid = args.get("vaultid")

        display.deprecated(f"dseeley.ansible_vault_pipe.ansible_vault_pipe with 'action: {args["action"]}' is deprecated in favour of dseeley.ansible_vault_pipe.{args["action"]}")

        if args["action"] == "encrypt":
            if "plaintext" not in args:
                return {"failed": True, "msg": "'plaintext' is required for encrypt."}

            enc = vault_encrypt(
                plaintext=args["plaintext"],
                vaultpass=vaultpass,
                vaultid=vaultid,
                multiline_out=args.get("multiline_out", False),
                loader=self._loader if not vaultpass else None,
            )
            result.update(enc)
        else:
            if "vaulttext" not in args:
                return {"failed": True, "msg": "'vaulttext' is required for decrypt."}

            dec = vault_decrypt(
                vaulttext=args["vaulttext"],
                vaultpass=vaultpass,
                vaultid=vaultid,
                loader=self._loader if not vaultpass else None,
            )
            result.update(dec)

        result['failed'] = False
        return result
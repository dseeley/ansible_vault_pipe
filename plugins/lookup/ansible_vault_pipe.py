# # Copyright 2026 Dougal Seeley <github@dougalseeley.com>
# # BSD 3-Clause License
#
# from __future__ import absolute_import, division, print_function
#
# __metaclass__ = type
#
# from ansible.errors import AnsibleError
# from ansible.plugins.lookup import LookupBase
# from ansible_collections.dseeley.ansible_vault_pipe.plugins.module_utils.vault_utils import vault_encrypt, vault_decrypt
# from ansible.utils.display import Display
#
# display = Display()
#
# #################################
# # A lookup plugin to perform vault encrypt/decrypt operations inside a playbook.  Can use either user-provided id/pass, or will otherwise try to use already-loaded vault secrets.
# # parameters:
# #   action: [encrypt|decrypt]
# #   vaultid: The vault-id if this is (or will be) associated with one. (optional)
# #   vaultpass: The vault password (the current password for action: decrypt, the desired for action: encrypt).  If this is not provided, will attempt to use the already-loaded secrets (command-line or vault script).
# #   vaulttext: (decrypt-only) - the vault text to be decrypted
# #   plaintext: (encrypt-only) - the plain text to be encrypted
# #   multiline_out: (encrypt-only) - whether to break the encrypted ciphertext into 80-character lines (as ansible-vault encrypt does).  Default: false
# #################################
# #
# # - name: dseeley.ansible_vault_pipe.ansible_vault_pipe | Encrypt using user-provided vaultid and vaultpass
# #   debug:
# #     msg: "{{ lookup('dseeley.ansible_vault_pipe.ansible_vault_pipe', 'sometext', action='encrypt', vaultid='sandbox', vaultpass='asdf') }}"
# #
# # - name: dseeley.ansible_vault_pipe.ansible_vault_pipe | Decrypt using user-provided vaultid and vaultpass
# #   debug:
# #     msg: "{{ lookup('dseeley.ansible_vault_pipe.ansible_vault_pipe', '$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165', action='decrypt', vaultid='sandbox', vaultpass='asdf') }}"
# #
# # - name: dseeley.ansible_vault_pipe.ansible_vault_pipe | Encrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
# #   debug:
# #     msg: "{{ lookup('dseeley.ansible_vault_pipe.ansible_vault_pipe', 'sometext', action='encrypt', multiline_out=true) }}"
# #
# # - name: dseeley.ansible_vault_pipe.ansible_vault_pipe | Decrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
# #   debug:
# #     msg: "{{ lookup('dseeley.ansible_vault_pipe.ansible_vault_pipe', '$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165, action='decrypt'') }}"
# #
# #################################
#
# class LookupModule(LookupBase):
#
#     def __init__(self, loader=None, templar=None, **kwargs):
#         super(LookupModule, self).__init__(loader=loader, templar=templar, **kwargs)
#         self._loader = loader
#
#     def run(self, terms, variables=None, **kwargs):
#
#         result = {}
#
#         # We expect only ONE term — the string to encrypt/decrypt (could extend to multiple terms later if needed)
#         if len(terms) != 1:
#             raise AnsibleError("ansible_vault_pipe lookup expects exactly one input value (the string to encrypt/decrypt)")
#
#         input_value = terms[0]
#
#         action = kwargs.get('action')
#         vaultpass = kwargs.get('vaultpass')
#         vaultid = kwargs.get('vaultid')
#
#         display.deprecated(f"dseeley.ansible_vault_pipe.ansible_vault_pipe with 'action: {action}' is deprecated in favour of dseeley.ansible_vault_pipe.{action}")
#
#         if action not in ('encrypt', 'decrypt'):
#             raise AnsibleError("action must be 'encrypt' or 'decrypt'")
#
#         # Use the captured loader only if no explicit password is provided
#         loader_to_use = self._loader if vaultpass is None else None
#
#         try:
#             if action == 'encrypt':
#                 result = vault_encrypt(
#                     plaintext=input_value,
#                     vaultpass=vaultpass,
#                     vaultid=vaultid,
#                     multiline_out=kwargs.get('multiline') or False,
#                     loader=loader_to_use,
#                 )
#                 return [result]
#
#             else:  # decrypt
#                 result = vault_decrypt(
#                     vaulttext=input_value,
#                     vaultpass=vaultpass,
#                     vaultid=vaultid,
#                     loader=loader_to_use,
#                 )
#                 return [result]
#
#         except Exception as e:
#             raise AnsibleError(f"ansible_vault_pipe lookup failed: {str(e)}") from e

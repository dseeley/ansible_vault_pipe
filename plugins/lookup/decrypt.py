# Copyright 2026 Dougal Seeley <github@dougalseeley.com>
# BSD 3-Clause License

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
name: decrypt
author: Dougal Seeley (@dseeley)
short_description: Decrypt an Ansible Vault-encrypted string.
version_added: "1.0.0"
description:
  - Decrypts a vault-encrypted string and returns the plaintext value.
  - Accepts an optional vault password and vault ID, or falls back to the configured loader.
options:
  _terms:
    description:
      - The vault-encrypted string to decrypt.
    required: true
    type: str
  vaultpass:
    description:
      - The vault password to use for decryption.
      - If omitted, the password is sourced from the configured loader (e.g. vault password file).
    required: false
    type: str
  vaultid:
    description:
      - An optional vault ID label associated with the encrypted value.
    required: false
    type: str
notes:
  - Exactly one term (vault-encrypted string) must be provided.
  - Part of the C(dseeley.ansible_vault_pipe) collection.
seealso:
  - plugin: dseeley.ansible_vault_pipe.encrypt
    plugin_type: lookup
    description: The corresponding lookup plugin for encrypting plaintext strings.
extends_documentation_fragment: []
"""

EXAMPLES = r"""
- name: Decrypt a vault-encrypted string using the default vault password
  ansible.builtin.debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.decrypt', encrypted_value) }}"

- name: Decrypt a vault-encrypted string using the default vault password
  debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.decrypt', '$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165') }}"

- name: Decrypt with an explicit vault password and vault ID
  ansible.builtin.debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.decrypt', encrypted_value, vaultpass='s3cr3t', vaultid='prod') }}"
"""

RETURN = r"""
_raw:
  description:
    - A list containing the single decrypted plaintext string.
  type: list
  elements: str
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible_collections.dseeley.ansible_vault_pipe.plugins.module_utils.vault_utils import vault_encrypt, vault_decrypt


class LookupModule(LookupBase):

    def __init__(self, loader=None, templar=None, **kwargs):
        super(LookupModule, self).__init__(loader=loader, templar=templar, **kwargs)
        self._loader = loader

    def run(self, terms, variables=None, **kwargs):
        # We expect only ONE term — the string to encrypt/decrypt (could extend to multiple terms later if needed)
        if len(terms) != 1:
            raise AnsibleError("ansible_vault_pipe lookup expects exactly one input value (the string to encrypt/decrypt)")

        result = vault_decrypt(
            vaulttext=terms[0],
            vaultpass=kwargs.get('vaultpass'),
            vaultid=kwargs.get('vaultid'),
            loader=self._loader if kwargs.get('vaultpass') is None else None
        )
        return [result]

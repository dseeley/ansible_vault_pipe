# Copyright 2026 Dougal Seeley <github@dougalseeley.com>
# BSD 3-Clause License

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
name: encrypt
author: Dougal Seeley (@dseeley)
short_description: Encrypt a string using Ansible Vault.
version_added: "1.0.0"
description:
  - Encrypts a plaintext string using Ansible Vault and returns the resulting vault-encrypted string.
  - Supports optional vault ID labelling and multiline output formatting.
options:
  _terms:
    description:
      - The plaintext string to encrypt.
    required: true
    type: str
  vaultpass:
    description:
      - The vault password to use for encryption.
      - If omitted, the password is sourced from the configured loader (e.g. vault password file).
    required: false
    type: str
  vaultid:
    description:
      - An optional vault ID label to associate with the encrypted value.
    required: false
    type: str
  multiline_out:
    description:
      - If C(true), formats the encrypted output across multiple lines.
      - Defaults to C(false).
    required: false
    type: bool
    default: false
notes:
  - Exactly one term (plaintext string) must be provided.
  - Part of the C(dseeley.ansible_vault_pipe) collection.
seealso:
  - plugin: dseeley.ansible_vault_pipe.decrypt
    plugin_type: lookup
    description: The corresponding lookup plugin for decrypting vault-encrypted strings.
extends_documentation_fragment: []
"""

EXAMPLES = r"""
- name: Encrypt a secret using the default vault password
  ansible.builtin.debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.encrypt', 'my_secret_value') }}"

- name: Encrypt with an explicit vault password and vault ID
  ansible.builtin.debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.encrypt', 'my_secret_value', vaultpass='s3cr3t', vaultid='prod') }}"

- name: Encrypt with multiline output
  ansible.builtin.debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.encrypt', 'my_secret_value', multiline_out=true) }}"
"""

RETURN = r"""
_raw:
  description:
    - A list containing the single vault-encrypted string.
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

        result = vault_encrypt(
            plaintext=terms[0],
            vaultpass=kwargs.get('vaultpass'),
            vaultid=kwargs.get('vaultid'),
            multiline_out=kwargs.get('multiline_out') or False,
            loader=self._loader if kwargs.get('vaultpass') is None else None
        )
        return [result]

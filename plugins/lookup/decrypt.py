# Copyright 2026 Dougal Seeley <github@dougalseeley.com>
# BSD 3-Clause License

from __future__ import absolute_import, division, print_function

__metaclass__ = type

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

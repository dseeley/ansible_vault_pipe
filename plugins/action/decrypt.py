# Copyright 2026 Dougal Seeley <github@dougalseeley.com>
# BSD 3-Clause License

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible_collections.dseeley.ansible_vault_pipe.plugins.module_utils.vault_utils import vault_encrypt, vault_decrypt

class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        del tmp  # tmp is deprecated

        args = self._task.args
        vaultpass = args.get("vaultpass")

        if "vaulttext" not in args:
            return {"failed": True, "msg": "'vaulttext' is required for decrypt."}

        dec = vault_decrypt(
            vaulttext=args["vaulttext"],
            vaultpass=vaultpass,
            vaultid=args.get("vaultid"),
            loader=self._loader if not vaultpass else None,
        )

        return dec | {"failed": False}

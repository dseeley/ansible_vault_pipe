# Copyright 2026 Dougal Seeley <github@dougalseeley.com>
# BSD 3-Clause License

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible import constants as C
from ansible.parsing.vault import VaultLib, VaultSecret, parse_vaulttext_envelope
from ansible.utils.display import Display

display = Display()


def build_vault_lib(vaultpass=None, vaultid=None, loader=None):
    """Build a VaultLib from explicit credentials or fall back to the loader's vault."""
    if vaultpass is not None:
        oVaultSecret = VaultSecret(vaultpass.encode('utf-8'))
        if vaultid:
            return VaultLib([(vaultid, oVaultSecret)])
        else:
            display.v(u'No vault-id supplied, using default identity.')
            return VaultLib([(C.DEFAULT_VAULT_IDENTITY, oVaultSecret)])
    elif loader is not None:
        display.v(u'No vault-id or vault-pass supplied, using playbook-sourced variables.')
        if len(loader._vault.secrets) == 0:
            display.warning("No Vault secrets loaded by config and none supplied to plugin.  Vault operations are not possible.")
        return loader._vault
    else:
        raise ValueError("Either 'vaultpass' or 'loader' must be provided.")


def vault_encrypt(plaintext, vaultpass=None, vaultid=None, multiline_out=False, loader=None):
    """Encrypt plaintext and return a dict with vaulttext and plaintext."""
    oVaultLib = build_vault_lib(vaultpass=vaultpass, vaultid=vaultid, loader=loader)

    b_vaulttext = oVaultLib.encrypt(plaintext)
    b_ciphertext, b_version, cipher_name, vault_id_out = parse_vaulttext_envelope(b_vaulttext)

    vaulttext_header = b_vaulttext.decode('utf-8').split('\n', 1)[0]
    ciphertext = b_ciphertext.decode('utf-8')

    if multiline_out:
        multiline_length = 80
        ciphertext = '\n'.join(
            [ciphertext[i:i + multiline_length] for i in range(0, len(ciphertext), multiline_length)]
        )

    return {
        'vaulttext': vaulttext_header + "\n" + ciphertext,
        # 'plaintext': plaintext,
    }


def vault_decrypt(vaulttext, vaultpass=None, vaultid=None, loader=None):
    """Decrypt vaulttext and return a dict with vaulttext and plaintext."""
    oVaultLib = build_vault_lib(vaultpass=vaultpass, vaultid=vaultid, loader=loader)

    plaintext = oVaultLib.decrypt(vaulttext)
    return {
        # 'vaulttext': vaulttext,
        'plaintext': plaintext,
    }

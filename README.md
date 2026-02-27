# Ansible Collection - dseeley.ansible_vault_pipe

An Ansible collection providing both an **action plugin** and an **action plugin** to perform vault encrypt/decrypt operations inside a playbook. Can use either user-provided id/pass, or can use already-loaded vault secrets.

## Installation

```bash
ansible-galaxy collection install dseeley.ansible_vault_pipe
```

## Plugins

### Parameters
Parameters can be passed to both the action plugin and the lookup plugin,

| Parameter       | Required | Description                                                                                                                                     |
|-----------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `vaultid`       | No       | The vault-id if this is (or will be) associated with one.                                                                                       |
| `vaultpass`     | No       | The vault password. If not provided, will attempt to use already-loaded secrets (command-line, ansible.cfg, vault script).                      |
| `plaintext`     | Encrypt  | The plain text to be encrypted.                                                                                                                 |
| `vaulttext`     | Decrypt  | The vault text to be decrypted.                                                                                                                 |
| `multiline_out` | No       | (encrypt-only) Whether to break the encrypted ciphertext into 80-character lines (as `ansible-vault encrypt` does). Default: `false`.           |


### Action Plugin

Use as a task to encrypt or decrypt vault data, with the result available via `register`.

#### Examples
```yaml
- name: ansible_vault_pipe.encrypt | Encrypt using user-provided vaultid and vaultpass
  dseeley.ansible_vault_pipe.encrypt:
    vaultid: sandbox
    vaultpass: asdf
    plaintext: "sometext"
  register: r__ansible_vault_encrypt

- debug: msg={{r__ansible_vault_encrypt}}

- name: ansible_vault_pipe.encrypt | Decrypt using user-provided vaultid and vaultpass
  dseeley.ansible_vault_pipe.decrypt:
    vaultid: sandbox
    vaultpass: asdf
    vaulttext: "$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165"
  register: r__ansible_vault_decrypt

- debug: msg={{r__ansible_vault_decrypt}}

- name: ansible_vault_pipe.encrypt | Encrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
  dseeley.ansible_vault_pipe.encrypt:
    multiline_out: true
    plaintext: "sometext"
  register: r__ansible_vault_encrypt

- debug: msg={{r__ansible_vault_encrypt}}

- name: ansible_vault_pipe.encrypt | Decrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
  dseeley.ansible_vault_pipe.decrypt:
    vaulttext: "$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165"
  register: r__ansible_vault_decrypt

- debug: msg={{r__ansible_vault_decrypt}}
``` 

---

### Lookup Plugin

Use inline in Jinja2 expressions for quick encrypt/decrypt operations.

#### Examples
```yaml
- name: ansible_vault_pipe.encrypt | Encrypt using user-provided vaultid and vaultpass
  debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.encrypt', 'sometext', vaultid='sandbox', vaultpass='asdf') }}"

- name: ansible_vault_pipe.encrypt | Decrypt using user-provided vaultid and vaultpass
  debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.decrypt', '$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165', vaultid='sandbox', vaultpass='asdf') }}"

- name: ansible_vault_pipe.encrypt | Encrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
  debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.encrypt', 'sometext', multiline_out=true) }}"

- name: ansible_vault_pipe.decrypt | Decrypt using already-loaded vault secrets (from command-line, ansible.cfg etc)
  debug:
    msg: "{{ lookup('dseeley.ansible_vault_pipe.decrypt', '$ANSIBLE_VAULT;1.2;AES256;sandbox\n303562383536366435346466313764636533353438653463373765616365623130333633613139326235633064643338316665653531663030643139373131390a323233356239303864343336663238616535386638646566623036383130643638373465646331316664636564376161376137623432616561343631313262620a3561656131353364616136373866343963626561366236653538633734653165') }}"
```
# RHEL Storage Health Check (Ansible)

Ansible playbook and role that perform a comprehensive storage health check on **Red Hat Enterprise Linux** hosts. Results are aggregated into a single structured variable, `storage_health_report`, on each target host.

## What it checks

| Category | Detection method |
|----------|------------------|
| Local filesystems (`ext4`, `xfs`, `btrfs`, …) | `ansible_mounts` from `ansible.builtin.setup` |
| LVM logical volumes | Device map from `lvs` JSON + `ansible_lvm` facts |
| SMB/CIFS shares | `fstype` of `cifs` or `smb3` |
| Volume Group free space | `vgs` JSON (bytes) + `community.general.lvg` (`state: info`) |

## Requirements

- Ansible 2.14+
- Target hosts: RHEL 8+ with `lvm2` package (standard on LVM-backed systems)
- Controller: `community.general` collection

```bash
ansible-galaxy collection install -r requirements.yml
```

## Quick start

1. Edit `inventory/hosts.yml` with your RHEL hosts.
2. Run the playbook:

```bash
ansible-playbook playbooks/storage_health_check.yml
```

3. Read the report from host vars (example):

```bash
ansible rhel_hosts -m debug -a "var=storage_health_report" -o
```

Or enable optional console output:

```bash
ansible-playbook playbooks/storage_health_check.yml -e storage_health_debug_output=true
```

## Report structure

`storage_health_report` is a **list of dictionaries**. Mount entries include:

| Key | Description |
|-----|-------------|
| `mount_point` | Filesystem mount path |
| `storage_type` | `local`, `lvm`, or `smb_cifs` |
| `total_size` | Human-readable total capacity |
| `percent_available` | Free space % on the mount |
| `vg_free_space` | Unallocated space in the backing VG (LVM mounts only) |

Additional VG summary rows use `storage_type: lvm_volume_group` with `mount_point: null` to expose VG-level free space explicitly.

## Project layout

```
playbooks/storage_health_check.yml   # Main playbook
roles/storage_health_check/          # Role (tasks, defaults, filter plugin)
inventory/hosts.yml                  # Example inventory
requirements.yml                     # Galaxy collections
```

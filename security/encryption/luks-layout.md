# AetherOS Encryption Layout

- ESP: FAT32, unencrypted
- /boot: ext4, optional unencrypted or unified kernel image flow
- Root: LUKS2 encrypted block device
- Filesystem: BTRFS default with snapshot subvolumes for rollback

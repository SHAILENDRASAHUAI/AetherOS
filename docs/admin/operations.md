# AetherOS Admin Guide (Draft)

## Build Artifacts

Run `./scripts/build.sh` to produce edition artifacts and checksums.

## Security Baseline

- enforce secure boot and signed updates
- keep SELinux/AppArmor profiles enabled
- deploy nftables baseline before network exposure

## Recovery

Use Recovery edition to run snapshot restore, boot repair, network repair, and password reset workflows.

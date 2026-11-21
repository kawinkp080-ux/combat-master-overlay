# HWID Spoofer setup (educational)

The `HwidSpoofer` class in `src/Infrastructure/HwidSpoofer.py` only computes a
deterministic hash of your SMBIOS UUID — it does **not** modify hardware identifiers.

To actually rotate identifiers you would need a signed kernel driver. We do not ship one.
If you're researching detection surfaces, read the driver-loading rules in `SECURITY.md`
first and only test on disposable VMs.
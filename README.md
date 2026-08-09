# EquipmentRENTALbyLC

UiPath Cloud equipment-rental lifecycle demonstration.

## Design artifacts

- [Corrected mock data model](docs/equipment-rental-data-model.md)
- [Solution Design Document](docs/equipment-rental-solution-sdd.md)
- [Solution delivery plan](docs/plans/equipment-rental-uipath-solution-plan.md)
- [Product requirements](docs/plans/prd-equipment-rental-uipath-solution.md)
- [Test specification](docs/plans/test-spec-equipment-rental-uipath-solution.md)

## Mock data naming standard

Generated dataset files use the human-readable convention:

```text
EquipmentRENTAL_LCversion_<EntityName>.csv
```

The dataset covers rental history from **2024-08-09 through 2026-08-09** and
daily vendor-equipment availability through **2029-02-09**. Regenerate it with:

```bash
python3 scripts/generate_mock_data.py
```

## GitHub repository access

| Item | Value |
|---|---|
| Repository | `git@github.com:Laurentcadieux/EquipmentRENTAL.git` |
| Access method | Project-specific ED25519 SSH deploy key |
| Private-key path | `/root/.ssh/id_ed25519_equipmentrental_lcversion` |
| Public-key path | `/root/.ssh/id_ed25519_equipmentrental_lcversion.pub` |
| Key fingerprint | `SHA256:PR8kEJ8DEFnRsGRYkt6PBJ+HmxB+pjHuAx39Voxlf3E` |

The private key must never be committed, copied into documentation, or shared.
Use this repository-specific key when Git operations require SSH authentication:

```bash
GIT_SSH_COMMAND='ssh -i /root/.ssh/id_ed25519_equipmentrental_lcversion -o IdentitiesOnly=yes' \
  git ls-remote origin
```

- [UiPath solution plan](docs/plans/equipment-rental-uipath-solution-plan.md)

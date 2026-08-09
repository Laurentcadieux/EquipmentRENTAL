#!/usr/bin/env bash
set -euo pipefail
repo=/root/EquipmentRENTALbyLC
cd "$repo"
git add -A
if ! git diff --cached --quiet; then
  git commit -m "Preserve EquipmentRental build progress

Automated checkpoint of work completed during the active UiPath solution build.

Constraint: Periodic synchronization requested by project owner
Confidence: high
Scope-risk: narrow
Reversibility: clean
Directive: Review automated checkpoints before release promotion
Tested: Git status and remote push
Not-tested: UiPath runtime behavior"
fi
git push origin master

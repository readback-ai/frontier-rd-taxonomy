"""Intervention records and the pacing model agree on policy names.

The model in pacing-takeoff-model/ is kept free of references to the records, so that its
directory can be published as it stands. This check therefore lives on the records' side.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def test_intervention_records_name_policies_the_model_has():
    sys.path.insert(0, str(ROOT / "pacing-takeoff-model"))
    import pacing_model

    names = {p.name for p in pacing_model.standard_policies(pacing_model.load_calibration())}
    records = sorted((ROOT / "data" / "interventions").glob("*.yml"))
    assert records
    for record in records:
        policy = yaml.safe_load(record.read_text()).get("pacing_policy")
        assert policy is None or policy in names, (record.name, policy)

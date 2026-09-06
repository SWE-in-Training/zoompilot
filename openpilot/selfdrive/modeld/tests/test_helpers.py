import pytest

from openpilot.common.test import OpenpilotTestCase
from openpilot.selfdrive.modeld.helpers import MODELD_PKL_KEYS, check_modeld_pkl


class TestCheckModeldPkl(OpenpilotTestCase):
  def test_current_schema_passes(self):
    check_modeld_pkl(dict.fromkeys(MODELD_PKL_KEYS), "driving_tinygrad.pkl")

  def test_pre_run_model_schema_is_named(self):
    # the pkl shape compile_modeld.py wrote before the warp and policy jits were fused:
    # sunnypilot staging 3e87c0f shipped one against a modeld that reads the fused shape
    stale = {'metadata': {}, 'run_policy': None, (1928, 1208): None, (1344, 760): None}
    with pytest.raises(RuntimeError, match=r"driving_tinygrad.pkl is missing \['input_devices', 'run_model'\]"):
      check_modeld_pkl(stale, "driving_tinygrad.pkl")

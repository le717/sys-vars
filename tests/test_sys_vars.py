import unittest
from datetime import datetime
from os import environ
from pathlib import Path


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Set an alternative path for sys vars for testing
        environ["SYS_VARS_PATH"] = "./tests/secrets"

        # Put a value in the environment
        environ["DEPLOY_ENV"] = "development"

        # Because the library sets the sys vars path at compile time,
        # we need to import it here and make it a global variable
        global sys_vars
        import sys_vars

    def test_not_found_sys_var_w_default(self) -> None:
        val = sys_vars.get("NON_EXISTENT_SYSTEM_VARIABLE", default="this-is-the-default")
        self.assertEqual(val, "this-is-the-default")

    def test_not_found_sys_var_wo_default(self) -> None:
        with self.assertRaises(sys_vars.SysVarNotFoundError):
            sys_vars.get("NON_EXISTENT_SYSTEM_VARIABLE")

    def test_get_sys_var(self) -> None:
        val = sys_vars.get("DEPLOY_ENV")
        self.assertEqual(val, "development")

    def test_get_str(self) -> None:
        val = sys_vars.get("HOST_ADDRESS")
        self.assertIsInstance(val, str)

    def test_get_bool(self) -> None:
        val = sys_vars.get_bool("DEBUG_MODE")
        self.assertIsInstance(val, bool)

    def test_get_bool_truthy_str(self) -> None:
        val = sys_vars.get_bool("AUTO_CONFIRM")
        self.assertIsInstance(val, bool)
        self.assertTrue(val)

    def test_get_bool_false_float(self) -> None:
        val = sys_vars.get_bool("BOOLEAN_FALSE_FLOAT_NUMBER")
        self.assertIsInstance(val, bool)
        self.assertFalse(val)

    def test_get_bool_true_int(self) -> None:
        val = sys_vars.get_bool("BOOLEAN_TRUE_INT_NUMBER")
        self.assertIsInstance(val, bool)
        self.assertTrue(val)

    def test_get_bool_default(self) -> None:
        val = sys_vars.get_bool("NON_EXISTENT_SYSTEM_VARIABLE", default=False)
        self.assertIsInstance(val, bool)

    def test_get_datetime(self) -> None:
        val = sys_vars.get_datetime("LAST_SYNC_RUN")
        self.assertIsInstance(val, datetime)

    def test_get_datetime_default(self) -> None:
        val = sys_vars.get_datetime("NON_EXISTENT_SYSTEM_VARIABLE", default=datetime.now())
        self.assertIsInstance(val, datetime)

    def test_get_datetime_fail_cast(self) -> None:
        with self.assertRaises(ValueError):
            sys_vars.get_datetime("BOOLEAN_TRUE_INT_NUMBER")

    def test_get_int(self) -> None:
        val = sys_vars.get_int("THE_MEANING_OF_LIFE")
        self.assertIsInstance(val, int)

    def test_get_int_fail_cast(self) -> None:
        with self.assertRaises(ValueError):
            sys_vars.get_int("pi")

    def test_get_float(self) -> None:
        val = sys_vars.get_float("pi")
        self.assertIsInstance(val, float)

    def test_get_float_fail_cast(self) -> None:
        with self.assertRaises(ValueError):
            sys_vars.get_float("ABBR_MAPPING_DICT")

    def test_get_json_dict(self) -> None:
        val = sys_vars.get_json("ABBR_MAPPING_DICT")
        self.assertIsInstance(val, dict)

    def test_get_json_list(self) -> None:
        val = sys_vars.get_json("USER_ID_LIST")
        self.assertIsInstance(val, list)

    def test_get_json_default(self) -> None:
        val = sys_vars.get_json("NON_EXISTENT_SYSTEM_VARIABLE", default={"exists": True})
        self.assertIsInstance(val, dict)

    def test_get_json_fail_cast(self) -> None:
        from json import JSONDecodeError

        with self.assertRaises(JSONDecodeError):
            sys_vars.get_json("LAST_SYNC_RUN")

    def test_get_path(self) -> None:
        p = sys_vars.get_path("SOME_FILE_PATH")
        self.assertIsInstance(p, Path)

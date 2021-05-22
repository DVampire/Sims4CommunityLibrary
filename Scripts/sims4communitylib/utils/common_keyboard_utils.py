"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
import os

from sims4communitylib.enums.common_key_code import CommonKey
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.modinfo import ModInfo

# noinspection PyBroadException
try:
    if os.name == 'nt':
        import ctypes_module as _ctypes_module
        _user32 = _ctypes_module.WinDLL('user32', use_last_error=True)

        def _can_detect_key_state_for_current_os() -> bool:
            return _user32 is not None

        def _is_holding_key_down(key: CommonKey) -> bool:
            key_code = _translate_to_key_code(key)
            if key_code == -1:
                return False
            return _user32.GetKeyState(key_code) > 1

        def _is_key_toggled_on(key: CommonKey):
            key_code = _translate_to_key_code(key)
            if key_code == -1:
                return False
            return _user32.GetKeyState(key_code) == 1

        def _translate_to_key_code(key: CommonKey) -> int:
            if isinstance(key, int):
                return key
            if key is None:
                return -1
            try:
                if isinstance(key, CommonKey):
                    letter_key = key.name.replace('KEY_', '')
                    if len(letter_key) != 1:
                        return int(key)

                    virtual_key = _user32.VkKeyScanW(ord(letter_key))
                    if virtual_key == -1:
                        return int(key)

                    mapped_virtual_key = _user32.MapVirtualKeyW(virtual_key & 255, 0)
                    mapped_scan_key = _user32.MapVirtualKeyW(mapped_virtual_key & 255, 1)
                    if mapped_scan_key == 0:
                        return int(key)
                    return mapped_scan_key
            except Exception as ex:
                CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'An error occurred while translating key to key code. {}'.format(key.name), exception=ex)
            return int(key)
    else:
        # noinspection PyUnresolvedReferences, PyPackageRequirements
        import Quartz as _Quartz

        def _can_detect_key_state_for_current_os() -> bool:
            return _Quartz.CGEventSourceKeyState is not None

        def _is_holding_key_down(key: CommonKey) -> bool:
            key_code = _translate_to_key_code(key)
            if key_code == -1:
                return False
            return bool(_Quartz.CGEventSourceKeyState(_Quartz.kCGEventSourceStateHIDSystemState, key_code))

        def _is_key_toggled_on(key: CommonKey):
            return _is_holding_key_down(key)

        def _translate_to_key_code(key: CommonKey) -> int:
            if key is None:
                return -1
            return int(key)
except:
    def _can_detect_key_state_for_current_os() -> bool:
        return False

    def _is_holding_key_down(_: CommonKey) -> bool:
        return False

    def _is_key_toggled_on(_: CommonKey) -> bool:
        return False

    def _translate_to_key_code(key: CommonKey) -> int:
        if key is None:
            return -1
        return int(key)


class CommonKeyboardUtils:
    """Utilities for manipulating the keyboard."""
    @staticmethod
    def can_detect_key_state_for_current_os() -> bool:
        """can_detect_key_state_for_current_os()

        Determine if CommonKeyboardUtils can detect the state of a key on the keyboard for the current Operating System.

        :return: True, if CommonKeyboardUtils can detect the state of a key on the keyboard for the current Operating System. False, if not.
        :rtype: bool
        """
        return _can_detect_key_state_for_current_os()

    @staticmethod
    def is_holding_key_down(key: CommonKey) -> bool:
        """is_holding_key_down(key)

        Determine if the player is holding a keyboard key down.

        :param key: The Key to check.
        :type key: CommonKey
        :return: True, if the player is holding the specified key down. False, if not.
        :rtype: bool
        """
        return _is_holding_key_down(key)

    @staticmethod
    def key_is_toggled_on(key: CommonKey) -> bool:
        """key_is_toggled_on(key)

        Determine if the player has a key set to the ON state, such as the CAPS LOCK key.

        :param key: The Key to check.
        :type key: CommonKey
        :return: True, if the player has the specified key set to the ON state. False, if not.
        :rtype: bool
        """
        return _is_key_toggled_on(key)

    @staticmethod
    def translate_to_key_code(key: CommonKey) -> int:
        """translate_to_key_code(key)

        Translate a Key to its Key Code counterpart.

        :param key: The Key to convert.
        :type key: CommonKey
        :return: The integer representation of the specified key or -1 if not found.
        :rtype: int
        """
        return _translate_to_key_code(key)

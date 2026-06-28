from fingerprints.models import FingerprintDefinition


PROTON_FINGERPRINTS = [

    FingerprintDefinition(
        id="PROTON_PREFIX_CORRUPTED",
        display_name="Corrupted Proton Prefix",
        short_description="The Proton/Wine prefix is damaged or missing critical files.",
        category="Proton Prefix",
        severity="high",
        patterns=[
            "wine: could not load kernel32.dll",
            "could not load kernel32.dll",
            "wine: cannot find",
            "prefix is unusable",
            "failed to open prefix",
            "wine prefix is not configured",
        ],
        causes=["PROTON_WINEBOOT_FAILURE", "PROTON_REGISTRY_FAILURE", "WINE_CRASH"],
        known_fix=[
            "Verify game files in Steam.",
            "Try switching to a different Proton version.",
            "Delete the Proton prefix and let Steam recreate it.",
        ],
        safe_commands=[
            "ls ~/.steam/steam/steamapps/compatdata/",
        ],
        icon="proton",
    ),

    FingerprintDefinition(
        id="PROTON_WINEBOOT_FAILURE",
        display_name="Proton Wineboot Failed",
        short_description="Wineboot failed during prefix setup or update.",
        category="Proton Prefix",
        severity="high",
        patterns=[
            "wineboot failed",
            "wineboot.exe failed",
            "wineboot: failed",
            "wine: failed to start",
            "wineserver: failed to create",
            "err:wineboot:",
        ],
        causes=["WINE_CRASH"],
        known_fix=[
            "Switch to a different Proton version.",
            "Verify game files in Steam.",
            "Delete the prefix and let Proton rebuild it.",
        ],
        safe_commands=[],
        icon="proton",
    ),

    FingerprintDefinition(
        id="PROTON_DLL_MISSING",
        display_name="Missing DLL",
        short_description="Proton or Wine could not load a required DLL.",
        category="Proton Dependency",
        severity="medium",
        patterns=[
            "failed to open dll",
            "err:module:import_dll",
            "err:module:load_dll",
            "could not load dll",
            "err:winediag:nodrv",
            "no driver found",
        ],
        known_fix=[
            "Verify game files in Steam.",
            "Try a clean Proton prefix.",
            "Do not manually download DLL files.",
        ],
        safe_commands=[],
        icon="proton",
    ),

    FingerprintDefinition(
        id="PROTON_REGISTRY_FAILURE",
        display_name="Wine Registry Failure",
        short_description="Wine could not open or write a required registry key.",
        category="Registry",
        severity="medium",
        patterns=[
            "failed to open registry key",
            "err:reg:open_key",
            "err:reg:create_key",
            "could not open registry",
            "registry key not found",
        ],
        known_fix=[
            "Try a clean Proton prefix.",
            "Switch Proton versions.",
            "Verify game files in Steam.",
        ],
        safe_commands=[],
        icon="proton",
    ),

    FingerprintDefinition(
        id="MEDIA_FOUNDATION_RELATED",
        display_name="Media Foundation Missing",
        short_description="The game requires Windows Media Foundation for video or audio playback.",
        category="Media Foundation",
        severity="medium",
        patterns=[
            "mfplat",
            "mf.dll",
            "mfreadwrite",
            "wmvcore",
            "windowsmediafoundation",
            "err:module:import_dll mfplat.dll",
            "err:module:import_dll mf.dll",
        ],
        known_fix=[
            "Use GE-Proton — it includes Media Foundation patches.",
            "Check ProtonDB for game-specific Media Foundation workarounds.",
            "If the issue is only intro videos, try pressing ESC to skip them.",
        ],
        safe_commands=[],
        icon="proton",
    ),

    FingerprintDefinition(
        id="PROTON_XINPUT_FAILURE",
        display_name="XInput Controller Failure",
        short_description="Proton could not initialize XInput for controller support.",
        category="Proton Dependency",
        severity="low",
        patterns=[
            "xinput",
            "err:xinput:",
            "xinput1_3.dll",
            "xinput9_1_0.dll",
        ],
        known_fix=[
            "Check whether a controller is connected and recognized by the system.",
            "Try a different Proton version.",
            "Use Steam Input instead of direct XInput if the game supports it.",
        ],
        safe_commands=["ls /dev/input/"],
        icon="proton",
    ),

    FingerprintDefinition(
        id="WINE_CRASH",
        display_name="Wine/Proton Crash",
        short_description="Wine or Proton crashed while running the game.",
        category="Wine",
        severity="medium",
        patterns=[
            "unhandled page fault",
            "segmentation fault",
            "core dumped",
            "err:seh:setup_exception",
            "err:seh:call_stack_handlers",
            "wine client error",
            "crashed with",
        ],
        causes=[],
        known_fix=[
            "Check earlier errors in the log for the root cause.",
            "Try a different Proton version.",
            "Disable overlays and custom launch options.",
            "Verify game files in Steam.",
        ],
        safe_commands=[],
        icon="proton",
    ),

    FingerprintDefinition(
        id="NTDLL_RELATED_CRASH",
        display_name="ntdll Crash",
        short_description="A crash involving ntdll, a core Wine compatibility component.",
        category="Wine",
        severity="medium",
        patterns=[
            "ntdll",
            "err:ntdll:",
            "ntdll.dll",
            "RtlRaiseException",
        ],
        known_fix=[
            "Look for earlier errors before the ntdll crash.",
            "Try a different Proton version.",
            "Disable overlays and launch options.",
            "Verify game files.",
        ],
        safe_commands=[],
        icon="proton",
    ),

]

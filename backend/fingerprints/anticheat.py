from fingerprints.models import FingerprintDefinition


ANTICHEAT_FINGERPRINTS = [

    FingerprintDefinition(
        id="EAC_FAILURE",
        display_name="Easy Anti-Cheat Failure",
        short_description="Easy Anti-Cheat failed to initialize or blocked the game.",
        category="Anti-Cheat",
        severity="high",
        patterns=[
            "easyanticheat",
            "easy anti-cheat",
            "eac: failed",
            "easyanticheat: error",
            "easyanticheat failed to initialize",
            "eac initialization failed",
        ],
        known_fix=[
            "Check ProtonDB to confirm whether EAC works for this game on Proton.",
            "Verify game files in Steam.",
            "Use the Proton version recommended by ProtonDB for this game.",
            "Do not troubleshoot graphics until EAC is confirmed working.",
        ],
        safe_commands=[],
        icon="anticheat",
    ),

    FingerprintDefinition(
        id="EAC_EOS_RELATED",
        display_name="Easy Anti-Cheat EOS",
        short_description="Easy Anti-Cheat EOS component encountered a problem.",
        category="Anti-Cheat",
        severity="high",
        patterns=[
            "easyanticheat eos",
            "eac eos",
            "easyanticheat_eos",
            "epiconlineservices",
            "eos sdk",
            "eos: failed",
        ],
        known_fix=[
            "Verify game files in Steam.",
            "Use the Proton version recommended by ProtonDB for this game.",
            "Ensure the Epic Online Services overlay is not disabled.",
        ],
        safe_commands=[],
        icon="anticheat",
    ),

    FingerprintDefinition(
        id="EAC_LINUX_RUNTIME_RELATED",
        display_name="Easy Anti-Cheat Linux Runtime",
        short_description="The native Linux EAC runtime was detected.",
        category="Anti-Cheat",
        severity="high",
        patterns=[
            "easyanticheat_x64.so",
            "easyanticheat_x86.so",
            "eac_linux",
            "easyanticheat.so",
        ],
        known_fix=[
            "Verify game files in Steam.",
            "Restart Steam and try again.",
            "Use Proton Experimental if using an older Proton version.",
        ],
        safe_commands=[],
        icon="anticheat",
    ),

    FingerprintDefinition(
        id="BATTLEYE_FAILURE",
        display_name="BattlEye Failure",
        short_description="BattlEye anti-cheat failed to initialize or blocked the game.",
        category="Anti-Cheat",
        severity="high",
        patterns=[
            "battleye",
            "battle eye",
            "be service failed",
            "battleye: error",
            "battleye failed",
            "battleye: service failed",
            "battleye initialization failed",
        ],
        known_fix=[
            "Check ProtonDB to confirm whether BattlEye works for this game on Proton.",
            "Verify game files in Steam.",
            "Use the Proton version recommended by ProtonDB for this game.",
            "Try Proton Experimental.",
        ],
        safe_commands=[],
        icon="anticheat",
    ),

    FingerprintDefinition(
        id="BATTLEYE_LAUNCHER_RELATED",
        display_name="BattlEye Launcher Issue",
        short_description="The BattlEye launcher component encountered a problem.",
        category="Anti-Cheat",
        severity="high",
        patterns=[
            "battleye launcher",
            "be launcher",
            "belauncher",
        ],
        known_fix=[
            "Verify game files in Steam.",
            "Try Proton Experimental.",
            "Check ProtonDB for current BattlEye compatibility reports.",
        ],
        safe_commands=[],
        icon="anticheat",
    ),

]

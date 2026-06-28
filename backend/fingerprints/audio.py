from fingerprints.models import FingerprintDefinition


AUDIO_FINGERPRINTS = [

    FingerprintDefinition(
        id="XAUDIO_RELATED",
        display_name="XAudio2 Issue",
        short_description="XAudio2, the Windows audio component, encountered a problem.",
        category="Audio",
        severity="medium",
        patterns=[
            "xaudio2",
            "xaudio2_7",
            "xaudio2_8",
            "xaudio2_9",
            "err:xaudio2:",
            "failed to initialize xaudio",
            "xaudio: failed",
        ],
        known_fix=[
            "Check that system audio is working outside the game.",
            "Set the audio output device in the game to 'Default'.",
            "Try a different Proton version.",
            "If using PipeWire, ensure pipewire-pulse is running.",
        ],
        safe_commands=[
            "pactl info",
            "systemctl --user status pipewire pipewire-pulse",
        ],
        icon="audio",
    ),

    FingerprintDefinition(
        id="FAUDIO_RELATED",
        display_name="FAudio Issue",
        short_description="FAudio (XAudio compatibility layer) encountered a problem.",
        category="Audio",
        severity="medium",
        patterns=[
            "faudio",
            "faudio: failed",
            "faudio: error",
            "err:faudio:",
            "failed to create faudio",
        ],
        known_fix=[
            "Check that audio works in other applications.",
            "Restart PipeWire: systemctl --user restart pipewire pipewire-pulse.",
            "Update Proton.",
        ],
        safe_commands=[
            "pactl info",
        ],
        icon="audio",
    ),

    FingerprintDefinition(
        id="PULSEAUDIO_RELATED",
        display_name="PulseAudio/PipeWire Audio Issue",
        short_description="The audio server reported a problem with audio routing.",
        category="Audio",
        severity="low",
        patterns=[
            "pulse audio",
            "pulseaudio",
            "pipewire-pulse",
            "pa_context_connect failed",
            "audio device not found",
            "failed to connect to pulseaudio",
        ],
        known_fix=[
            "Check the active audio server: pactl info.",
            "Restart PipeWire or PulseAudio.",
            "Test with the default audio output device.",
        ],
        safe_commands=[
            "pactl info",
            "systemctl --user status pipewire",
        ],
        icon="audio",
    ),

    FingerprintDefinition(
        id="ALSA_AUDIO_FAILURE",
        display_name="ALSA Audio Failure",
        short_description="ALSA (Linux audio subsystem) reported an error.",
        category="Audio",
        severity="low",
        patterns=[
            "alsa: failed",
            "alsa lib",
            "snd_pcm_open failed",
            "alsa: cannot open audio device",
            "cannot open audio device",
        ],
        known_fix=[
            "Check that audio is working outside the game.",
            "Try a different Proton version.",
            "Set audio to use a default device.",
        ],
        safe_commands=[
            "aplay -l",
            "pactl info",
        ],
        icon="audio",
    ),

    FingerprintDefinition(
        id="OPENAL_AUDIO_FAILURE",
        display_name="OpenAL Audio Failure",
        short_description="OpenAL could not initialize or find an audio device.",
        category="Audio",
        severity="low",
        patterns=[
            "openal: failed",
            "openal32.dll",
            "al: failed to open device",
            "openal: cannot open audio",
            "err:openal:",
        ],
        known_fix=[
            "Check that audio is working outside the game.",
            "Try a different Proton version.",
            "Try setting WINEDLLOVERRIDES=openal=b in launch options.",
        ],
        safe_commands=["pactl info"],
        icon="audio",
    ),

]

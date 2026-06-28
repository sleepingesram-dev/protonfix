export const fingerprintNames: Record<string, string> = {
  VULKAN_DRIVER_MISSING: "Missing or Broken Vulkan Driver",
  VULKAN_INIT_FAILURE: "Vulkan Initialization Failure",
  DXVK_ADAPTER_FAILURE: "DXVK Graphics Adapter Failure",
  DXVK_RELATED_FAILURE: "DXVK Failure",
  VKD3D_RELATED_FAILURE: "VKD3D Failure",
  WINE_CRASH: "Wine Crash",
  EAC_FAILURE: "Easy Anti-Cheat Failure",
  BATTLEYE_FAILURE: "BattlEye Failure",
  GAMESCOPE_FAILURE: "Gamescope Failure",
  MANGOHUD_FAILURE: "MangoHud Failure",
  STEAM_RUNTIME_FAILURE: "Steam Runtime Failure",
  GAMEMODE_RELATED: "GameMode Issue",
  PKEXEC_PERMISSION_ISSUE: "Permission Issue",
  SEGFAULT: "Segmentation Fault",
  CORE_DUMPED: "Application Crash",
};

export function humanizeFingerprint(id?: string) {
  if (!id) return null;

  if (fingerprintNames[id]) {
    return fingerprintNames[id];
  }

  return id
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

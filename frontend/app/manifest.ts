import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "ProtonFix",
    short_name: "ProtonFix",
    description:
      "Linux gaming log analyzer for Proton, Steam, DXVK, VKD3D, and Vulkan issues.",
    start_url: "/",
    display: "standalone",
    background_color: "#09090b",
    theme_color: "#2563eb",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
    ],
  };
}

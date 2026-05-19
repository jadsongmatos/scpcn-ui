import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";

import { Button } from "@/components/ui/warcraftcn/button";

export const metadata: Metadata = {
  title: "404 | SCP-CN UI",
};

export default function NotFound() {
  return (
    <div className="grid h-screen w-full place-content-center gap-5 bg-background px-4 text-center">
<Image
      alt="SCP 404"
      height={300}
      src={"/404/pixel-orc.webp"}
      width={300}
    />

    <h1 className="font-bold text-2xl tracking-tight sm:text-4xl">CONTAINMENT BREACH</h1>

    <p className="text-gray-500">Entity not found. This page does not exist.</p>
      <Link href={"/"}>
<Button className="p-5 px-10" variant="frame">
        Return to Site
      </Button>
      </Link>
    </div>
  );
}

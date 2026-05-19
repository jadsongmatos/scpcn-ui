import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/warcraftcn/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/warcraftcn/card";

export default function Home() {
  return (
    <div className="flex flex-col items-center px-4 pb-3">
      <h1 className="sr-only">SCP-CN UI — Foundation-style UI components</h1>

      {/* Gradient glow background */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute top-1/2 left-1/2 h-[800px] w-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[radial-gradient(circle,rgba(180,20,20,0.5)_0%,rgba(180,20,20,0.3)_20%,rgba(60,60,60,0.25)_50%,transparent_75%)] blur-[100px]" />
      </div>

      <Card className="relative z-10 h-[750px] max-w-xl">
        <CardHeader className="text-white">
<CardTitle className="text-center font-bold text-2xl md:text-4xl">
          SCP-CN
        </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-center justify-center gap-2 pt-5">
          <Image
            alt="logo"
            className="size-50 md:h-80 md:w-80"
            height={300}
            src="/warcraftcn-logo.png"
            width={300}
          />
<p className="text-center text-white">
          A set of components inspired by SCP Foundation bureaucratic
          aesthetics. Clinical, monospace, redacted. Open source, copy
          paste ready. Works with your favorite frameworks.
        </p>
        </CardContent>
        <CardFooter className="flex flex-col items-center justify-center gap-4">
          <Link href="/docs">
            <Button className="px-10 text-xl">Get Started</Button>
          </Link>
        </CardFooter>
      </Card>
    </div>
  );
}

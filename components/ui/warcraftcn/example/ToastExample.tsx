"use client";
import { useState } from "react";
import { triggerScrollToast } from "@/components/ui/warcraftcn/toast";
import { Button } from "@/components/ui/warcraftcn/button";
import {
  RadioGroup,
  RadioGroupItem,
} from "@/components/ui/warcraftcn/radio-group";
import { Label } from "@/components/ui/warcraftcn/label";

type Classification = "safe" | "euclid" | "keter" | "thaumiel" | "apollyon";
type Variant = "default" | "success" | "error" | "warning" | "info";
type Position =
  | "top-left"
  | "top-center"
  | "top-right"
  | "bottom-left"
  | "bottom-center"
  | "bottom-right";

const classificationQuotes: Record<Classification, string> = {
  safe: "Item is benign. Proceed as normal.",
  euclid: "Behavior is unpredictable. Caution advised.",
  keter: "Hostile and uncontainable. Full alert.",
  thaumiel: "Used for containment. Trust the protocol.",
  apollyon: "Inevitable breach. Prepare for end-of-world."
};

const variantClassificationMessages: Record<Classification, Record<Variant | "default", string>> = {
  safe: {
    success: "SCP secured successfully.",
    error: "Containment anomaly detected.",
    warning: "Minor deviation from baseline.",
    info: "Routine monitoring update.",
    default: classificationQuotes.safe
  },
  euclid: {
    success: "Euclid-class item recontained.",
    error: "Behavioral shift detected.",
    warning: "Euclid parameters exceeded.",
    info: "New behavioral data recorded.",
    default: classificationQuotes.euclid
  },
  keter: {
    success: "Emergency Keter lockdown engaged!",
    error: "Containment failure imminent!",
    warning: "Keter-class escalation warning.",
    info: "Threat level reassessment needed.",
    default: classificationQuotes.keter
  },
  thaumiel: {
    success: "Thaumiel protocol active.",
    error: "Countermeasure malfunction.",
    warning: "Thaumiel asset destabilizing.",
    info: "Cross-classification update.",
    default: classificationQuotes.thaumiel
  },
  apollyon: {
    success: "XK-class scenario postponed.",
    error: "Irreversible breach in progress.",
    warning: "Apollyon-class event window.",
    info: "End-of-world monitoring report.",
    default: classificationQuotes.apollyon
  }
};

const classifications: { label: string; value: Classification }[] = [
  { label: "Safe", value: "safe" },
  { label: "Euclid", value: "euclid" },
  { label: "Keter", value: "keter" },
  { label: "Thaumiel", value: "thaumiel" },
  { label: "Apollyon", value: "apollyon" },
];

const positions: { label: string; value: Position }[] = [
  { label: "Top Left", value: "top-left" },
  { label: "Top Center", value: "top-center" },
  { label: "Top Right", value: "top-right" },
  { label: "Bottom Left", value: "bottom-left" },
  { label: "Bottom Center", value: "bottom-center" },
  { label: "Bottom Right", value: "bottom-right" },
];

const variants: { label: string; value: Variant }[] = [
  { label: "Default", value: "default" },
  { label: "Success", value: "success" },
  { label: "Error", value: "error" },
  { label: "Warning", value: "warning" },
  { label: "Info", value: "info" },
];

const ToastExample = () => {
  const [classification, setClassification] = useState<Classification>("safe");
  const [position, setPosition] = useState<Position>("top-center");
  const [variant, setVariant] = useState<Variant>("default");

  const handleShowToast = () => {
    const classMap = variantClassificationMessages[classification] ?? variantClassificationMessages.safe;
    const message = classMap[variant] ?? classMap.default ?? "SCP Foundation notice";

    triggerScrollToast({
      message,
      classification,
      position,
      variant,
    });
  };

  return (
    <div
      className="w-[90vw] md:w-full md:p-2 p-8"
      style={{
        backgroundImage: "url('/warcraftcn/textarea-bg.webp')",
        backgroundSize: "100% 100%"
      }}
    >
      <div className="flex flex-col gap-6 p-4 sm:p-10">
        <fieldset className="mb-2 sm:mb-6">
          <legend className="font-semibold mb-2 sm:mb-3 text-white">Classification</legend>
          <RadioGroup
            defaultValue="safe"
            onValueChange={(val: Classification) => setClassification(val)}
          >
            <div className="flex flex-col lg:flex-row items-start lg:items-center gap-2 lg:gap-4">
              {classifications.map((c) => (
                <div className="flex items-center gap-2" key={c.value}>
                  <RadioGroupItem value={c.value} id={`classification-${c.value}`} />
                  <Label htmlFor={`classification-${c.value}`}>{c.label}</Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        </fieldset>

        <fieldset className="mb-2 sm:mb-6">
          <legend className="font-semibold mb-2 sm:mb-3 text-white">Position</legend>
          <RadioGroup
            defaultValue="top-center"
            onValueChange={(val: Position) => setPosition(val)}
          >
            <div className="flex flex-col lg:flex-row items-start lg:items-center gap-2 lg:gap-4">
              {positions.map((pos) => (
                <div className="flex items-center gap-2" key={pos.value}>
                  <RadioGroupItem value={pos.value} id={`position-${pos.value}`} />
                  <Label htmlFor={`position-${pos.value}`}>{pos.label}</Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        </fieldset>

        <fieldset className="mb-2 sm:mb-6">
          <legend className="font-semibold mb-2 sm:mb-3 text-white">Variant</legend>
          <RadioGroup
            defaultValue="default"
            onValueChange={(val: Variant) => setVariant(val)}
          >
            <div className="flex flex-col lg:flex-row items-start lg:items-center gap-2 lg:gap-4">
              {variants.map((v) => (
                <div className="flex items-center gap-2" key={v.value}>
                  <RadioGroupItem value={v.value} id={`variant-${v.value}`} />
                  <Label htmlFor={`variant-${v.value}`}>{v.label}</Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        </fieldset>
        <div>
          <Button variant="frame" onClick={handleShowToast} className="w-[200px] md:min-w-xs py-3 px-6">
            Show Toast
          </Button>
        </div>
      </div>
    </div>
  );
};

export { ToastExample };

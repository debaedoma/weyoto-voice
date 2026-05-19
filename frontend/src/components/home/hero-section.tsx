import { siteConfig } from "@/lib/constants";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden px-4 pb-8 pt-12 sm:px-6 sm:pb-10 sm:pt-16 lg:pt-20">
      {/* Background gradient */}
      <div
        className="absolute inset-0 -z-10 bg-gradient-to-b from-primary/5 via-transparent to-transparent"
        aria-hidden="true"
      />

      <div className="mx-auto max-w-3xl text-center">
        {/* Badge */}
        <div className="mb-4 inline-flex items-center rounded-full border border-border bg-muted/50 px-3 py-1 text-xs font-medium text-muted-foreground sm:mb-6 sm:text-sm">
          🎉 Powered by OpenAI GPT-4o-mini-tts
        </div>

        {/* Heading */}
        <h1 className="text-3xl font-bold leading-tight tracking-tight text-foreground sm:text-4xl md:text-5xl lg:text-6xl">
          Turn Text Into{" "}
          <span className="bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            Natural Speech
          </span>
        </h1>

        {/* Description */}
        <p className="mx-auto mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground sm:mt-4 sm:text-base lg:text-lg">
          {siteConfig.description}
        </p>

        {/* Scroll indicator */}
        <p className="mt-6 text-xs text-muted-foreground/60 sm:mt-8">
          ↓ Start generating below
        </p>
      </div>
    </section>
  );
}

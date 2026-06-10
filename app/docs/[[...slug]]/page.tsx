import { findNeighbour } from "fumadocs-core/page-tree";
import { createRelativeLink } from "fumadocs-ui/mdx";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { LLMCopyButton, ViewOptions } from "@/components/ai/page-actions";
import { ScrollArea } from "@/components/ui/scroll-area";
import { getPageImage, source } from "@/lib/source";
import { getMDXComponents } from "@/mdx-components";

export default async function Page(props: PageProps<"/docs/[[...slug]]">) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) {
    notFound();
  }

  const MDX = page.data.body;
  const neighbours = findNeighbour(source.pageTree, page.url);
  const gitConfig = {
    user: "TheOrcDev",
    repo: "scpcn-ui",
    branch: "main",
  };

  return (
    <div className="flex gap-8">
      {/* Main Content */}
      <article className="min-w-0 flex-1">
        <div className="space-y-2">
          <h1 className="scroll-m-20 font-bold text-4xl tracking-tight">
            {page.data.title}
          </h1>
          {page.data.description && (
            <p className="text-lg text-muted-foreground">
              {page.data.description}
            </p>
          )}
        </div>

        <div className="mb-6 flex flex-row items-center gap-2 border-b py-4">
          <LLMCopyButton markdownUrl={`${page.url}.mdx`} />
          <ViewOptions
            githubUrl={`https://github.com/${gitConfig.user}/${gitConfig.repo}/blob/${gitConfig.branch}/content/docs/${page.path}`}
            markdownUrl={`${page.url}.mdx`}
          />
        </div>

        <div className="prose prose-neutral dark:prose-invert max-w-none">
          <MDX
            components={getMDXComponents({
              a: createRelativeLink(source, page),
            })}
          />
        </div>

        {/* Previous/Next Navigation */}
        <div className="mt-12 flex items-center justify-between border-t pt-6">
          {neighbours.previous ? (
            <Link
              className="flex items-center gap-2 text-muted-foreground text-sm hover:text-foreground"
              href={neighbours.previous.url}
            >
              <ChevronLeft className="h-4 w-4" />
              <span>{neighbours.previous.name}</span>
            </Link>
          ) : (
            <div />
          )}
          {neighbours.next && (
            <Link
              className="flex items-center gap-2 text-muted-foreground text-sm hover:text-foreground"
              href={neighbours.next.url}
            >
              <span>{neighbours.next.name}</span>
              <ChevronRight className="h-4 w-4" />
            </Link>
          )}
        </div>
      </article>

      {/* Table of Contents */}
      {page.data.toc && page.data.toc.length > 0 && (
        <aside className="hidden w-64 shrink-0 lg:block">
          <div className="sticky top-20">
            <ScrollArea className="h-[calc(100vh-5rem)]">
              <div className="space-y-2">
                <p className="font-medium text-sm">On This Page</p>
                <ul className="space-y-2 text-sm">
                  {page.data.toc.map((item) => (
                    <li key={item.url}>
                      <a
                        className="text-muted-foreground transition-colors hover:text-foreground"
                        href={item.url}
                        style={{ paddingLeft: `${(item.depth - 2) * 12}px` }}
                      >
                        {item.title}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </ScrollArea>
          </div>
        </aside>
      )}
    </div>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(
  props: PageProps<"/docs/[[...slug]]">
): Promise<Metadata> {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) {
    notFound();
  }

  return {
    title: page.data.title,
    description: page.data.description,
    openGraph: {
      images: getPageImage(page).url,
    },
  };
}

#!/usr/bin/env python3
"""\
A script to download pads from pads.zapf.in that are linked in pages.

Call this e.g. as

    download_pads.py -cat:SoSe23

to download the Markdown files that are in pages that have the category
"SoSe23".

Files will be placed into directories below the output directory (see below)
named by the page title with one file per pad link, named "padname.md".

The following parameters are supported:

-outdir           The directory to put the markdown files in,
                  defaults to "wikipads".

-withcontent      Also download the content of the wikipage that contained
                  a padlink.

-merge            Additionally create a file "merge.wiki" containing the content
                  of the page and opens both this file and the markdown file
                  with an editor. If the merge and content file differ, the
                  content of the merge file will be saved as the new page
                  content. Implies -withcontent.

-always           The bot won't ask for confirmation when putting a page
"""

import filecmp
import os
import re
import shlex
import subprocess
import urllib.parse

import mwparserfromhell
import pywikibot as pwb
import pywikibot.bot
import pywikibot.logging
import pywikibot.pagegenerators
import requests

from pathlib import Path


class PadFinderBot(pwb.bot.ExistingPageBot):
    """Check if a page contains a pad link and download it"""
    available_options = {
        "outdir": Path("wikipads"),
        "withcontent": False,
        "merge": False,
        "always": False,
    }

    padmatcher = re.compile('(?P<padlink>https?://pad\.zapf\.in/(?P<padname>[^/#\?\s]+))')

    def treat_page(self):
        text = self.current_page.text
        parsed = mwparserfromhell.parse(text)
        outdir = self.opt.outdir / self.current_page.title(as_filename=True)
        for link in parsed.filter_external_links():
            if m := self.padmatcher.match(str(link.url)):
                padlink = m.group("padlink")
                padname = m.group("padname")
                padfile = outdir / f"{padname}.md"
                pwb.logging.info(f"Found padlink {padlink}")
                for base in ["https://pads.zapf.in", "https://broken-pads.zapf.in"]:
                    url = urllib.parse.urljoin(base, "/".join([padname, "download"]))
                    r = requests.get(url)
                    if r.ok and r.text:
                        pwb.logging.info(f"Downloading {url}")
                        padcontent = r.text
                        break
                else:
                    pwb.logging.error(f"{padname} had no content on either pads.zapf.in nor broken-pads.zapf.in")
                    continue

                pwb.logging.info(f"Saving {padname} to {padfile}")
                outdir.mkdir(exist_ok=True, parents=True)
                padfile.write_text(padcontent)

        if (self.opt.withcontent or self.opt.merge) and outdir.is_dir():
            contentfile = outdir / "content.wiki"
            pwb.logging.info(f"Saving page content to {contentfile}")
            contentfile.write_text(text)

        editor = os.getenv("VISUAL") or os.getenv("EDITOR")
        if self.opt.merge and editor:
            mergefile = outdir / "merge.wiki"
            mergefile.write_text(text)
            subprocess.run(
                [*shlex.split(editor), os.fspath(mergefile), os.fspath(padfile)]
            )
            if not filecmp.cmp(contentfile, mergefile):
                pwb.logging.info(f"Merge file content differs from current content.")
                newtext = mergefile.read_text()
                summary = pwb.input("Summary", default=f"Merge content from {url.removesuffix('/download')}")
                pwb.logging.info("Saving ")
                self.put_current(newtext, summary=summary)


def main():
    """Parse command line arguments and invoke bot."""
    options = {}
    # Can handle arguments to construct generator that yields pages,
    # e.g. -cat:SoSe23 will yield all pages in category Sose23
    gen_factory = pwb.pagegenerators.GeneratorFactory()
    ## Option parsing
    # global options
    local_args = pwb.handle_args()
    # generators options
    local_args = gen_factory.handle_args(local_args)
    # options for this script
    for arg in local_args:
        arg, _, val = arg.partition(':')
        opt = arg[1:]
        if opt in ("outdir",):
            if not val:
                pywikibot.input(f"Please enter a value for {arg}")
            options[opt] = Path(val)
        elif opt in ("withcontent", "merge", "always"):
            options[opt] = True
    PadFinderBot(generator=gen_factory.getCombinedGenerator(), **options).run()


if __name__ == '__main__':
    main()

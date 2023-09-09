#!/usr/bin/env python3
import re
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
    update_options = {
        "outdir": Path("wikipads")
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
                outfile = outdir / f"{padname}.md"
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

                pwb.logging.info(f"Saving {padname} to {outfile}")
                outdir.mkdir(exist_ok=True, parents=True)
                outfile.write_text(padcontent)


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
            options[opt] = val
    PadFinderBot(generator=gen_factory.getCombinedGenerator(), **options).run()


if __name__ == '__main__':
    main()

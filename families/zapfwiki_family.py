"""
This family file was auto-generated by generate_family_file.py script.

Configuration parameters:
  url = https://zapf.wiki
  name = zapfwiki

Please do not commit this to the Git repository!
"""
from pywikibot import family


class Family(family.Family):  # noqa: D101

    name = 'zapfwiki'
    langs = {
        'de': 'zapf.wiki',
    }

    def scriptpath(self, code):
        return {
            'de': '',
        }[code]

    def protocol(self, code):
        return {
            'de': 'https',
        }[code]
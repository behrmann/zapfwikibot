# ZaPF-Wiki Scripts

Diese Skripte benutzen
[pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot)
([docs](https://doc.wikimedia.org/pywikibot/stable/index.html)) um das
[ZaPFwiki](https://zapf.wiki) zu bearbeiten.

Die eigentlich Skripte sind in `scripts/`. Die notwendigen Dependencies
installiert man am besten in ein virtual environment, diese finden sich in
`requirements.txt`.

Um die Skripte zu benutzen benötigt man ein [families
file](https://www.mediawiki.org/wiki/Manual:Pywikibot/Use_on_third-party_wikis#Script_to_generate_family_file),
welches schon vorgeneriert in `families/zapfwiki_family.py` zu finden ist und
eine `user-config.py`, welche man mit ```sh pwb generate_user_file ``` erzeugen
kann. Dafür empfiehlt es sich vorher ein
[Botpasswort](https://zapf.wiki/Spezial:BotPasswords) anzulegen.

Die Generierung der `user-config.py` muss im Toplevel dieses Repos stattfinden,
damit das families file gefunden wird, dann einfach die Zahl des ZaPFwikis
auswählen, bei der Sprache `de` wählen, den eigenen Nutzernamen eingeben, nicht
mit anderen Projekten verbinden, Ja zum Botpasswort, dann Nutzernamen und
Passwort für den Bot angeben und den Rest kann man getrost verneinen.

## Mehr Skripte schreiben

Beispiele gibt es in `scripts/`, in [der
Doku](https://doc.wikimedia.org/pywikibot/stable/library_usage.html) und in den
[Beispielskripten von
pywikibot](https://doc.wikimedia.org/pywikibot/stable/scripts/index.html).

Skripte benötigen einen Moduldocstring damit Hilfeaufrufe mit `-help` möglich
sind. pywikibot benutzt eine etwas eigene Syntax für
Kommandozeilenargument. Optionen beginnen mit einem Bindestrich gefolgt von
einem Wort, z.B. `-help`, und etwaige Werte werden durch einen Doppelpunkt
getrennt angehängt, z.B. `-option:wert`.

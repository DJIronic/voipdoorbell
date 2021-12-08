# VOIP Doorbell built on RPi Zero with Seeed ReSpeaker
Zdrojové kódy VUT semestrálního projektu VOIP zvonku v rámcí studia na BPC-IBEP.

Projekt zvonku na Rapsberry Pi Zero umožňuje využít SIP operátora ke komunikaci se zvonící osobou. Vlastník má možnost spustit předem definovaný kód při zadání správného kódu pomocí číselné volby během hovoru (DTMF kódy).

Veškerý postup kompilace použitého softwaru PJSIP s knihovnou PJSUA2 a následná instalace je popsána v práci uveřejněné v systému VUT: [link to be added]

# Hardwarové požadavky (použitý HW)

- Raspberry Pi Zero W
- ReSpeaker 2-Mics Pi HAT
- Reproduktor
- SD karta

# Softwarové požadavky
- Raspberry Pi OS (včetně light verze)
- Python 3
- ReSpeaker 2 ovladače
- WPA Supplicant

# Varování:
### Pro správnou funkčnost zde uvedeného kódu přesuňte obsah složky ```pjsip-files``` do root adresáře projektu.

Obsah byl umístěn do jiné složky z licenční důvodů zmíněných níže.




## Licence
Soubory uložené ve složce pjsip-folder jsou licencovány pod licencí GNU General Public License v3.0. 

Ostatní, mnou vytvořené soubory v repozitáři spadají pod licenci MIT.

# VOIP Doorbell built on RPi Zero with Seeed ReSpeaker
Zdrojové kódy VUT bakalářské práce VOIP zvonku v rámcí studia na BPC-IBEP.

Projekt zvonku na Rapsberry Pi Zero umožňuje využít SIP operátora ke komunikaci se zvonící osobou. Vlastník má možnost spustit předem definovaný kód při zadání správného kódu pomocí číselné volby během hovoru (DTMF kódy). Pro demonstraci je po zadání správného kódu skrze GPIO piny spuštěno relé.

Zařízení zároveň využívá kameru (Pi Camera) pro soustavný stream video do lokální sítě skrze HTTP (JPEG stream).

Veškerý postup kompilace použitého softwaru PJSIP s knihovnou PJSUA2 a následná instalace je popsána v práci uveřejněné v systému VUT: [link to be added]

Výsledné zařízení bylo umístěno do 3D tisknutelného boxu, který je součástí tohoto repozitáře jako Autodesk Fusion 360 projekt. (Tisk proveden materiálem PLA)

# Hardwarové požadavky (použitý HW)

- Raspberry Pi Zero 2W
- ReSpeaker 2-Mics Pi HAT
- Pi Camera
- Tlačítko
- Relé
- Reproduktor
- SD karta

# Softwarové požadavky
- Raspberry Pi OS Buster (včetně light verze) *POZOR, nejnovější verze Raspberry Pi OS neobsahuje podporu pro ReSpeaker 2-Mics Pi HAT*
- Python 3
- ReSpeaker 2 ovladače
- WPA Supplicant

# Konfigurační soubory
- soubor motion.conf slouží pro konfiguraci streamu z kamery skrze software Motion (http://motion-project.github.io/)
- soubor wpa_supplicant.conf slouží pro konfiguraci připojení k WiFi síti
- doorbell.cfg slouží pro konfiguraci SIP účtu a číselného kódu pro spuštění relé
- .asoundrc slouží pro konfiguraci ALSA zvukového systému pro správnou funkci ReSpeaker 2-Mics Pi HAT na Raspberry Pi Zero 2W (a má byt umístěn v domovském adresáři uživatele pi)



## Licence
Celá práce je licencována pod GNU General Public License v3.0. 



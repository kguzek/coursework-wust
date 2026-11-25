# Lab 8 (Cyberbezpieczeństwo) — MitM / ARP + DNS spoofing — Handoff

## Cel laboratorium
Atak Man-in-the-Middle. **Kali = atakujący, Ubuntu = ofiara**, obie VM na tej samej
sieci L2 (UTM Shared Network). Dwa zadania + 4 pytania teoretyczne.

- **Zadanie 1:** ARP poisoning + DNS spoofing — przekierowanie `pwr.edu.pl` ofiary na
  Apache atakującego (fałszywa strona).
- **Zadanie 2:** ARP poisoning tylko ofiary → logowanie na
  `http://demo.testfire.net/login.jsp` (czysty HTTP) → przechwycenie danych logowania
  w Ettercap + Wireshark.
- **Pytania (str. 2 PDF):** różnica aktywny/pasywny MitM; obrona przed ARP poisoning;
  po co DNSSEC; co to tryb monitorowania.
- PDF: `lab08/8_Cyber_PL_Lab_Ataki_na_komunikację.pdf`.
  **Wybrano tryb GUI `ettercap -G`** (nie tekstowy).

## Środowisko (UTM, Apple Silicon, aarch64)

| | Kali (atakujący) | Ubuntu (ofiara) |
|---|---|---|
| IP | `192.168.64.4` / eth0 | `192.168.64.5` / enp0s1 |
| Brama/DNS | `192.168.64.1` | `192.168.64.1` |
| User desktopu | `konrad` (uid 1000), XFCE/**Xorg** `:0` | `konrad` (uid 1000), GNOME **Wayland** |
| Dostępność | ✅ oba pingują się nawzajem i bramę | |

- UTM MCP (`.mcp.json`, serwer `utm`) steruje obiema VM. Nazwy: `"Kali Linux"`, `"Ubuntu"`.
- `qemu-guest-agent` zainstalowany na Ubuntu (świeży desktop go nie miał — zrobione).
- DNS bazowy (przed atakiem): `pwr.edu.pl → 156.17.75.200` (do kontrastu w raporcie).

## Co JUŻ zrobione na Kali (gotowe do ataku)
- ✅ Narzędzia obecne: ettercap 0.8.4.1, dsniff/arpspoof, tshark/wireshark, apache2,
  xdotool, xfce4-screenshooter, ImageMagick. `konrad` jest w grupie `wireshark`.
- ✅ `/etc/ettercap/etter.dns` — backup `etter.dns.bak`, dopisany blok
  `## LAB8 SPOOF START/END`:
  ```
  pwr.edu.pl      A   192.168.64.4
  *.pwr.edu.pl    A   192.168.64.4
  www.pwr.edu.pl  PTR 192.168.64.4
  ```
- ✅ Apache serwuje fałszywą stronę „Politechnika Wrocławska / strona przejęta”
  (`/var/www/html/index.html`), zweryfikowane lokalnie. `ip_forward=1`.
- ✅ Plugin `dns_spoof` dostępny.
- ✅ Skrypt ataku **tekstowego** (fallback) `/tmp/lab8_attack.sh` na Kali: tryby
  `dns|creds|stop`, parametr `<VICTIM_IP>` = `192.168.64.5`. Loguje do `/tmp/lab8/`,
  robi pcap przez tshark. `ettercap -T`. **Działa niezależnie od GUI.**
- ✅ Helper screenshotów `/usr/local/bin/kshot <nazwa>` — zrzut `:0`, skaluje do JPG,
  zapisuje `.b64` w `/tmp/shots/`.
- ⚠️ **`ettercap -G` AKTUALNIE DZIAŁA** jako transient unit `ettlab8` (uruchomione przez
  `systemd-run`, pid był 50122). Żaden atak NIE wystartowany — tylko otwarte GUI.
  Tablice ARP **nietknięte**. Zatrzymanie: `systemctl stop ettlab8` lub `pkill -x ettercap`.

## Stan repo
- `lab08/screenshots/` i `lab08/texts/` utworzone (puste).
- Wzór raportu: `lab06/notes.md` (styl: nagłówek „Cyberbezpieczeństwo laboratorium”,
  data, „Konrad Guzek grupa 8”, sekcje, tabele, screeny, „Wnioski”).
  Render: `uv run render_pdf.py 8` z katalogu `cyber/`.
- **Pamięć (feedback usera):** notatki mają opisywać setup jak w zadaniu (Ubuntu
  „ofiara” itp.), **bez** wzmianek o obejściach/dziwactwach narzędzi. Obejścia tylko
  w czacie, nie w notes.md.

## ⛔ GŁÓWNY BLOKER — screenshoty GUI są czarne
Zrzuty ekranu Kali wychodzą **całkowicie czarne** (root window = obraz 2-kolorowy,
302 B), mimo że ettercap i cały XFCE działają (okna widoczne w `xdotool`/`wmctrl -l`).
Przyczyna: UTM/virtio-GPU prawdopodobnie **nie renderuje framebufora do odczytu, dopóki
okno danej VM nie jest aktywnie wyświetlane na hoście Mac**. Wyłączenie wygaszacza
(`xfce4-screensaver`) + `xset dpms force on` **nie pomogło**.
**Następny krok (testowany w momencie STOP):** poprosić usera, by uczynił okno Kali
widocznym/aktywnym w UTM na Macu, i ponowić `kshot`. Jeśli to nie pomoże → user sam robi
zrzuty ekranu ettercapa, a agent prowadzi/weryfikuje atak.

## Krytyczne gotchy UTM MCP (oszczędzą dużo czasu)
1. **`utm_exec_command` jest ASYNCHRONICZNE i NIE zwraca stdout.** Zawsze: przekieruj do
   pliku (`> /tmp/x.txt 2>&1`), potem `utm_file_pull` ścieżkę. Po komendzie ze
   `sleep`/pętlą plik bywa pusty przy pierwszym pull — pull ponownie (albo dopisz marker
   `DONE` na końcu i odpytuj).
2. **`pkill -f ettercap` POPEŁNIA SAMOBÓJSTWO** — command line powłoki
   `bash -c '...ettercap...'` sam zawiera słowo „ettercap”, więc `pkill -f` ubija własny
   shell → komenda „nic nie robi”. Używaj `pkill -x ettercap` (exact comm).
3. **Backgrounding (`&`, `nohup`, `setsid`) w guest-exec NIE przeżywa** powrotu z exec —
   proces jest zabijany. Trwałe procesy GUI uruchamiaj przez
   **`systemd-run --no-block --unit=NAZWA --setenv=DISPLAY=:0 --setenv=XAUTHORITY=/home/konrad/.Xauthority /usr/bin/...`**.
4. **GUI jako root na `:0`:** root ma dostęp do X przez
   `XAUTHORITY=/home/konrad/.Xauthority` (bez `xhost`). ettercap musi być rootem
   (raw sockets/ARP).
5. **Zrzuty binarne:** NIE rób `utm_file_pull` na PNG (zalewa kontekst). Zawsze base64 +
   downscale na gościu (robi to `kshot`), pull `.b64`, dekoduj lokalnie, czytaj jako obraz.
6. **Prawa zapisu:** `xfce4-screenshooter` uruchamiany jako `konrad` nie zapisze do
   katalogu root-owned — `kshot` pisze PNG do `/tmp` i `chmod 777 /tmp/shots`.
7. Sporadyczny błąd AppleEvents `OSStatus -10004` (jak -1743 w pamięci) — po prostu ponów
   wywołanie.
8. Ubuntu: GNOME **Wayland** blokuje skryptowe zrzuty (`org.gnome.Shell.Screenshot` →
   „not allowed”), a snap Firefox `--headless --screenshot` **wiesza się**. Dowód ataku
   po stronie ofiary rób tekstowo: `getent hosts pwr.edu.pl` + `curl -v http://pwr.edu.pl/`.
   Wizualny screen przeglądarki ofiary musi zrobić **user ręcznie**
   (PrtSc → `~/Pictures/Screenshots`).

## Pozostało do zrobienia
1. Rozwiązać blokadę czarnego ekranu (patrz wyżej) **albo** przełączyć się: user robi
   zrzuty ettercapa, agent prowadzi atak.
2. **Zad. 1:** w ettercap -G: wybór interfejsu eth0 → Hosts → Scan for hosts →
   Hosts List → brama (`.1`) do Target1, Ubuntu (`.5`) do Target2 → MITM → ARP poisoning
   (zaznacz „Sniff remote connections”) → Plugins → dns_spoof. Na Ubuntu otworzyć
   `pwr.edu.pl` w Firefoksie → zrzut przejętej strony + `getent`/`curl` jako dowód.
   (Fallback bez GUI: `sudo /tmp/lab8_attack.sh dns 192.168.64.5`.)
3. **Zad. 2:** stop MitM → Target1 = Ubuntu `.5`, Target2 pusty → ARP poisoning → na
   Ubuntu logowanie na `http://demo.testfire.net/login.jsp` (dowolny login/hasło) →
   podejrzeć USER/PASS w ettercap; potem Wireshark/tshark na eth0, wygenerować ruch,
   pokazać przechwycony POST. (Fallback: `sudo /tmp/lab8_attack.sh creds 192.168.64.5`.)
4. **Sprzątanie (WAŻNE):** `sudo /tmp/lab8_attack.sh stop` i/lub stop ettercap — ettercap
   przy czystym wyjściu przywraca tablice ARP ofiary. Potwierdzić.
5. Napisać `lab08/notes.md` w stylu lab06 (treść PO POLSKU, + odpowiedzi na 4 pytania),
   wrzucić screeny do `lab08/screenshots/`, wyrenderować `uv run render_pdf.py 8`.

Nic do zainstalowania — wszystkie narzędzia są. `ettercap -G` zostawione uruchomione
(unit `ettlab8`). Jeśli drugi agent ma zacząć od czysta: `systemctl stop ettlab8`.

# jaldh
just-another-little-documentation-helper
# jaldh - Just Another Little Doc Helper

**jaldh** ist ein kleines Kommandozeilen-Tool, das automatisch minimale Dokumentations-Header für Python-, C- und C++-Quellcode-Dateien erzeugt. Ziel ist es, Entwicklern eine Vorlage zu liefern, die sie schnell und einfach ausfüllen können, ohne die Motivation durch überflüssige Kommentare zu verlieren.

Generiert am 22.06.2025 von Peter Jacobi

Version: 0.1.0 Beta

---

## Merkmale

* Generiert **Datei-Header** mit Modulname, Autor und Beschreibung
* Fügt **Funktions-Kommentare** ein (inkl. Parameter und Rückgabewert)
* Erkennt C++-**Klassen** in Header-Dateien und ergänzt bei Bedarf einen Überblick
* Unterstützt folgende Dateitypen: `.py`, `.c`, `.h`, `.cpp`, `.hpp`, `.cc`
* Optional rekursiver Modus
* Dokumentationsextraktion über `--doc`

---

## Installation

```bash
# Klone das Repository
$ git clone https://github.com/dein-name/jaldh.git
$ cd jaldh

# Starte jaldh direkt
$ python jaldh.py -h
```

---

## Beispielverwendung

### 🔧 Quellcode automatisch mit Header versehen:

```bash
# Einzelne Datei (automatische Spracherkennung)
$ python jaldh.py -s main.c

# Alle unterstützten Dateien im aktuellen Verzeichnis
$ python jaldh.py -a

# Rekursiv alle Dateien in Unterverzeichnissen
$ python jaldh.py -r
```

### 📝 Ausgabe in neue Dateien schreiben (nicht überschreiben):

```bash
$ python jaldh.py -a -o new_
```

### 📄 Dokumentation extrahieren

```bash
$ python jaldh.py -a --doc projekt_doku.txt
```

---

## Konfiguration

Beim ersten Start wird automatisch eine `config.yaml` erstellt:

```yaml
language: auto
file_separator: "------------------------------"
function_separator: "------------------------------"
header:
  author: Your Name
  include_date: true
  date_format: "%Y-%m-%d"
```

Diese Datei kann manuell angepasst werden.

---

## Beispiel für generierten Kommentar (C-Funktion)

```c
/*------------------------------
my_function - <Describe what this function does>

Parameters:
    param1 - <description>

Returns:
    int - <description>
------------------------------*/
int my_function(int param1) {
    ...
}
```

## Beispiel für Python-Funktion

```python
    """------------------------------
    Description: <Describe what do_thing does>

    Parameters:
        arg1: <description>

    Returns:
        <description>
    ------------------------------"""
    def do_thing(arg1):
        ...
```

---

## Lizenz

Opensource

---

## Autor: Peter Jacobi

Dieses Tool wurde inspiriert und konzipiert von einem Entwickler, der pragmatische Dokumentation vor keiner Dokumentation für eine bessere Codebasis bevorzugt. ❤️

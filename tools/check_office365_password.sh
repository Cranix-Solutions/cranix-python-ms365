#!/usr/bin/env bash
# Prüfung eines Passworts gegen typische Office 365 Richtlinien

# Konfiguration (anpassen nach Bedarf)
MIN_LEN=12
MAX_LEN=64
REQUIRE_UPPER=1
REQUIRE_LOWER=1
REQUIRE_DIGIT=1
REQUIRE_SPECIAL=1
# Einschränkung für Wiederholungen (z.B. keine 3 gleichen hintereinander)
MAX_REPEAT_SEQ=2
# Blacklist-Datei (eine Zeile = ein Passwort, leerzeilen ignorieren)
BLACKLIST_FILE="./common_passwords.txt"

# Hilfsfunktionen
print_ok() { echo -e "\e[32mOK\e[0m"; }
print_fail() { echo -e "\e[31mFAIL\e[0m"; }

check_length() {
  local pw="$1"
  local len="${#pw}"
  if (( len < MIN_LEN )); then
    echo "Zu kurz: $len Zeichen (Minimum $MIN_LEN)"
    return 1
  fi
  if (( MAX_LEN > 0 && len > MAX_LEN )); then
    echo "Zu lang: $len Zeichen (Maximum $MAX_LEN)"
    return 1
  fi
  return 0
}

check_char_classes() {
  local pw="$1"
  local ok=0
  if (( REQUIRE_UPPER )); then
    if [[ "$pw" =~ [A-Z] ]]; then
      ok=$((ok+1))
    else
      echo "Fehlt Großbuchstabe"
      ok=2
    fi
  fi
  if (( REQUIRE_LOWER )); then
    if [[ "$pw" =~ [a-z] ]]; then
      ok=$((ok+1))
    else
      echo "Fehlt Kleinbuchstabe"
      ok=2
    fi
  fi
  if (( REQUIRE_DIGIT )); then
    if [[ "$pw" =~ [0-9] ]]; then
      ok=$((ok+1))
    else
      echo "Fehlt Ziffer"
      ok=2
    fi
  fi
  if (( REQUIRE_SPECIAL )); then
    if [[ "$pw" =~ [^A-Za-z0-9] ]]; then
      ok=$((ok+1))
    else
      echo "Fehlt Sonderzeichen"
      ok=2
    fi
  fi
  if (( ok >= 1 )); then
    return 0
  else
    return 1
  fi
}

check_repeats() {
  local pw="$1"
  if [[ "$pw" =~ (.)\1\1 ]]; then
    echo "Enthält drei aufeinanderfolgende gleiche Zeichen"
    return 1
  fi
  return 0
}

check_blacklist() {
  local pw="$1"
  if [[ -f "$BLACKLIST_FILE" ]]; then
    if grep -Fxq "$pw" "$BLACKLIST_FILE"; then
      echo "Passwort kommt in der Blacklist vor"
      return 1
    fi
  fi
  return 0
}

# Hauptlogik
read -rsp "Passwort eingeben (Inhalt wird versteckt eingegeben): " PASSWD

ok=0
err=0

# Länge prüfen
if ! check_length "$PASSWD"; then
  err=$((err+1))
fi

# Zeichengruppen prüfen
if ! check_char_classes "$PASSWD"; then
  err=$((err+1))
fi

# Wiederholungen prüfen
if ! check_repeats "$PASSWD"; then
  err=$((err+1))
fi

# Blacklist prüfen
if ! check_blacklist "$PASSWD"; then
  err=$((err+1))
fi

if (( err == 0 )); then
  exit 0
else
  exit 1
fi

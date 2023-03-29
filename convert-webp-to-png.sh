#!/bin/bash

# Vérifie si le nombre d'arguments est correct
if [ $# -ne 2 ]; then
  echo "Usage: $0 input_url output_file"
  exit 1
fi

# Vérifie si l'outil de conversion dwebp est installé
if ! [ -x "$(command -v dwebp)" ]; then
  echo "Error: dwebp is not installed. Please install the WebP library." >&2
  exit 1
fi

# Télécharge l'image à partir de l'URL spécifiée
curl -s "$1" > /tmp/input.webp

# Exécute la commande de conversion
dwebp /tmp/input.webp -quiet -o "$2"

# Supprime le fichier temporaire
rm /tmp/input.webp

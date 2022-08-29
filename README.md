# Efrei Menu

![menu](https://media.discordapp.net/attachments/972604017261830176/1012347118847016970/unknown.png)

Un menu permettant d'accéder rapidement aux différents services de l'Efrei.

## Utilisation

⚠️ Pour utiliser ce programme, vous devez télécharger le driver de Firefox [(geckodriver)](https://github.com/mozilla/geckodriver/releases) ou celui de Chrome [(chromedriver)](https://sites.google.com/chromium.org/driver/) et les navigateurs correspondants.

Pour choisir votre navigateur, changez la valeur de la variable `browser` dans le fichier `variables.json` (Firefox/Chrome).

[Installation du driver Firefox sur windows](https://stackoverflow.com/questions/42524114/how-to-install-geckodriver-on-a-windows-system)
[Installation du driver Chrome sur windows](https://chromedriver.chromium.org/getting-started)

OU

Lancez `install_driver_chrome.ps1` ou `install_driver_firefox.ps1`.

Installation du driver Firefox sur Mac : `λ brew install geckodriver`

Installation du driver Chrome sur Mac : `λ brew install chromedriver`

Je suppose que les utilisateurs de Linux savent faire leurs propres recherches. 👀

```bash
λ cp variables.json.template variables.json
λ pip install -r requirements.txt
λ python3 menu.py
```

### Précisions sur "Actualiser mes identifiants"

Pour que les appels API soient valides, il faut récupérer un cookie de session temporaire. Pour ce faire, le programme va vous demander de vous connecter sur le site web de l'Efrei. Par défaut, une page s'ouvre et vous devez vous connecter manuellement. Mais si vous le souhaitez, vous pouvez enregistrer vos identifiants pour que le programme se connecte automatiquement.

## TODO

- [x] Voir les matières de chaque semestre
- [x] Voir ses notes pour chaque semestre
- [x] Possibilité de changer de semestre
- [x] Possibilité de récupérer le cookie de session automatiquement
- [x] Voir son emploi du temps de la semaine
- [x] Générer un tableau excel de ses notes
- [ ] Voir son emploi du temps du jour

N'hésitez pas à rédiger une issue si vous avez des questions ou des suggestions.

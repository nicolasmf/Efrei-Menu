# Efrei Menu

![menu](https://media.discordapp.net/attachments/972604017261830176/1012347118847016970/unknown.png)

Un menu permettant d'accéder rapidement aux différents services de l'Efrei.

## Utilisation

```bash
λ pip install -r requirements.txt
λ python3 menu.py
```

⚠️ Ce programme utilise selenium pour Firefox. Il faut donc que Firefox soit installé sur votre ordinateur et que son [driver](https://github.com/mozilla/geckodriver/releases) soit téléchargé.

[Installation du driver sur windows](https://stackoverflow.com/questions/42524114/how-to-install-geckodriver-on-a-windows-system)

### Précisions sur "Actualiser mes identifiants"

Pour que les appels API soient valides, il faut récupérer un cookie de session temporaire. Pour ce faire, le programme va vous demander de vous connecter sur le site web de l'Efrei. Par défaut, une page s'ouvre et vous devez vous connecter manuellement. Mais si vous le souhaitez, vous pouvez enregistrer vos identifiants pour que le programme se connecte automatiquement.

## TODO

- [x] Voir les matières de chaque semestre
- [x] Voir ses notes pour chaque semestre
- [x] Possibilité de changer de semestre
- [x] Possibilité de récupérer le cookie de session automatiquement
- [x] Voir son emploi du temps de la semaine
- [ ] Voir son emploi du temps du jour
- [x] Générer un tableau excel de ses notes

N'hésitez pas à rédiger une issue si vous avez des questions ou des suggestions.

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Zh-HM8QW)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19858700&assignment_repo_type=AssignmentRepo)
# 🎓 Projet de Fin d’Année –  Développement d’un système de détection des micro-organismes à partir d’un prélèvement sanguin grâce au deep learning et analyse des résultats

> **Département** : [ Intelligence Artificielle]  
> **Filière** : [ Data Science ] 
> **Année académique** : 2024–2025  
> **Encadrant** :  La Commission

---

## 📌 Objectif du projet

Ce projet a pour objectif de **concevoir et développer MediScan AI**, un système intelligent basé sur le deep learning permettant d’analyser les images de frottis sanguins pour :

1. **Confirmer la validité d’un frottis sanguin** (filtrage automatique des images valides/non valides).  
2. **Détecter la présence ou non du paludisme** et déterminer la classe (infecté ou non infecté) avec un **pourcentage d’assurance**.  
3. Fournir une **interprétation médicale automatique** des résultats via l’intégration de ChatGPT pour générer un rapport interprétatif et des recommandations.


---

## 🛠️ Technologies utilisées

- Langage principal : `Python`
- Frameworks : `TensorFlow / Keras` (deep learning), `Django` (backend web)
- Base de données : `MongoDb` (dev) / possibilité `PostgreSQL` (prod)
- Outils : `GitHub`, `VSCode`

---


## 🚀 Etapes pour lancer le projet

⚠️ A compléter obligatoirement. Exemple : 

1. Cloner ce dépôt :

```bash
   git clone https://github.com/criagi-upc/projet-final-l3-Jenovickbg.git
   cd nom-du-repo
````

2. Créer un environnement virtuel (si Python) :

```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```
4. Lancer le serveur :

   ```bash
   python manage.py runserver
   ```

---

## 📁 Structure du projet

`📦 mediscan-ai
 ┣ 📂 ml_model/                # Modèles entraînés (.keras)
 ┣ 📂 diagnostics/            # Application Django (vues, forms, urls)
 ┣ 📂 static/                 # Fichiers CSS, JS, images statiques
 ┣ 📂 templates/              # Templates HTML
 ┣ 📄 manage.py               # Commande principale Django
 ┣ 📄 requirements.txt        # Dépendances Python
 ┣ 📄 README.md               # Présentation du projet
 ┗ 📄 .gitignore              # Fichier gitignore
```

---



## 🎥 Démonstration

Lien vers la démonstration vidéo :
👉 [https://youtu.be/votre-video-demo](https://youtu.be/votre-video-demo)



---



## 🔁 Vous avez déjà commencé votre projet ailleurs ?

Si vous avez déjà un projet sur GitHub (dans votre compte personnel), vous n’avez pas besoin de le recommencer.
Vous pouvez continuer à travailler dessus et simplement pousser le même code vers le dépôt de CRIAGI.

Pas de panique ! Voici comment transférer votre code existant dans ce dépôt :

### ✅ Étapes à suivre (une seule fois)

1. 📥 **Acceptez l’invitation GitHub Classroom**
   Exemple :
   `https://classroom.github.com/a/xxxxxxxx`
   → Un dépôt sera automatiquement créé pour vous dans l’organisation de CRIAGI (ex: `https://github.com/criagi-upc/projet-final-etudiant.git`)

2. 🔗 **Copiez le lien du dépôt Classroom généré**

   * Cliquez sur le bouton **“Code”** dans GitHub
   * Copiez l’URL HTTPS du dépôt créé (ex: `https://github.com/criagi-upc/projet-final-etudiant.git`)

3. 🧠 **Dans votre projet existant (sur votre machine)**
   Ouvrez un terminal et placez-vous dans le dossier :

   ```bash
   cd mon-projet
   ```

4. ➕ **Ajoutez le dépôt de CRIAGI comme destination secondaire (remote)**

   ```bash
   git remote add criagi https://github.com/criagi-upc/projet-final-etudiant.git
   git fetch criagi
   git merge criagi/main --allow-unrelated-histories
   ```

---

### 🚀 Pour soumettre votre projet

À chaque fois que vous souhaitez soumettre votre travail à l’université :

```bash
git push criagi main
```

Et pour continuer à sauvegarder sur votre dépôt personnel habituel :

```bash
git push origin main
```

---



### ⚠️ Une autre étape à suivre (une seule fois) — Cette étape est optionnelle mais récommandée

5. **Créez un remote "both" pour tout pousser d’un coup**

Cette étape permet de **pousser automatiquement votre code vers votre dépôt personnel *et* le dépôt CRIAGI** en une seule commande.

Dans votre terminal, toujours dans le dossier du projet :

```bash
git remote add both https://github.com/votre-utilisateur/mon-projet.git
git remote set-url --add both https://github.com/criagi-upc/projet-final-etudiant.git
```

✅ Vous pouvez maintenant soumettre votre travail aux **deux dépôts en même temps** avec :

```bash
git push both main
```


---

### Résumé des commandes possibles

| Commande               | Effet                                                   |
| ---------------------- | ------------------------------------------------------- |
| `git push origin main` | 🔐 Sauvegarde dans votre dépôt personnel                |
| `git push criagi main` | 🎓 Soumission officielle à CRIAGI                       |
| `git push both main`   | ✅ Soumet dans les **deux dépôts** en une seule commande |


--- 


### Conditions 

Pour que votre projet soit pris en compte, **merci de suivre scrupuleusement toutes les étapes décrites dans ce README**.

* Assurez-vous d’avoir accepté l’invitation GitHub Classroom avant de commencer.
* Copiez et ajoutez correctement le dépôt CRIAGI comme remote secondaire (`criagi` ou `both`).
* Poussez votre code dans le dépôt CRIAGI **avant la date limite**.
* Vérifiez que vos dernières modifications sont bien visibles sur GitHub.
* Tout dépôt non soumis conformément à ces consignes ne sera pas pris en compte.

En cas de difficulté, contactez votre la COMMISSION **avant la deadline**.


---


## 💡 Comprendre Git et GitHub

Cette vidéo vous explique les bases de Git et GitHub : création de dépôt, commits, push/pull, branches, etc.  
Utile pour bien démarrer avec le versioning collaboratif.

👉 [Regarder la vidéo sur YouTube](https://www.youtube.com/watch?v=V6Zo68uQPqE)

---
## 📄 Licence

Projet académique – Usage Strictement Pédagogique.
© 2025 – Université Protestante au Congo - CRIAGI


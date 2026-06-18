# Jeu d'échecs 3D ( vue isométrique )

## Présentation :

    Voici mon projet de code en python d'implémentation d'un jeu d'échecs à deux joueurs en affichage isométrique. Il est possible de jouer complètement en local en suivant toutes les règles du jeu. 
    Enfin, j'ai suivi une approche de dévelopement orienté objet, en séparant donc la logique métier du moteur de jeu et de la partie affiche graphique. 

## Fonctionnalités incluses :

    - partie à 2 joueurs en local
    - gestion des tours de jeu
    - affichage des coups autorisés lors de la sélection d'une pièce
    - sauvegarde et chargement d'une partie (.json)
    - conservation de l'historique de la partie

## Architecture

Ce projet suit une architecture inspirée du modèle MVC (Model – View – Controller).

### Modèle :

Le modèle contient l'ensemble de la logique métier :

* `Game`
* `Board`
* `Piece`
* `Pawn`
* `Knight`
* `Bishop`
* `Tower`
* `Queen`
* `King`

Le modèle gère :

* les déplacements ;
* les captures ;
* les règles spéciales ;
* l'état de la partie ;
* la détection des situations d'échec.

### Vue :

J'ai choisi d'utiliser la bibliothèque pygame, car c'est celle avec laquelle je suis la plus familière.
Je m'en sers pour :

* l'affichage du plateau ;
* l'affichage des pièces ;
* l'affichage du joueur courant ;
* l'affichage des états de la partie (echec, nul, ...) ;

### Contrôleur :

La classe `GameManager` joue le rôle de contrôleur.

Elle assure :

* la gestion des événements utilisateur ;
* la sélection des pièces ;
* l'exécution des déplacements ;
* la sauvegarde et le chargement.


## Sauvegarde et chargement :

Les parties sont enregistrées au format JSON.

Les informations sauvegardées comprennent :

* le joueur dont c'est le tour ;
* la position des pièces ;
* leur couleur ;
* leur état de déplacement (`has_moved`).

Le fichier de sauvegarde par défaut est :

save.json

Pour l'instant, pour sauver il faut presser `s` (pour `save`) durant une partie, ce qui crée un fichier json de la partie à ce moment. Cela écrase donc un possible fichier déjà existant. Pour la charger ensuite, il faut presser `l` (pour `load`) ce qui reprend la partie à l'état de la sauvegarde. 

## Installation

### Prérequis

* Python 3.10 ou supérieur
* Pygame

### Installation

* Cloner le dépôt :
* Accéder au dossier :

-> `cd projet-echecs`

* Installer les dépendances :

-> `pip install pygame`


### Exécution

* Lancer l'application :

-> `python game_manager.py`


## Contrôles

### Souris

* Clic sur une pièce : sélection.
* Clic sur une case valide : déplacement.

### Clavier

* Touche S : sauvegarder la partie.
* Touche L : charger une partie.


L'objectif de ce projet est de concevoir et développer, en Python, un jeu d'échecs en vue 3D isométrique (pseudo-3D).

## Objectif du projet

Le projet doit aboutir à une application jouable, structurée proprement sur le plan logiciel, et, développée avec une démarche d'ingénierie cohérente.

L'accent est mis à la fois sur :
- la qualité de conception ;
- la séparation entre logique métier et interface ;
- la progression incrémentale du développement ;
- la validation du comportement du moteur de jeu.

## Fonctionnalités minimales (MVP obligatoire)

Votre application doit permettre, au minimum :
- de jouer une partie d'échecs à deux joueurs, en local et au tour par tour ;
- de sauvegarder une partie en cours, puis de la recharger ;
- d'afficher les coups autorisés lorsqu'une pièce est sélectionnée.

## Fonctionnalités complémentaires

Si l'avancement du projet le permet, vous pourrez proposer une ou plusieurs extensions, par exemple :
- un mode de jeu à distance, par échange différé (email) ou via un serveur ;
- une intelligence artificielle permettant d'affronter un joueur virtuel ;
- un mode d'observation dans lequel deux joueurs virtuels s'affrontent.

Ces fonctionnalités sont facultatives. Elles ne doivent pas se faire au détriment de la solidité du socle minimal.

## Contraintes techniques

Le projet doit être réalisé en Python 3, dans une approche orientée objet.

Une séparation claire est attendue entre :
- le moteur de jeu, qui porte la logique métier ;
- l'interface utilisateur, qui gère l'affichage et les interactions.

Vous êtes libres de choisir les bibliothèques nécessaires à l'implémentation, par exemple `pyglet`, `arcade` ou `pygame-ce`.

Dans le cadre du rendu isométrique, vous pourrez vous appuyer sur l'algorithme du peintre afin de gérer correctement l'ordre d'affichage des éléments de la scène. Cette approche consiste à dessiner d'abord les éléments les plus éloignés, puis les éléments les plus proches, de manière à produire une impression de profondeur cohérente sans recourir à un moteur 3D complet. Une réflexion explicite sur cet ordonnancement du rendu est attendue.

## Architecture attendue

Vous proposerez une architecture lisible, inspirée du modèle MVC :
- un modèle regroupant notamment le plateau, les pièces, l'état de la partie et l'historique ;
- une ou plusieurs vues pour l'affichage ;
- un ou plusieurs contrôleurs orchestrant les actions utilisateur et le déroulement de la partie.

L'usage de patrons de conception pertinents, comme Observateur (ou un mécanisme équivalent), est encouragé lorsque cela améliore la clarté et la maintenabilité.

## Démarche de développement

Le projet devra être mené de manière incrémentale. Il est attendu que vous construisiez d'abord un noyau fonctionnel minimal, puis, que vous l'enrichissiez progressivement.

Votre démarche devra être structurée et explicite, particulièrement sur les points suivants :
- planification des itérations ;
- priorisation des fonctionnalités ;
- stratégie de test ;
- documentation d'installation et d'exécution.

## Qualité logicielle et tests

Vous écrirez des tests unitaires ciblant le moteur de jeu, indépendamment de l'interface graphique. Ces tests devront surtout permettre de valider les règles de déplacement, de capture et, plus généralement, les mécanismes centraux du jeu.

Si le temps le permet, vous pourrez compléter cette base par des tests de plus haut niveau, par exemple des tests de bout en bout.

Lorsque cela est pertinent, vous mettrez en place des outils de qualité de code, tels qu'un linter et un formateur automatique.

## Gestion de versions

Le développement devra être versionné avec Git et hébergé sur GitLab : https://gibson.telecomnancy.univ-lorraine.fr/

Une utilisation régulière et rigoureuse du gestionnaire de versions est attendue tout au long du projet.

## Usage des assistants d'IA

L'usage d'assistants d'IA de programmation est autorisé, à condition d'en faire un usage critique et maîtrisé.

Dans ce cas, vous tiendrez un journal d'usage nommé `IA_USAGE.md`, dans lequel vous décrirez quelques cas représentatifs :
- le contexte ;
- le prompt ;
- la réponse produite ;
- ce qui a été conservé, modifié ou rejeté ;
- la justification de ces choix.

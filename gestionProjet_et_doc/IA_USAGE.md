# Utilisation faite de l'IA :

### Utilisation 1 :
- contexte : au tout début du projet, j'ai copier-coller l'entièreté de mon travail avec le sujet en lui demandant d'évaluer l'état actuel par rapport aux attendus. Le but était surtout d'avoir un avis sur mon code actuel (qui n'avait pas été codé dans un contexte de MVP). J'espérais donc obtenir, de 1. des corrections d'erreurs qui auraient pu rester, et de 2. un plan ou une idée de ce que je devais faire pour le convertir selon les attendus du sujet.
- prompt :
```
Voici le sujet:
[copie du sujet de la coding week]
et voici mon travail
[copie de mon fichier de travail initial]
```
- la réponse :
```
Tu as déjà implémenté une bonne partie du moteur d'échecs : déplacements des pièces, captures, échec, échec et mat, promotion. Pour un projet universitaire comme celui-ci, je te conseillerais maintenant de te concentrer davantage sur l'architecture que sur l'ajout de règles, parce que c'est justement ce qui est évalué dans le sujet.

Ce qui est bien dans ton code

✅ Les mouvements sont séparés par pièce.

✅ Tu as déjà une classe Game.

✅ Tu as commencé à gérer :

l'échec ;
l'échec et mat ;
la promotion ;
les captures.

✅ La logique métier est indépendante de l'affichage terminal.
```

Les principaux problèmes actuels
### 1. Les pièces sont des variables globales
```
par exemple
[...]
les deux parties partageront les mêmes objets.

C'est une très mauvaise pratique.

Il faudrait créer les pièces dans le constructeur du jeu :
```

### 2. Le nom Pions
```
Tu as :

class Pions

alors qu'elle représente :

un pion
une tour
un fou
un roi
une reine

Donc elle devrait plutôt s'appeler class Pieces
```
### 3. Utilisation d'identifiants magiques
```
Tu utilises :
1 -> pion
2 -> cavalier
3 -> fou
4 -> tour
5 -> reine
6 -> roi
et les négatifs pour les noirs.

C'est difficile à maintenir.

Par exemple :

piece.id == 5

ne dit rien.

Je te conseille :
from enum import Enum

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
et 
class Color(Enum):
    WHITE = 0
    BLACK = 1
```
### 4. Les mouvements sont des fonctions globales
```
En POO, on ferait plutôt :
class Piece:
    def valid_moves(self, board):
        pass
puis
class Pawn(Piece):
    ...

class Knight(Piece):
    ...
C'est beaucoup plus extensible.
```
### 5. Mélange logique métier / interface
```
Dans le moteur tu as :

print("Invalid move")

ou

input(...)

Le moteur ne devrait jamais faire ça.
Par exemple :

resolve_move(...)

devrait retourner :

MoveResult.SUCCESS

MoveResult.INVALID

MoveResult.CHECK

et c'est l'interface qui affiche
```
### Architecture que je te recommande :
project/
│
├── model/
│   ├── game.py
│   ├── board.py
│   ├── move.py
│   ├── piece.py
│   ├── pawn.py
│   ├── knight.py
│   ├── bishop.py
│   ├── rook.py
│   ├── queen.py
│   └── king.py
│
├── controller/
│   └── game_controller.py
│
├── view/
│   ├── board_view.py
│   ├── iso_renderer.py
│   └── sprites/
│
├── tests/
│   ├── test_pawn.py
│   ├── test_rook.py
│   ├── test_check.py
│   └── test_mate.py
│
├── saves/
│
├── main.py
│
└── README.md

### Pour la partie isométrique

Je te conseille fortement pygame-ce.
Le plateau logique reste :

board[8][8]

mais l'affichage utilise une projection isométrique :
screen_x = (col - row) * TILE_WIDTH // 2
screen_y = (col + row) * TILE_HEIGHT // 2

### Fonctionnalité "afficher les coups possibles"

Avec l'architecture orientée objet :

moves = selected_piece.valid_moves(game)

Puis dans la vue :

for move in moves:
    draw_highlight(move)

C'est exactement une exigence du MVP.

### Sauvegarde

Je te conseille un format JSON :

{
  "turn": "white",
  "pieces": [
    {
      "type": "pawn",
      "color": "white",
      "x": 6,
      "y": 3
    }
  ]
}

Puis :

save_game(filename)
load_game(filename)

### Tests unitaires

Le sujet insiste beaucoup dessus.

Exemple :

def test_rook_blocked():

    game = Game()

    assert not game.board[7][0].can_move(5,0)

ou :

def test_pawn_double_move():

    game = Game()

    assert game.board[6][0].can_move(4,0)

Tu peux utiliser le framework standard :

pytest

À mon avis, avant de commencer la vue 3D isométrique, la priorité est de refactoriser ton moteur en vraies classes Piece, Pawn, Rook, Knight, etc.. Cela simplifiera énormément l'ajout de l'affichage, de la sauvegarde et des tests, et correspond beaucoup mieux à l'architecture MVC demandée.
- ce qui a été conservé, modifié ou rejeté + justification :
globalement je pense conserver au moins tous les changements numérotés de 1 à 5 dans sa réponse, ainsi que son architecture recomandée, car ça me semble effectivement juste et pertinant.
Pour ce qui est de la partie isométrique, je ne me suis pas encore vraiment intérogé sur la réalisation pratique, car ce sera après que la partie logique métier fonctionne. De même pour la partie de la sauvegarde.
Enfin pour les tests, il ne me donne rien de bien surprennant, c'est ce que j'aurais fait aussi, avec juste l'utilisation de pytest ou non.
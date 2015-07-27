**Attention** Le code présenté ici n'a rien à voir avec le projet Sketchfab en lui-même
**Warranty** The code from this project has no link with the Sketchfab project


# Exercice proposé par Sketchfab
------------------------------

Voici ma solution que je vous propose pour l'exercice que vous m'avez posé
suite à notre premier entretien.

## Rappel de l'énoncé:

* Partir d'une structure Django vierge **ok**
* Rajouter les users + un model Model3d() qui représente un modèle 3d **ok**
* Implémenter une fonctionnalité de 'badges'
    * il existe plusieurs types de badge, chacun étant décerné pour une action ou série d'action effectuée par l'utilisateur sur le site
        * La liste des badges qu'un user a obtenu doit être accessible via
          l'api **ok**
        * Le backend doit "décerner" les badges aux users (ie: détecter quand une action a été réalisée et donner le badge au user)
        * Badges a implémenter (liste non limitative):
            * _Star_: le modèle d'un user a plus de 1k views **ok**
            * _Collector_: un user a uploadé plus de 5 modèles **ok**
            * _Pionneer_: le user est inscrit depuis plus de 1 an sur le site
              **ok**

## installation

Le projet se nomme sketchfab_test_badges et l'application badges_handler.

creation d'un environnement virtuel, installation des dépendances et tests

    $ mkvirtualenv skechfab_exercice
    $ cd sketchfab_test_badges
    $ pip install -r requirements.txt
    $ python manage.py test badges_handler
    $ python manage.py runserver

## settings

dans le fichier de settings _sketchfab_test_badges/settings.py_, le
dictionnaire suivant permet de configurer les options des badges.

    BADGES_SETTINGS = {
        'star': 1000,  # number of views
        'pionner': ['00:00', ],  # each day at theses hours, check for pionner users
        'collector': 5,  # number of models a user must upload to get this badge
    }

## notes

* Le badge _star_ a été géré grace à un middleware, à chaque fois que la
  _DetailView_ d'un modèle est visité, le middleware met à plus 1 son nombre de
  visite. Ce choix a été fait plutôt que de surcharger la fonction
  _get\_queryset_ de la _DetailView_ _Model3dDetailView_. Il suffit en effet
  d'ajouter les urls cibles pour ajouter ce même badge à d'autres objets que
  les modèles 3d.
* Le badge _pionner_ est géré grâce à une tâche cron au travers de
  l'application django-cron. Après reflexion, pour un site avec de nombreux
  utilisateurs comme je pense _SketchFab_, une routine celery serait peut-être
  plus efficace.
* le badge _collector_ est remis au travers d'un callback associé au signal
  _post\_save_ sur le modèle Model3d. Lorsqu'un modèle est crée en base, son
  auteur est automatiquement enregistré à l'aide d'une clef étrangère. Si on
  suit cette clef, on peut récupérer son créateur et compter le nombre de
  modèles qu'il a déjà créer.
* Pour récupérer tout les badges de l'instance _creator_

        badges = creator.badges.all()

* J'ai décidé d'utiliser l'application _ContentType_ de Django pour créer une
  clef généric dans le modèle _Badge_ afin de pourvoir décerner de façon
  généric des badges à un utilisateur ou un modèle (ainsi chaque modèle peut
  être starré) ou encore à d'autres entités possibles.

### applications externes
* django-cron: http://django-cron.readthedocs.org/en/latest/index.html
* freezegun: https://github.com/spulec/freezegun

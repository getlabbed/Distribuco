**********
Distribuco
**********

.. raw:: html
    <div>

        <a href="https://distribuco.ca">
        <img src="https://img.shields.io/website?down_message=hors%20ligne&label=site%20web&up_message=en%20ligne&url=https%3A%2F%2Fdistribuco.ca" alt="Status du site"/>
        </a>

        <a href="https://github.com/getlabbed/Distribuco/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/getlabbed/Distribuco?color=blue" alt="License"/>
        </a>
    
    </div>

Mélangeur de boissons automatique connecté
==========================================

Projet Synthèse de programme pour `DEC en Technologies de systèmes ordinés <https://cegepoutaouais.qc.ca/programmes/programmes-techniques/genie-et-batiment/genie-electronique-programmable/>`_

Installation de l'environnement de développement
================================================

Installer Visual studio Code

Installer l'environnement de développement virtuel

run le script  

Installation des prérequis
==========================

.. code-block:: console

    pip install -r requirements.txt

Fichier d'environnement
=======================

importer le fichier d'environnement venant de google nommé «client_secret.json»

Exécuter le script GenerateSecretKey.py afin de générer un secret TOPT dans un fichier .env

Organisation du projet
======================
📚 `documentation/ <https://github.com/getlabbed/Distribuco/tree/main/docs/>`_
Aussi Disponible sur `docs.distribuco.ca <https://docs.distribuco.ca>`_

🖥️ `app/ <https://github.com/getlabbed/Distribuco/tree/main/app>`_
Application web accessible à partir de `distribuco.ca <https://distribuco.ca/>`_

⚙️ `start.py/ <https://github.com/getlabbed/Distribuco/blob/main/start.py>`_
Démarre l'application web

🖳 `raspberryApp/ <https://github.com/getlabbed/Distribuco/tree/main/raspberryApp/>`_
Application web sur le Raspberry Pi

⚙️ `raspStart.py/ <https://github.com/getlabbed/Distribuco/blob/main/raspStart.py>`_
Démarre l'application web pour le Raspberry Pi

Documentation réalisée à l'aide de `sphinx <https://www.sphinx-doc.org/>`_
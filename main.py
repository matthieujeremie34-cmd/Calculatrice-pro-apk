import kivy
kivy.require("2.0.0")

import math
import json
import os
import statistics

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


# =========================
# COULEURS
# =========================

FOND = (0.04, 0.07, 0.09, 1)
CARTE = (0.08, 0.12, 0.16, 1)
BLEU = (0.10, 0.45, 0.85, 1)
VERT = (0.05, 0.55, 0.35, 1)
VIOLET = (0.40, 0.25, 0.65, 1)
ORANGE = (0.75, 0.40, 0.10, 1)
ROUGE = (0.60, 0.15, 0.15, 1)
BLANC = (1, 1, 1, 1)


FICHIER_HISTORIQUE = "historique.json"


# =========================
# HISTORIQUE
# =========================

def charger_historique():
    if os.path.exists(FICHIER_HISTORIQUE):
        try:
            with open(FICHIER_HISTORIQUE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


historique = charger_historique()


def sauvegarder_historique():
    try:
        with open(FICHIER_HISTORIQUE, "w", encoding="utf-8") as f:
            json.dump(historique, f, ensure_ascii=False, indent=2)
    except:
        pass


# =========================
# BOUTON
# =========================

def bouton(texte, couleur=CARTE, taille=18):
    b = Button(
        text=texte,
        font_size=taille,
        background_normal="",
        background_color=couleur,
        color=BLANC
    )
    return b


# =========================
# ACCUEIL
# =========================

class Accueil(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        titre = Label(
            text="[b]CALCULATRICE PRO[/b]",
            markup=True,
            font_size=30,
            color=BLANC,
            size_hint_y=None,
            height=70
        )

        sous_titre = Label(
            text="Calcul scientifique et outils pratiques",
            font_size=16,
            color=(0.7, 0.75, 0.8, 1),
            size_hint_y=None,
            height=50
        )

        layout.add_widget(titre)
        layout.add_widget(sous_titre)

        b = bouton("🧮  CALCULATRICE", BLEU, 20)
        b.bind(on_press=lambda x: self.ouvrir("calculatrice"))
        layout.add_widget(b)

        b = bouton("🔄  CONVERTISSEUR", VERT, 20)
        b.bind(on_press=lambda x: self.ouvrir("convertisseur"))
        layout.add_widget(b)

        b = bouton("📊  STATISTIQUES", VIOLET, 20)
        b.bind(on_press=lambda x: self.ouvrir("statistiques"))
        layout.add_widget(b)

        b = bouton("📐  GÉOMÉTRIE", ORANGE, 20)
        b.bind(on_press=lambda x: self.ouvrir("geometrie"))
        layout.add_widget(b)

        b = bouton("📜  HISTORIQUE", CARTE, 20)
        b.bind(on_press=lambda x: self.ouvrir("historique"))
        layout.add_widget(b)

        b = bouton("ℹ️  À PROPOS", CARTE, 20)
        b.bind(on_press=lambda x: self.ouvrir("apropos"))
        layout.add_widget(b)

        version = Label(
            text="Version 1.0 • Créée avec Python + Kivy",
            font_size=13,
            color=(0.6, 0.65, 0.7, 1)
        )

        layout.add_widget(version)

        self.add_widget(layout)

    def ouvrir(self, nom):
        self.manager.current = nom


# =========================
# CALCULATRICE
# =========================

class Calculatrice(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.memoire = 0

        principal = BoxLayout(
            orientation="vertical",
            padding=8,
            spacing=5
        )

        # Affichage
        self.affichage = TextInput(
            text="",
            font_size=28,
            multiline=False,
            halign="right",
            size_hint_y=None,
            height=65,
            background_color=(0.02, 0.03, 0.04, 1),
            foreground_color=BLANC
        )

        principal.add_widget(self.affichage)

        # Retour
        retour = bouton("← Accueil", CARTE, 16)
        retour.size_hint_y = None
        retour.height = 45
        retour.bind(on_press=lambda x: self.accueil())
        principal.add_widget(retour)

        grille = GridLayout(
            cols=5,
            spacing=4
        )

        touches = [
            "C", "⌫", "(", ")", "^",
            "sin", "cos", "tan", "√", "π",
            "x²", "log", "ln", "1/x", "x!",
            "M+", "M-", "MR", "MC", "/",
            "7", "8", "9", "×", "−",
            "4", "5", "6", "+", "%",
            "1", "2", "3", ".", "=",
            "0"
        ]

        for t in touches:

            couleur = CARTE

            if t == "=":
                couleur = BLEU
            elif t == "C":
                couleur = ROUGE
            elif t in ["+", "−", "×", "/", "^"]:
                couleur = ORANGE
            elif t in ["sin", "cos", "tan", "√", "π",
                       "x²", "log", "ln", "1/x", "x!"]:
                couleur = VIOLET
            elif t in ["M+", "M-", "MR", "MC"]:
                couleur = VERT

            b = bouton(t, couleur, 17)
            b.bind(on_press=self.action)
            grille.add_widget(b)

        principal.add_widget(grille)

        self.add_widget(principal)

    def accueil(self):
        self.manager.current = "accueil"

    def action(self, instance):

        touche = instance.text

        try:

            if touche == "C":
                self.affichage.text = ""

            elif touche == "⌫":
                self.affichage.text = self.affichage.text[:-1]

            elif touche == "=":
                self.calculer()

            elif touche == "π":
                self.affichage.text += str(math.pi)

            elif touche == "√":
                valeur = float(self.affichage.text)
                self.affichage.text = str(math.sqrt(valeur))

            elif touche == "x²":
                valeur = float(self.affichage.text)
                self.affichage.text = str(valeur ** 2)

            elif touche == "sin":
                valeur = float(self.affichage.text)
                self.affichage.text = str(
                    math.sin(math.radians(valeur))
                )

            elif touche == "cos":
                valeur = float(self.affichage.text)
                self.affichage.text = str(
                    math.cos(math.radians(valeur))
                )

            elif touche == "tan":
                valeur = float(self.affichage.text)
                self.affichage.text = str(
                    math.tan(math.radians(valeur))
                )

            elif touche == "log":
                valeur = float(self.affichage.text)
                self.affichage.text = str(math.log10(valeur))

            elif touche == "ln":
                valeur = float(self.affichage.text)
                self.affichage.text = str(math.log(valeur))

            elif touche == "1/x":
                valeur = float(self.affichage.text)
                self.affichage.text = str(1 / valeur)

            elif touche == "x!":
                valeur = int(float(self.affichage.text))
                self.affichage.text = str(math.factorial(valeur))

            elif touche == "M+":
                self.memoire += float(self.affichage.text)

            elif touche == "M-":
                self.memoire -= float(self.affichage.text)

            elif touche == "MR":
                self.affichage.text = str(self.memoire)

            elif touche == "MC":
                self.memoire = 0

            else:

                symbole = {
                    "×": "*",
                    "−": "-",
                    "^": "**"
                }

                self.affichage.text += symbole.get(
                    touche, touche
                )

        except Exception:
            self.affichage.text = "Erreur"

    def calculer(self):

        expression = self.affichage.text

        try:

            expression = expression.replace(
                "×", "*"
            ).replace(
                "−", "-"
            ).replace(
                "^", "**"
            )

            resultat = eval(
                expression,
                {
                    "__builtins__": {},
                    "math": math
                }
            )

            resultat_str = str(resultat)

            historique.append(
                f"{expression} = {resultat_str}"
            )

            sauvegarder_historique()

            self.affichage.text = resultat_str

        except:
            self.affichage.text = "Erreur"


# =========================
# HISTORIQUE
# =========================

class Historique(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        titre = Label(
            text="[b]HISTORIQUE[/b]",
            markup=True,
            font_size=26,
            size_hint_y=None,
            height=60
        )

        layout.add_widget(titre)

        scroll = ScrollView()

        self.liste = Label(
            text="",
            font_size=17,
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.liste.bind(
            texture_size=self.liste.setter("size")
        )

        scroll.add_widget(self.liste)

        layout.add_widget(scroll)

        boutons = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=5
        )

        effacer = bouton(
            "Effacer",
            ROUGE,
            16
        )

        effacer.bind(
            on_press=self.effacer
        )

        retour = bouton(
            "← Accueil",
            CARTE,
            16
        )

        retour.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "accueil"
            )
        )

        boutons.add_widget(effacer)
        boutons.add_widget(retour)

        layout.add_widget(boutons)

        self.add_widget(layout)

        self.bind(
            on_enter=lambda x:
            self.actualiser()
        )

    def actualiser(self):

        if historique:

            texte = "\n".join(
                f"{i+1}. {ligne}"
                for i, ligne in enumerate(historique)
            )

        else:
            texte = "Aucun calcul."

        self.liste.text = texte

    def effacer(self, instance):

        historique.clear()
        sauvegarder_historique()
        self.actualiser()


# =========================
# CONVERTISSEUR
# =========================

class Convertisseur(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        layout.add_widget(
            Label(
                text="[b]CONVERTISSEUR[/b]",
                markup=True,
                font_size=26,
                size_hint_y=None,
                height=60
            )
        )

        self.type = Spinner(
            text="Longueur",
            values=[
                "Longueur",
                "Poids",
                "Température",
                "Temps"
            ],
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.type)

        self.unite1 = Spinner(
            text="m",
            values=["m", "km", "cm", "mm"],
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.unite1)

        self.unite2 = Spinner(
            text="km",
            values=["m", "km", "cm", "mm"],
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.unite2)

        self.entree = TextInput(
            hint_text="Valeur",
            input_filter="float",
            multiline=False,
            font_size=22,
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.entree)

        convertir = bouton(
            "CONVERTIR",
            BLEU,
            20
        )

        convertir.size_hint_y = None
        convertir.height = 60
        convertir.bind(
            on_press=self.convertir
        )

        layout.add_widget(convertir)

        self.resultat = Label(
            text="Résultat",
            font_size=22
        )

        layout.add_widget(self.resultat)

        retour = bouton(
            "← Accueil",
            CARTE,
            17
        )

        retour.size_hint_y = None
        retour.height = 55

        retour.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "accueil"
            )
        )

        layout.add_widget(retour)

        self.add_widget(layout)

        self.type.bind(
            text=self.changer_unites
        )

    def changer_unites(self, spinner, text):

        if text == "Longueur":

            valeurs = [
                "m", "km", "cm", "mm"
            ]

        elif text == "Poids":

            valeurs = [
                "kg", "g", "mg"
            ]

        elif text == "Température":

            valeurs = [
                "°C", "°F", "K"
            ]

        else:

            valeurs = [
                "s", "min", "h"
            ]

        self.unite1.values = valeurs
        self.unite2.values = valeurs

        self.unite1.text = valeurs[0]
        self.unite2.text = valeurs[1]

    def convertir(self, instance):

        try:

            valeur = float(
                self.entree.text
            )

            categorie = self.type.text
            u1 = self.unite1.text
            u2 = self.unite2.text

            if categorie == "Longueur":

                facteurs = {
                    "m": 1,
                    "km": 1000,
                    "cm": 0.01,
                    "mm": 0.001
                }

                resultat = (
                    valeur * facteurs[u1]
                ) / facteurs[u2]

            elif categorie == "Poids":

                facteurs = {
                    "kg": 1,
                    "g": 0.001,
                    "mg": 0.000001
                }

                resultat = (
                    valeur * facteurs[u1]
                ) / facteurs[u2]

            elif categorie == "Temps":

                facteurs = {
                    "s": 1,
                    "min": 60,
                    "h": 3600
                }

                resultat = (
                    valeur * facteurs[u1]
                ) / facteurs[u2]

            else:

                if u1 == "°C":
                    celsius = valeur
                elif u1 == "°F":
                    celsius = (valeur - 32) * 5 / 9
                else:
                    celsius = valeur - 273.15

                if u2 == "°C":
                    resultat = celsius
                elif u2 == "°F":
                    resultat = celsius * 9 / 5 + 32
                else:
                    resultat = celsius + 273.15

            self.resultat.text = (
                f"{valeur} {u1} = "
                f"{resultat:.6g} {u2}"
            )

        except:
            self.resultat.text = "Erreur"


# =========================
# STATISTIQUES
# =========================

class Statistiques(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        layout.add_widget(
            Label(
                text="[b]STATISTIQUES[/b]",
                markup=True,
                font_size=26,
                size_hint_y=None,
                height=60
            )
        )

        self.entree = TextInput(
            hint_text="Exemple : 10, 12, 15, 18",
            multiline=False,
            font_size=20,
            size_hint_y=None,
            height=60
        )

        layout.add_widget(self.entree)

        calculer = bouton(
            "CALCULER",
            BLEU,
            20
        )

        calculer.size_hint_y = None
        calculer.height = 60

        calculer.bind(
            on_press=self.calculer
        )

        layout.add_widget(calculer)

        self.resultat = Label(
            text="Résultats",
            font_size=18
        )

        layout.add_widget(self.resultat)

        retour = bouton(
            "← Accueil",
            CARTE,
            17
        )

        retour.size_hint_y = None
        retour.height = 55

        retour.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "accueil"
            )
        )

        layout.add_widget(retour)

        self.add_widget(layout)

    def calculer(self, instance):

        try:

            nombres = [
                float(x.strip())
                for x in self.entree.text.split(",")
            ]

            texte = (
                f"Somme : {sum(nombres):.2f}\n"
                f"Moyenne : {statistics.mean(nombres):.2f}\n"
                f"Médiane : {statistics.median(nombres):.2f}\n"
                f"Maximum : {max(nombres):.2f}\n"
                f"Minimum : {min(nombres):.2f}\n"
                f"Nombre : {len(nombres)}"
            )

            self.resultat.text = texte

        except:
            self.resultat.text = (
                "Erreur.\n"
                "Utilise par exemple :\n"
                "10, 12, 15, 20"
            )


# =========================
# GÉOMÉTRIE
# =========================

class Geometrie(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        layout.add_widget(
            Label(
                text="[b]GÉOMÉTRIE[/b]",
                markup=True,
                font_size=26,
                size_hint_y=None,
                height=60
            )
        )

        self.forme = Spinner(
            text="Carré",
            values=[
                "Carré",
                "Rectangle",
                "Cercle",
                "Triangle",
                "Cube",
                "Pavé droit"
            ],
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.forme)

        self.a = TextInput(
            hint_text="Valeur A",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.a)

        self.b = TextInput(
            hint_text="Valeur B",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.b)

        self.c = TextInput(
            hint_text="Valeur C",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.c)

        calculer = bouton(
            "CALCULER",
            ORANGE,
            20
        )

        calculer.size_hint_y = None
        calculer.height = 60

        calculer.bind(
            on_press=self.calculer
        )

        layout.add_widget(calculer)

        self.resultat = Label(
            text="Résultat",
            font_size=18
        )

        layout.add_widget(self.resultat)

        retour = bouton(
            "← Accueil",
            CARTE,
          17
        )

        retour.size_hint_y = None
        retour.height = 55

        retour.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "accueil"
            )
        )

        layout.add_widget(retour)

        self.add_widget(layout)

    def calculer(self, instance):

        try:

            forme = self.forme.text
            a = float(self.a.text or 0)
            b = float(self.b.text or 0)
            c = float(self.c.text or 0)

            if forme == "Carré":

                surface = a * a
                perimetre = 4 * a

                texte = (
                    f"Surface : {surface:.2f}\n"
                    f"Périmètre : {perimetre:.2f}"
                )

            elif forme == "Rectangle":

                surface = a * b
                perimetre = 2 * (a + b)

                texte = (
                    f"Surface : {surface:.2f}\n"
                    f"Périmètre : {perimetre:.2f}"
                )

            elif forme == "Cercle":

                surface = math.pi * a ** 2
                perimetre = 2 * math.pi * a

                texte = (
                    f"Surface : {surface:.2f}\n"
                    f"Circonférence : {perimetre:.2f}"
                )

            elif forme == "Triangle":

                surface = (a * b) / 2

                texte = (
                    f"Surface : {surface:.2f}"
                )

            elif forme == "Cube":

                surface = 6 * a ** 2
                volume = a ** 3

                texte = (
                    f"Surface : {surface:.2f}\n"
                    f"Volume : {volume:.2f}"
                )

            else:

                volume = a * b * c

                texte = (
                    f"Volume : {volume:.2f}"
                )

            self.resultat.text = texte

        except:
            self.resultat.text = "Erreur"


# =========================
# À PROPOS
# =========================

class APropos(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=20
        )

        layout.add_widget(
            Label(
                text="[b]CALCULATRICE PRO[/b]",
                markup=True,
                font_size=30
            )
        )

        layout.add_widget(
            Label(
                text=(
                    "Une calculatrice scientifique "
                    "créée avec Python et Kivy.\n\n"
                    "Fonctions disponibles :\n"
                    "• Calcul scientifique\n"
                    "• Historique\n"
                    "• Mémoire\n"
                    "• Convertisseur\n"
                    "• Statistiques\n"
                    "• Géométrie"
                ),
                font_size=17
            )
        )

        retour = bouton(
            "← Accueil",
            BLEU,
            18
        )

        retour.size_hint_y = None
        retour.height = 60

        retour.bind(
            on_press=lambda x:
            setattr(
                self.manager,
                "current",
                "accueil"
            )
        )

        layout.add_widget(retour)

        self.add_widget(layout)


# =========================
# APPLICATION
# =========================

class CalculatriceProApp(App):

    def build(self):

        self.title = "Calculatrice Pro"

        sm = ScreenManager()

        sm.add_widget(
            Accueil(name="accueil")
        )

        sm.add_widget(
            Calculatrice(name="calculatrice")
        )

        sm.add_widget(
            Historique(name="historique")
        )

        sm.add_widget(
            Convertisseur(name="convertisseur")
        )

        sm.add_widget(
            Statistiques(name="statistiques")
        )

        sm.add_widget(
            Geometrie(name="geometrie")
        )

        sm.add_widget(
            APropos(name="apropos")
        )

        return sm


if __name__ == "__main__":
    CalculatriceProApp().run()
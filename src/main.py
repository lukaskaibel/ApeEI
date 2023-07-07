from wikiPT import call_wikiPT_api
from eventPT import call_eventPT_api
from reflectionPT import analyse_reflection
from utils.create_event import create_event
from datetime import datetime


analyse_reflection(
    "In der letzten Woche habe ich mir Gedanken über das Projektthema gemacht, dass ich für das Softwareprojekt wählen möchte. Zur Auswahl stehen 4 Projekte, 2 mit Bienen, eins mit Fischen und eins mit der App in die ich gerade schreibe. Zunächst habe ich mich besonders für die App interessiert, weil ich es interessant finde, an einem neuen Produkt zu arbeiten. Allerdings interessieren mich in diesem Projekt die Unteraufgaben nicht so sehr, da sie häufig mit testen zu tun haben. Die Unteraugabe die mich am meisten interessiert hat ist die, wo man ein LLM trainieren soll. Das fände ich interessant, weil ich mich sowieso mal mit LLMs auseinandersetzen wollte. Meine zweite Option ist das eine Bienenprojekt, in dem Bienen aus Videomaterial herausgefiltert werden sollen. Das Projekt klingt interessant, ich war nur zunächst abgeneigt, weil ich mich bei meiner Bachelorarbeit bereits mit der Erkennung von Tieren (Pferden) beschäftigt habe und ich gerne eine neue Erfahrung machen wollte. Zu dem jetzigen Zeitpunkt bin ich mir immer noch nicht 100%ig sicher und werde die Entscheidung eventuell auch davon abhängig machen, wer meine Gruppenmitglieder sein werden. "
)

# term, url = call_wikiPT_api(
#     "Die Integration von Pythoncode in C++ Programm führte zu konflikten deren Bewältigung länger dauerte als die eigentliche Integration."
# )

# print(term)
# print(url)

# call_eventPT_api(
#     "I was very stressed today, because of my presentation tomorrow morning."
# )

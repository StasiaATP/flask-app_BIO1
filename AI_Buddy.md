<center>

# **AI-BUDDY: Verwendung von AI im Dev-Prozess des Flask Projekts "DEVTRACK"**

</center>


##  Studienfach: Datenbanksysteme  
**Team Gruppe BIO_1:** Anastasia Ceta, Edit Felföldi, Sabina Raykova, Doris Steinbauer

---

##  Einsatz von AI im Entwicklungsprozess

In unserem **DEVTRACK-Projekt** haben wir an verschiedenen Stellen AI-Tools (primär ChatGPT-4o) genutzt, um den Entwicklungsprozess zu beschleunigen und zu verbessern. AI wurde insbesondere in folgenden Bereichen eingesetzt:

###  1. Unbekannten Code erklären lassen

Dies funktioniert recht gut.  

Beispielprompt: "Bitte erkläre mir diesen Code [...] detailreich, so als ob ich noch nie mit CSS gearbeitet hätte."

###  2. CSS & Frontend-Design
Da das Styling in einem größeren Projekt schnell unübersichtlich werden kann, haben wir AI genutzt, um:

Vorschläge für **CSS-Strukturierung** und **Responsive Design** zu erhalten.  
Fehlerhafte Darstellungen und **Overlapping-Probleme** zu beheben.  
Bestehende **Bootstrap-Komponenten** für unsere Zwecke genau anzupassen.  

Beim Generieren von **HTML templates** war AI sehr hilfreich und hat uns viel Tipparbeit erspart.  

Dazu ein Beispielprompt: "Das ist mein Code für die Datenbank [...]. Bitte gib mir ein template HTML, das eine Liste aller Personen in der Datenbank anzeigt."

### 3. Generieren von Testdaten

Das **Generieren von Testdaten** funktionierte einwandfrei mit AI und hat uns wieder viel Tipparbeit erspart.

###  4. Fehlersuche & Debugging

AI wurde zur Analyse von **Fehlermeldungen** genutzt, insbesondere bei **Flask-Blueprints**, **SQLAlchemy-Fehlermeldungen** und **Flask-Login**.  
Komplexe Fehlermeldungen konnten schneller eingeordnet und behoben werden.  

Beispielprompt: "Ich bekomme bei flask run diesen Fehler [...]. Was ist der Grund dafür?"

###  5. AI vs. klassische Online-Recherche

#### Erkenntnis:
Während StackOverflow, Flask- und SQLAlchemy-Dokumentationen eine gute Ressource für spezifische Fragen bleiben, hat sich AI als **schneller und präziser** herausgestellt, um **individuelle Code-Optimierungen** vorzunehmen und **Konfigurationsprobleme** zu lösen. Besonders bei **komplexen Debugging-Prozessen** (z. B. Datenbank-Migrationsfehler) war AI hilfreicher als eine manuelle Suche.

###  6. Limitationen von AI

AI generiert nicht immer **fehlerfreien Code**, besonders bei spezifischen Flask-Konfigurationen.  
Wir mussten die Vorschläge immer **kritisch prüfen** und an die Anforderungen unseres Projekts anpassen.  
AI ist stark von den **gestellten Fragen** abhängig – präzise Prompts (auch mit Beispielcode) bringen bessere Ergebnisse.  

Beim Fehlersuchen findet AI meist nur die **häufigsten Fehler**, bei spezifischen Fehlern hilft sie oft nicht, man muss sie manuell suchen, v.a. wenn sich der Code auf mehrere andere Dateien bezieht.

---

##  Fazit & Lessons Learned

> **"Mit großem Code kommt großes Debugging!"**

Unser **AI-Buddy** hat uns in vielen Bereichen Zeit gespart, insbesondere bei der **Fehlersuche**. Dennoch bleibt die klassische **Recherche auf Entwickler-Foren** unverzichtbar, besonders wenn es um spezielle **Framework-Probleme** geht.  
**ChatGPT-4o** eignet sich gut zur **Erklärung, Strukturierung und Optimierung**, aber **denken & testen** und spezifisch anpassen mussten wir selbst.


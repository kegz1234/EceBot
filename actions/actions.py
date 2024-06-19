# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import random
import re
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from fuzzywuzzy import process
import requests
from bs4 import BeautifulSoup
import mysql.connector

config_db = {
    'host': 'localhost',
    'user': '****',
    'password': '****',
    'database': 'e_grammateia'
}

met_db = ["Πράσινη Ηλεκτρική Ενέργεια: Ευφυείς Τεχνολογίες και Στρατηγικές Διαχείρισης", "Βιοϊατρική Μηχανική",
          "Ολοκληρωμένα Συστήματα Υλικού και Λογισμικού", "Αλληλεπίδραση Ανθρώπου-Υπολογιστή",
          "Συστήματα Επεξεργασίας Πληροφορίας και Μηχανική Νοημοσύνη"]


# computer_choice & determine_winner functions refactored from
# https://github.com/thedanelias/rock-paper-scissors-python/blob/master/rockpaperscissors.py, MIT liscence

class ActionProgrammaSpoudon(Action):

    def name(self) -> Text:
        return "action_programma_spoudon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entry_year = tracker.get_slot("etos_eisagoghs")

        entry_year = re.split("-|/| ", entry_year)
        if int(entry_year[0]) <= 2014:
            dispatcher.utter_message(
                "Το προγράμμα σπουδών για τα έτη εισαγωγής 2014-2015 και πριν είναι:\n https://www.ece.upatras.gr/images/Attachments/programma_spoudwn/%CE%A0%CF%81%CE%BF%CC%81%CE%B3%CF%81%CE%B1%CE%BC%CE%BC%CE%B1_%CE%A3%CF%80%CE%BF%CF%85%CE%B4%CF%89%CC%81%CE%BD_2023_2024_%CE%95%CE%B9%CF%83%CE%B1%CE%B3%CF%89%CE%B3%CE%B7%CC%81_2014_2015_%CE%BA%CE%B1%CE%B9_%CF%80%CF%81%CE%B9%CE%BD_v1.pdf ")
        elif int(entry_year[0]) == 2015 or int(entry_year[0]) == 2016:
            dispatcher.utter_message(
                "Το προγράμμα σπουδών για τα έτη εισαγωγής 2015-2016 και 2016-2017 είναι:\n https://www.ece.upatras.gr/images/Attachments/programma_spoudwn/%CE%A0%CF%81%CE%BF%CC%81%CE%B3%CF%81%CE%B1%CE%BC%CE%BC%CE%B1_%CE%A3%CF%80%CE%BF%CF%85%CE%B4%CF%89%CC%81%CE%BD_2023_2024_%CE%95%CE%B9%CF%83%CE%B1%CE%B3%CF%89%CE%B3%CE%B7%CC%81_2015_2016__2016_2017_v1.pdf")
        else:
            dispatcher.utter_message(
                "Το προγράμμα σπουδών για τα έτη εισαγωγής  2017-2018 και έπειτα είναι:\n  https://www.ece.upatras.gr/images/Attachments/programma_spoudwn/%CE%A0%CF%81%CE%BF%CC%81%CE%B3%CF%81%CE%B1%CE%BC%CE%BC%CE%B1_%CE%A3%CF%80%CE%BF%CF%85%CE%B4%CF%89%CC%81%CE%BD_2023_2024_v1.pdf")

        return [SlotSet("etos_eisagoghs", None)]


class SecretaryCommunication(Action):
    def name(self) -> Text:
        return "action_secretary_communication"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        eidos_f = tracker.get_slot("eidos_foithshs")
        telephone = tracker.get_slot("phone")
        email = tracker.get_slot("mail")
        stoixeia_ep = tracker.get_slot("communication_info")

        if eidos_f is None:
            if (stoixeia_ep is not None) or (telephone is not None and email is not None):
                dispatcher.utter_message(
                    "Τα τηλεφωνα και τo mail επικοινωνίας της  γραμματείας του προπτυχιακού κύκλου σπουδών φαίνονται παρακάτω:")
                dispatcher.utter_message("THΛΕΦΩΝΑ:\n2610996423,\n2610996418,\n2610996420")
                dispatcher.utter_message("e-mail:secretary-students@ece.upatras.gr")
                dispatcher.utter_message(
                    "Τα τηλεφωνα και τo mail επικοινωνίας της  γραμματείας του μεταπτυχιακού κύκλου σπουδών φαίνονται παρακάτω:")
                dispatcher.utter_message("THΛΕΦΩΝΑ:\n2610996422,\n2610996493,\n2610996419")
                dispatcher.utter_message("e-mail:\nsecretary-graduate@ece.upatras.gr\npanagiot@ece.upatras.gr")
            elif telephone is not None and email is None:
                dispatcher.utter_message(
                    "Tα τηλέφωνα της γραμματείας του προπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("2610996423\n2610996418\n2610996420")
                dispatcher.utter_message(
                    "Τα τηλεφωνα επικοινωνίας της  γραμματείας του μεταπτυχιακού κύκλου σπουδών φαίνονται παρακάτω:")
                dispatcher.utter_message("THΛΕΦΩΝΑ:\n2610996422\n2610996493\n2610996419")
            elif email is not None:
                dispatcher.utter_message("To mail του προπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("secretary-students@ece.upatras.gr")
                dispatcher.utter_message(
                    "Tα mail της γραμματείας του μεταπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("secretary-graduate@ece.upatras.gr\npanagiot@ece.upatras.gr")
        elif eidos_f.startswith("π") or eidos_f.startswith("Π"):
            if stoixeia_ep is not None or (telephone is not None and email is not None):
                dispatcher.utter_message(
                    "Τα τηλεφωνα και τo mail επικοινωνίας της  γραμματείας του προπτυχιακού κύκλου σπουδών φαίνονται παρακάτω:")
                dispatcher.utter_message("THΛΕΦΩΝΑ:\n2610996423\n2610996418\n2610996420")
                dispatcher.utter_message("e-mail:secretary-students@ece.upatras.gr")
            elif telephone is not None:
                dispatcher.utter_message(
                    "Tα τηλέφωνα της γραμματείας του προπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("2610996423\n2610996418\n2610996420")
            elif email is not None:
                dispatcher.utter_message("To mail του προπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("secretary-students@ece.upatras.gr")
        elif eidos_f.startswith("μ") or eidos_f.startswith("Μ"):
            if stoixeia_ep is not None or (telephone is not None and email is not None):
                dispatcher.utter_message(
                    "Τα τηλεφωνα και τo mail επικοινωνίας της  γραμματείας του μεταπτυχιακού κύκλου σπουδών φαίνονται παρακάτω:")
                dispatcher.utter_message("THΛΕΦΩΝΑ:\n2610996422\n2610996493\n2610996419")
                dispatcher.utter_message("e-mail:\nsecretary-graduate@ece.upatras.gr\npanagiot@ece.upatras.gr")
            elif telephone is not None:
                dispatcher.utter_message(
                    "Tα τηλέφωνα της γραμματείας του μεταπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("2610996422\n2610996493\n2610996419")
            elif email is not None:
                dispatcher.utter_message(
                    "Tα mail της γραμματείας του μεταπτυχιακού κυκλου σπουδών είναι τα παρακάτω:\n")
                dispatcher.utter_message("secretary-graduate@ece.upatras.gr\npanagiot@ece.upatras.gr")
        return [SlotSet("eidos_foithshs", None), SlotSet("phone", None), SlotSet("mail", None),
                SlotSet("communication_info", None)]


class MasterProgramms(Action):
    def name(self) -> Text:
        return "action_specific_postgrad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        master_programms = tracker.get_slot("masters")
        if master_programms is None:
            dispatcher.utter_message(
                "Ουπς δεν σε κατάλαβα.Μπορείς να επαναδιατυπώσεις ή να δεις τις επιλογές σου πατώντας ΜΕΝΟΥ")
            return []

        for master in master_programms:
            best_match = process.extractOne(master, met_db)[0]
            if best_match == met_db[0]:
                response = requests.get(
                    "http://greenpower.upatras.gr/index.php/%CF%80%CE%BB%CE%B7%CF%81%CE%BF%CF%86%CE%BF%CF%81%CE%B9%CE%B5%CF%83/%CE%B1%CE%BD%CF%84%CE%B9%CE%BA%CE%B5%CE%B9%CE%BC%CE%B5%CE%BD%CE%BF-%CF%83%CE%BA%CE%BF%CF%80%CE%BF%CF%83")
                my_website_code = response.text

                soup = BeautifulSoup(my_website_code, "html.parser")
                descriptions = soup.find_all(name="p", style="text-align: justify;")
                names = soup.find_all(name="p", style="text-align: left;")
                for target in range(len(descriptions)):
                    if target == 1:
                        for i in range(len(names) - 1):
                            dispatcher.utter_message(names[i].getText())
                    dispatcher.utter_message(descriptions[target].getText())
                for name in names:
                    dispatcher.utter_message(name.getText())
                #dispatcher.utter_message(names[i + 1].getText())
                dispatcher.utter_message(
                    f'Μπορείς να δεις περισσότερες πληροφορίες για το ΜΔΕ {best_match} εδω:http://greenpower.upatras.gr/')
                return [SlotSet("masters", None)]
            elif best_match == met_db[1]:
                response = requests.get("https://www.biomed.upatras.gr/overview/")
                my_website = response.text

                soup = BeautifulSoup(my_website, "html.parser")
                description = soup.find_all("p")
                for i in range(2, len(description)):
                    dispatcher.utter_message(description[i].text)
                dispatcher.utter_message(
                    f'Μπορείς να δεις περισσότερες πληροφορίες για το ΜΔΕ {best_match} εδω:https://www.biomed.upatras.gr/')
                return [SlotSet("masters", None)]
            elif best_match == met_db[2]:
                response = requests.get("https://hsis.upatras.gr/")
                my_website = response.text

                soup = BeautifulSoup(my_website, "html.parser")
                description = soup.find_all("p")

                for i in range(9, len(description) - 1):
                    dispatcher.utter_message(description[i].text)
                dispatcher.utter_message(
                    f'Μπορείς να δεις περισσότερες πληροφορίες για το ΜΔΕ {best_match} εδω:https://hsis.upatras.gr/')
                return [SlotSet("masters", None)]
            elif best_match == met_db[3]:
                dispatcher.utter_message(
                    f'Μπορείς να δεις περισσότερες πληροφορίες για το ΜΔΕ {best_match} εδω:https://hcimaster.upatras.gr/')
                return [SlotSet("masters", None)]
            elif best_match == met_db[4]:
                response = requests.get("http://xanthippi.ceid.upatras.gr/dsp/")
                my_website = response.text

                soup = BeautifulSoup(my_website, "html.parser")
                description = soup.find_all("p")

                for i in range(1, len(description)):
                    dispatcher.utter_message(description[i].text)
                dispatcher.utter_message(
                    f'Μπορείς να δεις περισσότερες πληροφορίες για το ΜΔΕ {best_match} εδω:http://xanthippi.ceid.upatras.gr/dsp/')
                return [SlotSet("masters", None)]


class Classrooms(Action):
    def name(self) -> Text:
        return "action_aithousa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        classroom = tracker.get_slot("aithousa")
        if classroom is None:
            dispatcher.utter_message(
                "Mπορείς να δεις τις αίθουσες του τμήματος εδώ:https://www.ece.upatras.gr/images/IMAGES/classrooms_ece_.png")
        elif classroom is not None:
            dispatcher.utter_message(
                f"Μπορείς να δείς που βρίσκεται η αίθουσα {classroom} εδώ:https://www.ece.upatras.gr/images/IMAGES/classrooms_ece_.png")

        return [SlotSet("aithousa", None)]


class ArgiesEtous(Action):
    def name(self) -> Text:
        return "action_argies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("https://www.upatras.gr/stay-tuned/academic-calendar/")
        my_website = response.text

        soup = BeautifulSoup(my_website, "html.parser")
        web_s_info = soup.find_all("ul", style="text-align: justify;")
        argies = web_s_info[4].find_all("li")
        dispatcher.utter_message("Οι αργίες του ακαδημαϊκου έτους είναι οι παρακάτω:")
        for argia in argies:
            dispatcher.utter_message(argia.text)
        return []


class Stegash(Action):
    def name(self) -> Text:
        return "action_dikaiologhtika_stegashs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "Μπορείς να βρείς τα απαραίτητα δικαιολογητικά για δωρεάν στέγαση στιw φοιτητικές εστίες του Πανεπιστημίου εδώ:https://rb.gy/r7w09v")

        response = requests.get('https://www.upatras.gr/foitites/foititiki-merimna/stegasi/')
        my_web = response.text

        soup = BeautifulSoup(my_web, "html.parser")
        periexomena = soup.find("div", class_="entry-content")
        tag_list = []
        for p_tags in periexomena.find_all("p"):
            a_tags = p_tags.find("a", target="_blank")
            if a_tags:
                tag_list.append(a_tags.get("href"))
        dispatcher.utter_message(f"Για τη συμπλήρωση και κατάθεση της αίτησης πατήστε εδώ :{tag_list[0]}")
        return []


class Sitisi(Action):
    def name(self) -> Text:
        return "action_dikaiologhtika_sitisis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "Μπορείς να βρείς τα απαραίτητα δικαιολογητικά για έκδοση κάρτας σίτισης εδώ:https://rb.gy/l9pu6o")
        dispatcher.utter_message("Καθώς επίσης και το όριο εισοδήματος εδώ:https://rb.gy/hh3do5")

        response = requests.get('https://www.upatras.gr/foitites/foititiki-merimna/sitisi/')
        my_web = response.text

        tag_list = []
        soup = BeautifulSoup(my_web, "html.parser")
        periexomena = soup.find("div", class_="entry-content")
        tags = periexomena.find_all("p")
        for tag in tags:
            if tag.find("a"):
                tag_list.append(tag.find("a")["href"])

        dispatcher.utter_message(f"Για τη συμπλήρωση και κατάθεση της αίτησης πατήστε εδώ :{tag_list[0]}")
        return []


class Tomeis_Gen(Action):
    def name(self) -> Text:
        return "action_tomeis_general"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db = mysql.connector.connect(**config_db)
        tomeas = next(tracker.get_latest_entity_values('tomeas'), None)

        if tomeas is not None:

            try:

                cursor = db.cursor()


                cursor.execute("select Name_Tomea from tomeis")
                resulta=cursor.fetchall()
                cursor.execute("SELECT Name_Tomea FROM tomeis")
                result = cursor.fetchall()
                tomeis_list = [row[0] for row in result]

                if tomeas not in tomeis_list:
                    best_match = process.extractOne(tomeas, tomeis_list)
                    tomeas = best_match[0] if best_match else tomeas



                query = """
                                SELECT Prof_name FROM professor p
                                INNER JOIN tomeis t ON p.Prof_no = t.Director_ID
                                WHERE t.Name_Tomea = %s
                                """
                cursor.execute(query, (tomeas,))
                result = cursor.fetchall()

                if tomeas == "Τηλεπικοινωνιών και Τεχνολογίας Πληροφορίας":
                    dispatcher.utter_message(f"Ο τομέας Τ/ΤΠ έιναι ένας απο τους 4 τομείς του ΗΜΤΥ.")
                    dispatcher.utter_message(f"Διευθυντής του είναι ο {result[0][0]}.")
                    dispatcher.utter_message(
                        f"Μπορεις να βρεις όλες τις πληροφορίες που χρειάζεσαι για τον τομέα {tomeas} παρακάτω:")
                    dispatcher.utter_message(
                        "https://www.ece.upatras.gr/index.php/el/divisions/division-of-telecommunications-information-technology.html")
                if tomeas == "Συστημάτων Ηλεκτρικής Ενέργειας":
                    dispatcher.utter_message(f"Ο τομέας ΣΗΕ έιναι ένας απο τους 4 τομείς του ΗΜΤΥ.")
                    dispatcher.utter_message(f"Διευθυντής του είναι ο {result[0][0]}.")
                    dispatcher.utter_message(
                        f"Μπορεις να βρεις όλες τις πληροφορίες που χρειάζεσαι για τον τομέα {tomeas} παρακάτω:")
                    dispatcher.utter_message(
                        "https://www.ece.upatras.gr/index.php/el/divisions/division-of-electric-power-systems.html")

                if tomeas == "Ηλεκτρονικής και Υπολογιστών":
                    dispatcher.utter_message(f"Ο τομέας Η/Υ έιναι ένας απο τους 4 τομείς του ΗΜΤΥ.")
                    dispatcher.utter_message(f"Διευθυντής του είναι ο {result[0][0]}.")
                    dispatcher.utter_message(
                        f"Μπορεις να βρεις όλες τις πληροφορίες που χρειάζεσαι για τον τομέα {tomeas} παρακάτω:")
                    dispatcher.utter_message(
                        "https://www.ece.upatras.gr/index.php/el/divisions/division-of-electronics-and-computers.html")

                if tomeas == "Συστημάτων και Αυτομάτου Ελέγχου":
                    dispatcher.utter_message(f"Ο τομέας ΣΑΕ έιναι ένας απο τους 4 τομείς του ΗΜΤΥ.")
                    dispatcher.utter_message(f"Διευθυντής του είναι ο {result[0][0]}.")
                    dispatcher.utter_message(
                        f"Μπορεις να βρεις όλες τις πληροφορίες που χρειάζεσαι για τον τομέα {tomeas} παρακάτω:")
                    dispatcher.utter_message(
                        "https://www.ece.upatras.gr/index.php/el/divisions/division-of-systems-and-control.html")
                cursor.close()
            except:
                dispatcher.utter_message("Ούπς...  Δεν μπόρεσα να ανακτήσω στοιχεία...")
        else:
            dispatcher.utter_message("Οι τομείς του ΗΜΤΥ είναι οι εξής:")

            try:
                cursor = db.cursor()
                q = "select Name_Tomea from tomeis"
                cursor.execute(q)
                result = cursor.fetchall()
                for i in range(len(result)):
                    if i == 0:
                        dispatcher.utter_message(
                            f'{result[i][0]},https://www.ece.upatras.gr/index.php/el/divisions/division-of-telecommunications-information-technology.html')
                    if i == 1:
                        dispatcher.utter_message(
                            f'{result[i][0]},https://www.ece.upatras.gr/index.php/el/divisions/division-of-electric-power-systems.html')
                    if i == 2:
                        dispatcher.utter_message(
                            f'{result[i][0]},https://www.ece.upatras.gr/index.php/el/divisions/division-of-electronics-and-computers.html')
                    if i == 3:
                        dispatcher.utter_message(
                            f'{result[i][0]},https://www.ece.upatras.gr/index.php/el/divisions/division-of-systems-and-control.html')
                    cursor.close()
            except:
                dispatcher.utter_message("Ούπς...  Δεν μπόρεσα να ανακτήσω στοιχεία...")
        db.close()
        return []





class Roes(Action):
    def name(self) -> Text:
        return "action_roes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        db = mysql.connector.connect(**config_db)
        try:
            cursor = db.cursor()
            q = "select name_rohs from roes"
            cursor.execute(q)
            result = cursor.fetchall()
            dispatcher.utter_message("Οι κατευθύνσεις του τμήματος είναι οι παρακάτω:")
            for row in result:
                dispatcher.utter_message(row[0])
            cursor.close()
        except:
            dispatcher.utter_message("Ούπς...  Δεν μπόρεσα να ανακτήσω στοιχεία...")
        db.close()
        return []


class Roes_Mathimata(Action):
    def name(self) -> Text:
        return "action_roes_lessons"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        semester = tracker.get_slot("semno")
        kat = tracker.get_slot("roh")
        omada = tracker.get_slot("omada")
        labs=tracker.get_slot("lab")
        if kat=="Υπολογιστές Λογισμικό και Υλικό":
            kat="Υπολογιστές: Λογισμικό και Υλικό"


        sem_dict = {"πρώτο": 1, "δεύτερο": 2, "τρίτο": 3, "τέταρτο": 4, "πέμπτο": 5, "έκτο": 6, "έβδομο": 7, "όγδωο": 8,
                    "έννατο": 9, "δέκατο": 10}
        if semester not in sem_dict.keys() and semester is not None:
            dispatcher.utter_message("Λυπάμαι δεν καταλαβαίνω το εξάμηνο για το οποίο θες πληροφορίες.Μπορείς να επανλάβεις την ερώτηση;")
            return [SlotSet("semno", None), SlotSet("omada", None), SlotSet("roh", None), SlotSet("lab", None)]
        if semester is not None:
            sem_i = sem_dict[semester]
            db = mysql.connector.connect(**config_db)
            try:
                cursor = db.cursor()
                if sem_i>=7 and sem_i<11:

                    q = "select name_rohs from Roes"
                    cursor.execute(q)
                    res1 = cursor.fetchall()
                    result_roes = [row[0] for row in res1]
                    if kat is not None and kat not in result_roes:
                        best_match=process.extractOne(kat,result_roes)
                        kat=best_match[0]

                    if kat in result_roes:

                        if labs is None:
                            if omada is None:
                                q1 = "select c.Course_name, c.Semester, r.name_rohs " \
                                     "from c_belongs_r cr " \
                                     "inner join courses c on c.Course_Code=cr.Course_Code " \
                                     "inner join roes r on r.id_rohs=cr.id_rohs " \
                                     "where c.Semester=%s and r.name_rohs=%s"
                                cursor.execute(q1,(sem_i,kat))
                                res2=cursor.fetchall()
                                dispatcher.utter_message(f"Τα μαθήματα της κατεύθυνσης {kat} του {sem_i}ου εξαμήνου είναι:")
                                for row in res2:
                                    dispatcher.utter_message(row[0])
                            elif omada=="Α":
                                q2 = "select c.Course_name, c.Semester, r.name_rohs " \
                                     "from c_belongs_r cr " \
                                     "inner join courses c on c.Course_Code=cr.Course_Code " \
                                     "inner join roes r on r.id_rohs=cr.id_rohs " \
                                     "where c.Semester=%s and r.name_rohs=%s and cr.Omada=%s"
                                cursor.execute(q2,(sem_i,kat,omada))
                                res3=cursor.fetchall()
                                dispatcher.utter_message(f"Τα μαθήματα της {omada} ομάδας της κατεύθυνσης {kat} του {sem_i}ου εξαμήνου είναι:")
                                for row in res3:
                                    dispatcher.utter_message(row[0])
                            else:
                                q3 = "select c.Course_name, c.Semester, r.name_rohs " \
                                     "from c_belongs_r cr " \
                                     "inner join courses c on c.Course_Code=cr.Course_Code " \
                                     "inner join roes r on r.id_rohs=cr.id_rohs " \
                                     "where c.Semester=%s and r.name_rohs=%s and cr.Omada=%s"
                                cursor.execute(q3,(sem_i,kat,omada))
                                res4=cursor.fetchall()
                                dispatcher.utter_message(f"Τα μαθήματα της {omada} ομάδας της κατεύθυνσης {kat} του {sem_i}ου εξαμήνου είναι:")
                                for row in res4:
                                    dispatcher.utter_message(row[0])
                                dispatcher.utter_message("Καθώς επίσης και όλα τα μαθήματα των άλλων κατευθύνσεων!!!")
                        else:

                            if omada is None:
                                q1 = "select c.Course_name, c.Lab " \
                                     "from c_belongs_r cr " \
                                     "inner join courses c on c.Course_Code=cr.Course_Code " \
                                     "inner join roes r on r.id_rohs=cr.id_rohs " \
                                     "where c.Semester=%s and r.name_rohs=%s and c.Lab='Ν'"
                                cursor.execute(q1,(sem_i,kat))
                                res2=cursor.fetchall()
                                dispatcher.utter_message(f"Τα μαθήματα της κατεύθυνσης {kat} του {sem_i}ου εξαμήνου που έχουν εργαστήριο είναι:")
                                for row in res2:
                                    dispatcher.utter_message(row[0])
                            elif omada=="Α":
                                q2 = "select c.Course_name " \
                                     "from c_belongs_r cr " \
                                     "inner join courses c on c.Course_Code=cr.Course_Code " \
                                     "inner join roes r on r.id_rohs=cr.id_rohs " \
                                     "where c.Semester=%s and r.name_rohs=%s and cr.Omada=%s and c.Lab='Ν'"
                                cursor.execute(q2,(sem_i,kat,omada))
                                res3=cursor.fetchall()
                                dispatcher.utter_message(f"Τα μαθήματα της {omada} ομάδας της κατεύθυνσης {kat} του {sem_i}ου εξαμήνου που έχουν εργαστήριο είναι:")
                                for row in res3:
                                    dispatcher.utter_message(row[0])
                            else:
                                q3 = "select c.Course_name, c.Semester, r.name_rohs " \
                                     "from c_belongs_r cr " \
                                     "inner join courses c on c.Course_Code=cr.Course_Code " \
                                     "inner join roes r on r.id_rohs=cr.id_rohs " \
                                     "where c.Semester=%s and r.name_rohs=%s and cr.Omada=%s and c.Lab='Ν'"
                                cursor.execute(q3,(sem_i,kat,omada))
                                res4=cursor.fetchall()
                                dispatcher.utter_message(f"Τα μαθήματα της {omada} ομάδας της κατεύθυνσης {kat} του {sem_i}ου εξαμήνου που έχουν εργαστήριο είναι:")
                                for row in res4:
                                    dispatcher.utter_message(row[0])
                    elif kat is None:
                        if labs is None:
                            q1 = "SELECT DISTINCT Course_name FROM Courses WHERE Semester=%s"
                            cursor.execute(q1, (sem_i,))
                            res2 = cursor.fetchall()
                            dispatcher.utter_message(f"Τα μαθήματα του {sem_i}ου εξαμήνου είναι:")
                            for row in res2:
                                dispatcher.utter_message(row[0])

                        else:
                            q1 = "SELECT DISTINCT Course_name FROM Courses WHERE Semester=%s AND Lab='Ν'"
                            cursor.execute(q1, (sem_i,))
                            res2 = cursor.fetchall()
                            dispatcher.utter_message(f"Τα μαθήματα του {sem_i}ου εξαμήνου που έχουν εργαστήριο είναι:")
                            for row in res2:
                                dispatcher.utter_message(row[0])
                elif sem_i>0 and sem_i<7:
                    if labs is None:
                        if sem_i>1:
                            q1 = "SELECT DISTINCT Course_name FROM Courses WHERE Semester=%s"
                            cursor.execute(q1, (sem_i,))
                            res2 = cursor.fetchall()
                            dispatcher.utter_message(f"Τα μαθήματα του {sem_i}ου εξαμήνου είναι:")
                            for row in res2:
                                dispatcher.utter_message(row[0])
                        else:
                            q1 = "SELECT DISTINCT Course_name FROM Courses WHERE Semester=%s and Course_Type='O'"
                            cursor.execute(q1, (sem_i,))
                            res2 = cursor.fetchall()
                            dispatcher.utter_message(f"Τα μαθήματα του {sem_i}ου εξαμήνου είναι:")
                            for row in res2:
                                dispatcher.utter_message(row[0])

                            dispatcher.utter_message("Καθώς επίσης και ένα απο τα παρακάτω επιλογής:")
                            q2 = "SELECT DISTINCT Course_name FROM Courses WHERE Semester=%s and Course_Type='C'"
                            cursor.execute(q2, (sem_i,))
                            res3 = cursor.fetchall()
                            for row in res3:
                                dispatcher.utter_message(row[0])
                    else:
                        q1 = "SELECT DISTINCT Course_name FROM Courses WHERE Semester=%s AND Lab='Ν'"
                        cursor.execute(q1, (sem_i,))
                        res2 = cursor.fetchall()
                        dispatcher.utter_message(f"Τα μαθήματα του {sem_i}ου εξαμήνου που έχουν εργαστήριο είναι:")
                        for row in res2:
                            dispatcher.utter_message(row[0])

                else:
                    dispatcher.utter_message("Δεν κατάλαβα το εξάμηνο για το οποίο θες πληροφορίες")
                cursor.close()
            except:
                dispatcher.utter_message(f"Ουπς... κάτι πήγε στραβά!!!")

            db.close()
        else:
            dispatcher.utter_message("Συγγνωμη αλλά για να σε βοηθήσω πρέπει να επαναδιατυπώσεις την ερώτηση σου με το εξάμηνο για το οποίο θες πληροφορίες!!!")
        return [SlotSet("omada", None),SlotSet("lab", None)]

class Kathigites_Mathimata(Action):
    def name(self) -> Text:
        return "action_prof_lessons"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        professor=tracker.get_slot("prof")


        db = mysql.connector.connect(**config_db)
        cursor = db.cursor()
        q = "select Prof_name from Professor"
        cursor.execute(q)
        res = cursor.fetchall()
        prof_list = [row[0] for row in res]
        if professor is not None:

            if professor in prof_list:
                qa="select c.Course_name,c.Semester " \
                    "from courses c " \
                    "inner join teaches t " \
                    "on c.Course_Code=t.Course_code " \
                    "inner join Professor p " \
                    "on p.Prof_no=t.Prof_id " \
                    "where p.Prof_name=%s" \
                    "order by c.Semester"
                cursor.execute(qa,(professor,))
                resa=cursor.fetchall()
                if professor[-1]!="α":
                    dispatcher.utter_message(f"Τα μαθήματα που διδάσκει ο καθηγητής {professor} είναι:")
                else:
                    dispatcher.utter_message(f"Τα μαθήματα που διδάσκει η καθηγήτρια {professor} είναι:")
                for row in resa:
                    dispatcher.utter_message(f"{row[0]}  {row[1]}ο εξάμηνο")
                cursor.close()
                return[]
            else:
                best_match = process.extractOne(professor, prof_list)
                professor = best_match[0]
                qa = """
                SELECT c.Course_name,c.Semester 
                FROM courses c 
                INNER JOIN teaches t ON c.Course_Code = t.Course_code 
                INNER JOIN Professor p ON p.Prof_no = t.Prof_id 
                WHERE p.Prof_name = %s
                order by c.Semester
                """
                cursor.execute(qa, (professor,))
                resa = cursor.fetchall()

                if professor.endswith("α"):
                    message = f"Τα μαθήματα που διδάσκει η καθηγήτρια {professor} είναι:"
                else:
                    message = f"Τα μαθήματα που διδάσκει ο καθηγητής {professor} είναι:"

                dispatcher.utter_message(message)
                for row in resa:
                    dispatcher.utter_message(f"{row[0]}  {row[1]}ο εξάμηνο")
                cursor.close()
                return[]
        else:
            user_message = tracker.latest_message.get('text')

            best_match = process.extractOne(user_message, prof_list)


            if best_match and best_match[1]>60:
                professor = best_match[0]
                qa = """
                SELECT c.Course_name,c.Semester 
                FROM courses c 
                INNER JOIN teaches t ON c.Course_Code = t.Course_code 
                INNER JOIN Professor p ON p.Prof_no = t.Prof_id 
                WHERE p.Prof_name = %s
                order by c.Semester
                """
                cursor.execute(qa, (professor,))
                resa = cursor.fetchall()

                if professor.endswith("α"):
                    message = f"Τα μαθήματα που διδάσκει η καθηγήτρια {professor} είναι:"
                else:
                    message = f"Τα μαθήματα που διδάσκει ο καθηγητής {professor} είναι:"

                dispatcher.utter_message(message)

                for row in resa:
                    dispatcher.utter_message(f"{row[0]}  {row[1]}ο εξάμηνο")

                cursor.close()
                return[]
            else:
                dispatcher.utter_message("Συγγνωμη δεν κατάλαβα τι εννοείς,μπορείς να επαναλάβεις την ερώτηση;")
        db.close()
        return[]


class Kathigites_Epikoinonia(Action):
    def name(self) -> Text:
        return "action_prof_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        professor=tracker.get_slot("prof")
        user_message=tracker.latest_message.get("text")
        user=user_message.split()

        best_match_thl=process.extractOne('τηλέφωνο',user)
        mail_list=["mail","email","μειλ","μαιλ"]
        max_val=0
        for mail in mail_list:
            best_match_mail=process.extractOne(mail,user)
            if best_match_mail[1]>max_val:
                max_val=best_match_mail[1]
        db = mysql.connector.connect(**config_db)

        cursor=db.cursor()
        qp="select Prof_name from Professor"
        cursor.execute(qp)
        pr=cursor.fetchall()
        prof_list=[row[0] for row in pr]
        cursor.close()
        if professor in prof_list:
            pass
        elif professor is not None:
            best_match_prof=process.extractOne(professor,prof_list)
            if best_match_prof[1]>=65:
                professor=best_match_prof[0]
            else:
                professor=None
        else:
            professor=None

        if professor is not None:

            if (best_match_thl[1]>60  and max_val>60) or (best_match_thl[1]<60  and max_val<60) :

                cursor=db.cursor()
                q="select Phone,email from Professor where Prof_name=%s"
                try:
                    cursor.execute(q,(professor,))
                    res=cursor.fetchall()
                    if professor.endswith("α"):
                        message = f"Το τηλέφωνο και το mail που έχει η καθηγήτρια {professor} είναι:"

                    else:
                        message = f"Το τηλέφωνο και το mail που έχει ο καθηγητής {professor} είναι:"
                    dispatcher.utter_message(message)
                    dispatcher.utter_message(res[0][0])
                    dispatcher.utter_message(res[0][1])

                    cursor.close()
                except:
                    dispatcher.utter_message("Ουπς,κάτι πήγε στραβά!!!")
            elif best_match_thl[1]>60  and max_val<=60:
                cursor=db.cursor()
                q="select Phone from Professor where Prof_name=%s"
                try:
                    cursor.execute(q,(professor,))
                    res=cursor.fetchall()
                    if professor.endswith("α"):
                        message = f"Το τηλέφωνο  που έχει η καθηγήτρια {professor} είναι:"

                    else:
                        message = f"Το τηλέφωνο  που έχει ο καθηγητής {professor} είναι:"
                    dispatcher.utter_message(message)
                    dispatcher.utter_message(res[0][0])
                    cursor.close()
                except:
                    dispatcher.utter_message("Ουπς,κάτι πήγε στραβά!!!")
            elif best_match_thl[1]<=60  and max_val>60:
                cursor=db.cursor()
                q="select email from Professor where Prof_name=%s"
                try:
                    cursor.execute(q,(professor,))
                    res=cursor.fetchall()
                    if professor.endswith("α"):
                        message = f"Το mail  που έχει η καθηγήτρια {professor} είναι:"

                    else:
                        message = f"Το mail  που έχει ο καθηγητής {professor} είναι:"
                    dispatcher.utter_message(message)
                    dispatcher.utter_message(res[0][0])
                    cursor.close()
                except:
                    dispatcher.utter_message("Ουπς,κάτι πήγε στραβά!!!")
            else:
                dispatcher.utter_message("Δεν σε κατάλαβα μπορείς να επαναδιατυπώσεις την ερώτηση ή να δεις τις επιλογές σου πατώντας ΜΕΝΟΥ!!!")
        else:
            dispatcher.utter_message("Δεν κατάλαβα το όνομα του καθηγητή μπορείς να επαναλάβεις την ερώτηση;")
        db.close()
        return[]




class ECTS_Per_Course(Action):
    def name(self) -> Text:
        return "action_ects_per_course"

    def get_course_list(self, cursor):
        query = 'SELECT Course_name FROM Courses'
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def get_ects_for_course(self, course, cursor):
        query = 'SELECT ects FROM Courses WHERE Course_name=%s'
        cursor.execute(query, (course,))
        result = cursor.fetchone()
        return result[0] if result else None

    def lab_y_n(self,course,cursor):
        query = 'SELECT Lab FROM Courses WHERE Course_name=%s'
        cursor.execute(query, (course,))
        result = cursor.fetchone()
        return result[0] if result else None

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        course = tracker.get_slot("course")
        dm=tracker.get_slot("ects")

        with mysql.connector.connect(**config_db) as db:
            with db.cursor() as cursor:
                course_list = self.get_course_list(cursor)

                if course:
                    if course in course_list:
                        ects = self.get_ects_for_course(course, cursor)
                        if ects:
                            message = f"Το μάθημα {course} έχει {ects} ects"
                        else:
                            message = "Δεν βρεθηκαν ECTS για το μάθημα."
                        dispatcher.utter_message(message)
                    else:
                        best_match_course = process.extractOne(course, course_list)
                        if best_match_course[1] > 65:
                            course = best_match_course[0]
                            ects = self.get_ects_for_course(course, cursor)
                            if ects:
                                dispatcher.utter_message(f"Το μάθημα {course} έχει {ects} ects")
                                lab = self.lab_y_n(course,cursor)
                                if lab=="Ν":
                                    dispatcher.utter_message(f"Το μάθημα αυτό συνοδεύεται από εργαστήριο")
                                else:
                                    dispatcher.utter_message(f"Το μάθημα αυτό δεν έχει εργαστήριο")
                            else:
                                dispatcher.utter_message("No ECTS data found for the course.")
                        else:
                            dispatcher.utter_message("Συγγνωμη δεν κατάλαβα ποιο μάθημα εννοείς.")
                else:
                    user_message = tracker.latest_message.get('text', '')
                    best_match = process.extractOne(user_message, course_list)
                    if best_match[1] > 60:
                        course = best_match[0]
                        ects = self.get_ects_for_course(course, cursor)
                        if ects:
                            dispatcher.utter_message(f"Το μάθημα {course} έχει {ects} ects")
                            lab = self.lab_y_n(course,cursor)
                            if lab=="Ν":
                                dispatcher.utter_message(f"Το μάθημα συνοδεύεται από εργαστήριο")
                            else:
                                dispatcher.utter_message(f"Το μάθημα αυτο δεν έχει εργαστήριο")

                        else:
                            dispatcher.utter_message("No ECTS data found for the course.")
                    else:
                        dispatcher.utter_message("Συγγνωμη δεν κατάλαβα ποιο μάθημα εννοείς.")

        return []

class Kanonismos_Spoudon(Action):
    def name(self) -> Text:
        return "action_kanonismos_spoudon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return[]

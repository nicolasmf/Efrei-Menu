from typing import List
import requests
from Subject import Subject
from Grade import Grade
import json


class Wrapper:

    request: dict = {}

    def __init__(self) -> None:
        self.request = self.make_request()

    def change_semester(self, semester_number):

        with open("variables.json", "r+") as semester:
            data = json.load(semester)
            temp_semester_number = data["semester"]
            data["semester"] = semester_number

            semester.seek(0)
            json.dump(data, semester)
            semester.truncate()

        if self.make_request() == {}:
            with open("variables.json", "r+") as semester:
                data = json.load(semester)
                data["semester"] = temp_semester_number

                semester.seek(0)
                json.dump(data, semester)
                semester.truncate()

            print("Erreur, le numéro de semestre n'est pas valide")
            return

        self.request = self.make_request()

        print("Semestre changé !")

    def make_request(self) -> dict:
        with open("variables.json", "r") as cookie:

            cookie.seek(0)

            data = json.load(cookie)
            myefrei_sid = data["myefrei.sid"]
            semester_number = data["semester"]

            if myefrei_sid == "":
                self.get_cookie()
                return self.make_request()

        HEADERS = {
            "Host": "www.myefrei.fr",
            "Cookie": "myefrei.sid=" + myefrei_sid,
        }
        try:
            re = requests.get(
                f"https://myefrei.fr/api/extranet/student/queries/student-courses-semester?semester=S{semester_number}&year=*",
                headers=HEADERS,
            )

            return re.json()

        except requests.exceptions.TooManyRedirects:
            self.get_cookie()
            self.make_request()

    def get_cookie(self) -> str:
        from get_cookie import myefrei_sid

        with open("variables.json", "r+") as cookie:
            data = json.load(cookie)

            data["myefrei.sid"] = myefrei_sid

            cookie.seek(0)  # rewind
            json.dump(data, cookie)
            cookie.truncate()

    def get_subjects(self) -> List[str]:

        json_dict = self.request

        subjects = []
        for i in range(json_dict["totalRowCount"]):
            if json_dict["rows"][i]["soffServiceGrpId"] == "MODULE":
                subjects.append(json_dict["rows"][i]["soffOfferingDesc"])

        return subjects

    def get_subjects_info(self) -> List[Subject]:

        subjects = self.get_subjects()

        results = []

        for subject in subjects:
            grades = []
            for i in range(self.request["totalRowCount"]):
                if subject == self.request["rows"][i]["soffOfferingDesc"]:
                    if (
                        self.request["rows"][i]["custExamination"] != ""
                    ):  # Nom de la matière uniquement
                        grades.append(
                            Grade(
                                self.request["rows"][i]["custExamination"],
                                f"{float(self.request['rows'][i]['soffCredits']):.1f}",
                                self.request["rows"][i]["custMarkCode"],
                            )
                        )

                    else:
                        mean = self.request["rows"][i]["custMarkCode"]

            new_subject = Subject(subject, mean, grades)

            results.append(new_subject)

        return results

    def print_subjects_info(self) -> None:

        subjects = self.get_subjects_info()

        for subject in subjects:

            print(subject.name, ":", "", end="")

            for i in range(len(subject.grades)):
                print(subject.grades[i].type_, f"({subject.grades[i].coeff})", end=" ")
            print()

    def print_subjects_grades(self) -> None:

        subjects = self.get_subjects_info()

        for subject in subjects:

            print(subject.name, subject.mean if subject.mean != "" else "...")

            for grade in subject.grades:
                print(
                    " " * 3 + grade.type_,
                    grade.coeff,
                    grade.grade if grade.grade != "" else "...",
                )
            print()

    def save_credentials(self) -> None:
        with open("variables.json", "r+") as credentials:
            data = json.load(credentials)

            data["username"] = input("Entrez votre numéro étudiant : ")
            data["password"] = input("Entrez votre mot de passe : ")

            credentials.seek(0)

            json.dump(data, credentials)
            credentials.truncate()

            print("Identifiants sauvegardés dans variables.json")


wrapper = Wrapper()

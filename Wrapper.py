from typing import List
import requests
from Subject import Subject
from Grade import Grade
from Course import Course
import json
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font


class Wrapper:

    request: dict = {}

    def __init__(self) -> None:
        self.request = self.make_request_subjects()

    def change_semester(self, semester_number):

        with open("variables.json", "r+") as semester:
            data = json.load(semester)
            temp_semester_number = data["semester"]
            data["semester"] = semester_number

            semester.seek(0)
            json.dump(data, semester)
            semester.truncate()

        if self.make_request_subjects() == {}:
            with open("variables.json", "r+") as semester:
                data = json.load(semester)
                data["semester"] = temp_semester_number

                semester.seek(0)
                json.dump(data, semester)
                semester.truncate()

            print("Erreur, le numéro de semestre n'est pas valide")
            return

        self.request = self.make_request_subjects()

        print("Semestre changé !")

    def make_request_subjects(self) -> dict:
        with open("variables.json", "r") as cookie:

            cookie.seek(0)

            data = json.load(cookie)
            myefrei_sid = data["myefrei.sid"]
            semester_number = data["semester"]

            if myefrei_sid == "":
                self.get_cookie()
                return self.make_request_subjects()

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
            return self.make_request_subjects()

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

            if new_subject not in results:
                results.append(new_subject)

        return results

    def print_subjects_info(self) -> None:

        subjects = self.get_subjects_info()

        for subject in subjects:

            if len(subject.grades) == 0:
                print(subject.name, "", end="")
            else:
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

    def get_course_week(self) -> List[Course]:

        today_date = (
            f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        )
        today_date_raw = datetime.strptime(today_date, "%Y-%m-%d")

        week_start_raw = today_date_raw - timedelta(days=today_date_raw.weekday())
        week_end_raw = week_start_raw + timedelta(days=6)

        week_start = week_start_raw.strftime("%Y-%m-%d")
        week_end = week_end_raw.strftime("%Y-%m-%d")

        with open("variables.json", "r") as cookie:

            data = json.load(cookie)
            myefrei_sid = data["myefrei.sid"]

        HEADERS = {
            "Host": "www.myefrei.fr",
            "Cookie": "myefrei.sid=" + myefrei_sid,
        }

        re = requests.get(
            f"https://www.myefrei.fr/api/extranet/student/queries/planning?enddate={week_end}&startdate={week_start}",
            headers=HEADERS,
        )

        list_of_courses = []

        for course in re.json()["rows"]:

            course_start = course["timeCrTimeFrom"].zfill(4)
            start = f"{course_start[0:2]}:{course_start[2:4]}"

            course_end = course["timeCrTimeTo"].zfill(4)
            end = f"{course_end[0:2]}:{course_end[2:4]}"

            course_room = course["srvTimeCrDelRoom"].split(",")

            if course_room[-1] == "VISIO":
                room = "VISIO"
            else:
                room = f"{course_room[0]} Bat. {course_room[1]} {course_room[2]}"

            list_of_courses.append(
                Course(
                    course["prgoOfferingDesc"],
                    course["srvTimeCrDateFrom"][0:10],
                    start,
                    end,
                    course["tchResName"],
                    room,
                    course["valDescription"],
                )
            )

        return list_of_courses

    def print_course_week(self) -> None:

        list_of_courses = self.get_course_week()

        first_date = list_of_courses[0].date

        print(f"\n{list_of_courses[0].date[-2:]}/{list_of_courses[0].date[5:7]}")

        for course in list_of_courses:
            if course.date != first_date:
                print("\n----------")
                print(f"\n{course.date[-2:]}/{course.date[5:7]}")

            first_date = course.date

            print(
                f"""
{course.start}-{course.end}
{course.name} ({course.description})
{course.room} - {course.teacher}"""
            )

    def generate_excel(self) -> None:

        print("Génération du fichier Excel...")

        subjects = self.get_subjects_info()
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Notes"
        worksheet.append(["Subject", "Mean", "Type", "Coeff", "Grade"])

        top_cell = worksheet["A1:E1"]

        for i in top_cell[0]:
            i.font = Font(bold=True)

        for subject in subjects:
            worksheet.append([subject.name, subject.mean])
            for grade in subject.grades:
                worksheet.append(["", "", grade.type_, grade.coeff, grade.grade])
            worksheet.append([])

        worksheet.column_dimensions["A"].width = (
            len(max(subjects, key=lambda x: len(x.name)).name) - 2
        )

        with open("variables.json", "r") as file:
            data = json.load(file)
            semester = data["semester"]

            workbook.save(f"notes-S{semester}.xlsx")

            print(f"Fichier Excel généré sous le nom notes-S{semester}.xlsx")

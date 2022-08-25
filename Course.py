from dataclasses import dataclass


@dataclass
class Course:
    name: str  # prgoOfferingDesc
    date: str  # srvTimeCrDateFrom
    start: str  # timeCrTimeFrom
    end: str  # timeCrTimeTo
    teacher: str  # tchResName
    room: str  # srvTimeCrDelRoom
    description: str  # valDescription

from .attendance_schema import AttendanceCreate, AttendanceOut, AttendanceQuery, FraudResponse
from .user_schema import UserCreate, UserOut, Token, TokenData
from .class_schema import SubjectCreate, SubjectOut, ClassCreate, ClassOut, ClassWithSubject

__all__ = [
    "AttendanceCreate",
    "AttendanceOut",
    "AttendanceQuery",
    "FraudResponse",
    "UserCreate",
    "UserOut",
    "Token",
    "TokenData",
    "SubjectCreate",
    "SubjectOut",
    "ClassCreate",
    "ClassOut",
    "ClassWithSubject",
]

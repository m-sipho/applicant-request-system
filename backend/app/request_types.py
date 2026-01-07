from enum import Enum

class RequestType(str, Enum):
    REMARKING_SCRIPT = "REMARKING SCRIPT"
    AEGROTAT_SPECIAL_EXAM = "AEGROTAT/SPECIAL EXAM"
    REFUND_REQUEST = "REFUND REQUEST"



REQUEST_TYPE_RULES = {
    RequestType.REMARKING_SCRIPT: {
        "required": {
            "student_number": str,
            "module_code": str,
        }
    },
    RequestType.AEGROTAT_SPECIAL_EXAM: {
        "required": {
            "student_number": str,
            "module_code": str
        }
    },
    RequestType.REFUND_REQUEST: {
        "required": {
            "student_number": str
        }
    }
}

def http_400_duplicate_bad_application_details() -> str:
    return f"Application already exists"


def http_400_email_details(email: str) -> str:
    return f"The email {email} is already registered!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed! Email already in use"


def http_400_sigin_credentials_details() -> str:
    return "Signin failed! Recheck all your credentials!"


def http_401_unauthorized_details() -> str:
    return "Unauthorized"


def http_403_forbidden_details() -> str:
    return "Refused access to the requested resource!"


def http_404_id_details(id: int) -> str:
    return f"Either the account with id `{id}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_search_query_details(search_query: str) -> str:
    return f"Either the account with search_query `{search_query}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_email_details(email: str) -> str:
    return f"Either the account with email `{email}` doesn't exist, has been deleted, or you are not authorized!"

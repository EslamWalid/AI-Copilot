import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_core.tools import tool
from App.utils.logger import get_logger

logger = get_logger(__name__)

SCOPES = ['https://www.googleapis.com/auth/forms.body']


def get_forms_service():
    """Google Forms API Authentication"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    logger.info("google form authentication Done")

    return build('forms', 'v1', credentials=creds)


def create_new_form(service, title):
    """Create a new Google Form using ONLY the title."""
    # FIX: Google Forms API only accepts `info.title` during creation.
    new_form = {'info': {'title': title}}

    created_form = service.forms().create(body=new_form).execute()
    logger.info("google form has been created")

    return created_form['formId']


def build_google_forms_payload(custom_questions, form_description=None):
    requests = []

    # 1. Update form description if provided
    if form_description:
        requests.append({
            "updateFormInfo": {
                "info": {
                    "description": form_description
                },
                "updateMask": "description"
            }
        })

    # 2. Build item creation requests
    for index, raw_q in enumerate(custom_questions):
        # Normalize Pydantic model / Dict format
        if hasattr(raw_q, "model_dump"):
            q = raw_q.model_dump()
        elif hasattr(raw_q, "dict"):
            q = raw_q.dict()
        elif isinstance(raw_q, dict):
            q = raw_q
        else:
            q = getattr(raw_q, "__dict__", raw_q)

        item = {"title": q.get("title", "")}

        if q.get("description"):
            item["description"] = q["description"]

        # Unwrap Enum value to string
        q_type = q.get("question_type")
        if hasattr(q_type, "value"):
            q_type = q_type.value
        elif isinstance(q_type, str):
            q_type = q_type.upper()

        # Handle Multiple Choice & Checkboxes
        if q_type in ["MULTIPLE_CHOICE", "CHECKBOXES", "CHECKBOX"]:
            choice_type = "CHECKBOX" if q_type in ["CHECKBOXES", "CHECKBOX"] else "RADIO"
            item["questionItem"] = {
                "question": {
                    "required": q.get("required", False),
                    "choiceQuestion": {
                        "type": choice_type,
                        "options": [{"value": str(opt)} for opt in (q.get("options") or [])]
                    }
                }
            }

        # Handle Short Answer & Paragraph
        elif q_type in ["SHORT_ANSWER", "PARAGRAPH"]:
            item["questionItem"] = {
                "question": {
                    "required": q.get("required", False),
                    "textQuestion": {
                        "paragraph": True if q_type == "PARAGRAPH" else False
                    }
                }
            }

        # Handle Rating Scale
        elif q_type == "SCALE":
            item["questionItem"] = {
                "question": {
                    "required": q.get("required", False),
                    "scaleQuestion": {
                        "low": q.get("scale_min") or 1,
                        "high": q.get("scale_max") or 5
                    }
                }
            }

        # Safety Fallback: Default unrecognized types to Short Text
        else:
            item["questionItem"] = {
                "question": {
                    "required": q.get("required", False),
                    "textQuestion": {
                        "paragraph": False
                    }
                }
            }

        requests.append({
            "createItem": {
                "item": item,
                "location": {"index": index}
            }
        })

    return {"requests": requests}


def add_questions_to_form(service, form_id, questions_payload):
    response = (
        service.forms()
        .batchUpdate(formId=form_id, body=questions_payload)
        .execute()
    )

    logger.info("all questions and metadata have been updated")
    return response


def create_google_form_tool(form_title, form_description, payload):
    """Tool used to create a Google Form with questions."""
    service = get_forms_service()

    # Pass only form_title to create_new_form
    form_id = create_new_form(service, form_title)
    
    # Include description inside batchUpdate payload creation
    batch_payload = build_google_forms_payload(payload, form_description=form_description)
    
    add_questions_to_form(service, form_id, batch_payload)

    form_url = f"https://docs.google.com/forms/d/{form_id}/edit"
    logger.info(f"google form created : {form_url}")

    return {"Form": form_url}
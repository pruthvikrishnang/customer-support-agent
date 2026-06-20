# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import google.auth
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

from google.genai import Client
from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.agents.context import Context
from google.adk.apps import App
from google.adk.events.event import Event
from google.adk.models import Gemini
from google.adk.workflow import Workflow, START

try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    pass

os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

if os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
else:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

model_name = "gemini-flash-latest"

model = Gemini(
    model=model_name,
    retry_options=types.HttpRetryOptions(attempts=3),
)


class Classification(BaseModel):
    is_shipping_related: bool = Field(
        description="True if the user's query is about shipping (rates, tracking, delivery, returns, or shipping policy). False otherwise."
    )


def classifier(node_input: types.Content) -> Event:
    user_query = ""
    if node_input and node_input.parts:
        user_query = node_input.parts[0].text or ""

    client = Client()
    response = client.models.generate_content(
        model=model_name,
        contents=user_query,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Classification,
            system_instruction="Classify if the user query is related to shipping (rates, tracking, delivery, returns, shipping policy) or unrelated.",
        ),
    )

    try:
        data = json.loads(response.text)
        is_shipping = data.get("is_shipping_related", False)
    except Exception:
        is_shipping = False

    return Event(
        output={"is_shipping_related": is_shipping},
        state={"classification": {"is_shipping_related": is_shipping}},  # type: ignore
    )


def router(node_input: dict) -> Event:
    is_shipping = node_input.get("is_shipping_related", False)
    if is_shipping:
        return Event(route="shipping")  # type: ignore
    return Event(route="unrelated")  # type: ignore


shipping_faq_agent = LlmAgent(
    name="shipping_faq_agent",
    model=model,
    instruction="""You are a super playful and enthusiastic customer support agent for a shipping company! 🚀📦
Answer the user's shipping query with high energy, clarity, and lots of helpful emojis! 🎉
If the user asks about shipping rates, be sure to enthusiastically highlight our amazing FREE shipping threshold: Free shipping on all orders over $50! 🥳💰
If you do not know the answer, politely and cheerfully let the customer know.""",
)


def decline_node(ctx: Context) -> Event:
    decline_text = "I apologize, but I can only assist with shipping-related queries (such as rates, tracking, delivery, and returns). How can I help you with your shipping needs today?"
    return Event(
        content=types.Content(
            role="model", parts=[types.Part.from_text(text=decline_text)]
        ),
        output=decline_text,
    )


root_agent = Workflow(
    name="customer_support_workflow",
    edges=[
        (START, classifier),
        (classifier, router),
        (router, {"shipping": shipping_faq_agent, "unrelated": decline_node}),
    ],
    description="Routes customer support queries to either shipping FAQ or declines them if unrelated.",
)

app = App(
    root_agent=root_agent,
    name="app",
)

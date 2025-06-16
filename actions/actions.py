from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai
import os
import psycopg2 # For database connection (example)

# Configure OpenAI API key
openai.api_key = os.getenv("your_openai_api_key_here")

class ActionLookupOrderStatus(Action):
    def name(self) -> Text:
        return "action_lookup_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_number = tracker.get_slot("order_number")
        if order_number:
            try:
                # Example database connection (replace with your actual DB logic)
                conn = psycopg2.connect(
                    host="localhost",
                    database="database name",
                    user="username",
                    password="pwd"
                )
                cur = conn.cursor()
                cur.execute(f"SELECT status FROM orders WHERE order_id = '{order_number}'")
                result = cur.fetchone()
                cur.close()
                conn.close()

                if result:
                    status = result[0]
                    dispatcher.utter_message(text=f"The status for order {order_number} is: {status}.")
                else:
                    dispatcher.utter_message(text=f"Could not find order {order_number}. Please double-check.")
            except Exception as e:
                print(f"Database error: {e}")
                dispatcher.utter_message(text="Sorry, I'm having trouble looking up your order right now.")
        else:
            dispatcher.utter_message(text="I need an order number to look up the status.")
        return []

class ActionFallbackWithGPT(Action):
    def name(self) -> Text:
        return "action_fallback_with_gpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        print(f"Falling back to GPT for message: '{user_message}'")

        try:
            # Integrate with GPT-3.5
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            gpt_response = response.choices[0].message.content.strip()
            dispatcher.utter_message(text=gpt_response)
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            dispatcher.utter_message(text="I'm sorry, I couldn't understand that. Could you please rephrase or try a different query?")
        return []

class ActionEscalateIssueToCRM(Action):
    def name(self) -> Text:
        return "action_escalate_issue_to_crm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I've escalated your issue to our support team. A human agent will contact you shortly.")
        # Here, you would integrate with your CRM system (e.g., Salesforce, Zendesk API)
        # Example: Create a new ticket with user's query
        print(f"Issue escalated: User message: '{tracker.latest_message.get('text')}'")
        return []
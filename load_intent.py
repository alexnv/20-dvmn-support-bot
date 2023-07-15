import argparse
import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(intent_name, intent_value, project_id):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in intent_value['questions']:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    message_texts = [intent_value['answer']]
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=intent_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    load_dotenv()
    dialogflow_project_id = os.environ["PROJECT_ID"]

    parser = argparse.ArgumentParser()
    parser.add_argument('--p', default='questions.json', help='Path to json file')

    args = parser.parse_args()
    path = args.p

    with open(path, "r", encoding="utf-8") as questions_file:
        questions = json.load(questions_file)

    for intent_name, intent_value in questions.items():
        create_intent(intent_name, intent_value, dialogflow_project_id)


if __name__ == '__main__':
    main()

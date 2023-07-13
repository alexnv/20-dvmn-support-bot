import json

def create_intent(intent_name, intent_value, project_id, ):
    from google.cloud import dialogflow
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
    with open("questions.json", "r", encoding="utf-8") as questions_file:
        questions = json.load(questions_file)

    for intent_name, intent_value in questions.items():
        create_intent(intent_name, intent_value, "devman-support-bot-392412")


if __name__ == '__main__':
    main()
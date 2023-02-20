import os
from dotenv import load_dotenv
import openai
import telebot

load_dotenv("env/.env")

openai.api_key = os.getenv("OPENAI_API_KEY")
telebot_api_key = os.getenv("TELEBOT_API_KEY")

bot = telebot.TeleBot(telebot_api_key)

previous_questions = []

@bot.message_handler(func=lambda _: True)
def handle_message(msg):
	# print(msg)
	# print(msg.text)
	
	global previous_questions

	new_question = f"You: {msg.text}.\nFriend:"

	if len(previous_questions) == 0:
		question = new_question
	elif len(previous_questions) == 1:
		question = f"{previous_questions[0]}\n{new_question}"
	elif len(previous_questions) == 2:
		question = f"{previous_questions.pop(0)}\n{previous_questions[0]}\n{new_question}"

	response = openai.Completion.create(
		model="text-davinci-003",
		# prompt="You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend:",
		# prompt="what is python?",
		prompt=question,
		temperature=0.5,
		max_tokens=1000,
		top_p=1.0,
		frequency_penalty=0.5,
		presence_penalty=0.0,
		stop=["You:"]
	)
	res = response["choices"][0]["text"]

	previous_questions.append(f"{new_question} {res}.")
	
	print(previous_questions)

	bot.send_message(chat_id=msg.from_user.id, text=res)

bot.polling()



# response = openai.Completion.create(
#   model="text-davinci-003",
# #   prompt="You: What have you been up to?\nFriend: Watching old movies.\nYou: Did you watch anything interesting?\nFriend:",
# #   prompt="what is python?",
#   prompt="что такое python?",
#   temperature=0.5,
#   max_tokens=1000,
#   top_p=1.0,
#   frequency_penalty=0.5,
#   presence_penalty=0.0,
# #   stop=["You:"]
# )

# print(len(response["choices"]))
# print(response["choices"][0]["text"])
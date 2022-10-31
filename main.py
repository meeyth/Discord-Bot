import discord
from dotenv import load_dotenv, find_dotenv
import os
import requests

load_dotenv(find_dotenv())

intents = discord.Intents.all()

client = discord.Client(intents=intents)


def calculate_bmi(height, weight):
    """Underweight = <18.5
        Normal weight = 18.5–24.9
        Overweight = 25–29.9
        Obesity = BMI of 30 or greater"""

    weight_in_pounds = weight * 2.20462262185
    feet, inches = height
    height_in_inches = feet * 12 + inches

    bmi = weight_in_pounds / height_in_inches**2 * 703
    if bmi < 18.5:
        status = "Underweight!"
    elif bmi >= 18.5 and bmi <= 24.9:
        status = "Normal weight"
    elif bmi >= 25 and bmi <= 29.9:
        status = "Overweight!"
    else:
        status = "Obesity!!!"

    return bmi, status


def get_weather(city):
    API_KEY = os.getenv('API_KEY')
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    request_url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['main']
        temp = weather['temp']
        humidity = weather['humidity']
        sky = data['weather'][0]['description']
        wind_speed = data['wind']['speed']

        return f""" 
                Tempreture: {round(temp-273.15,3)} °C
Humidity: {humidity} %
Sky: {sky}
Wind speed: {wind_speed} km/h"""

    else:
        return "No Such Location!!"


def get_quote():
    res = requests.get('https://zenquotes.io/api/random')
    data = res.json()
    quote = data[0]['q'] + ' -' + data[0]['a']
    return quote


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}.')


@client.event
async def on_member_join(member):
    await member.send(
        f'Welcome to the server, {member.mention}! Enjoy your stay here.'
    )


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if message.content.startswith('$help'):
            help_message = """
            >>USE THIS FORMATS TO HAVE A RESPONSE<<
            $inspire > To read a random inspirational  quote.
            $weather in Location > To check weather of any location.
            $calculate bmi feet:inches:kgs > To know your Body Mass Index. An example input $calculate bmi 5:7:54.
            """
            await message.channel.send(help_message)

        if message.content.startswith('$inspire'):
            await message.channel.send(f"#general")
            await message.channel.send(f"`{get_quote()}`")

        if message.content.startswith('$weather in'):
            city = message.content.split()[-1]
            await message.channel.send(get_weather(city=city))

        if message.content.startswith('$calculate bmi'):
            data = message.content.split()[-1]
            feet, inches, weight = data.split(':')
            feet, inches, weight = float(feet), float(inches), float(weight)
            bmi = calculate_bmi((feet, inches), weight)
            round_off_bmi = round(bmi[0], 2)
            status = bmi[1]
            await message.channel.send(f'Your BMI is {round_off_bmi} ({status})')

    except Exception as e:
        print(e)


if __name__ == "__main__":
    client.run(os.getenv('TOKEN'))

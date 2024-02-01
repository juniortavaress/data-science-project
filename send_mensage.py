import smtplib
import pandas as pd
import email.message

from datetime import datetime

class OrderSuggestions:
    def __init__(self):
        self.getPizzas()
        self.getClient()

    # Loading the datas
    def getPizzas(self):
        self.df_pizzas = pd.read_csv('client_suggestions.csv', sep=';')
        print(self.df_pizzas)

    # Obtaining information about customers and suggested flavors
    def getClient(self):
        date = datetime.now().weekday()
        days_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        day = days_of_week[date]
        print(day)

        self.df_day_pizzas = self.df_pizzas[self.df_pizzas["Day"] == day]
        print(self.df_day_pizzas)

        # for index, client in self.df_day_pizzas.iterrows():
        for index, client in self.df_day_pizzas.iloc[0:3].iterrows():    # To test, only sends to three customerts
            contact = client["Number"]
            flavor = client['Flavor'].replace("'", "").strip("[]").split(",")
            EmailSender.sendEmail(self, contact, flavor)

    def sendEmail(self, contact, flavor):  
        mensage = f"""
        <p><b>Hello from NY Pizzeria!</b></p>
        <p>We have a special pizza offer just for you tonight. Here are some flavor suggestions we think you'll enjoy...</p>
        <p style="margin-left: 20px;">🍕 {flavor[0]}</p>
        <p style="margin-left: 20px;">🍕 {flavor[1]}</p>
        <p style="margin-left: 20px;">🍕 {flavor[2]}</p>
        <p style="margin-left: 20px;">🍕 {flavor[3]}</p>
        <p style="margin-left: 20px;">🍕 {flavor[4]}</p>
        <p>And remember, on purchases over <b>$20</b>, you'll receive a complimentary dessert pizza!</p>
        <p>But hurry, this promotion is valid only for <b>today</b>, for orders placed until <b>9 PM</b>.</p>
        """

        msg = email.message.Message()
        msg['Subject'] = "Check out these pizzas - Pizzeria NY"
        msg['From'] = 'sciencedataproject@gmail.com'
        msg['To'] = f'{contact}@gmail.com'
        password = 'ynvbtngtnfbxtkqm' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(mensage)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email sent')

if __name__ == "__main__":
    OrderSuggestions()
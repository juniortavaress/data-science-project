# Importing libraries
import random 
import pandas as pd
import mysql.connector

class SuggestionAnalyzer:
    def __init__(self, list):
        self.listClient = list
        self.getDataFrame()     # Loading datas        
        self.clientsLoop()

    def getDataFrame(self):
        # Creating connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='SenhaMySQL2024',
            database='dataproject')

        cursor = connection.cursor()

        # Querying the datas
        query = 'SELECT * FROM pizzas_suggestions;'

        cursor.execute(query)
        result = cursor.fetchall()  

        # columns = [i[0] for i in cursor.description], get the name of the columns
        self.df = pd.DataFrame(result, columns = [i[0] for i in cursor.description])

        print(self.df)

    def createClientData(self, client_ID):
        self.df_client = self.df.loc[self.df['Client_ID'] == client_ID]
        self.df_client = self.df_client.reset_index(drop=True)
        return self.df_client

    def createIngredientsData(self):
        # Creating a DataFrame of flavors
        self.df_ingredients = self.df.drop(['id', 'Client_ID', 'Phone_Number', 'Day'], axis=1)
        self.df_ingredients = self.df_ingredients.drop_duplicates()
        self.df_ingredients = self.df_ingredients.reset_index(drop=True)
        print('ee', self.df_ingredients)
        return self.df_ingredients

    def clientIngredients(self):
        # value_counts(), count occurrences of each element
        # head(4), returns the first 4 elements of a series or DataFrame column
        # index, returnsthe indices of the series, without the output being the line number 
        # tolist(), converts the indices into a list

        # Create lists with the most chosen ingredients.
        self.first_ingredient = self.df_client['First_Ingredient'].value_counts()
        self.first_ingredient = self.first_ingredient.head(4).index.tolist()

        self.second_ingredient = self.df_client['Second_Ingredient'].value_counts()
        self.second_ingredient = self.second_ingredient.head(4).index.tolist()

        # Set removes any duplicate
        self.ingredients = list(set( self.first_ingredient +  self.second_ingredient))
        return self.ingredients


    def getSuggestion(self):
        suggestions = []
        list_columns = ['First_Ingredient', 'Second_Ingredient']

        # Get index
        for ingredient in self.ingredients:
            for i in list_columns:
                indices = self.df_ingredients[self.df_ingredients[i] == ingredient].index.tolist()
                suggestions.extend(indices)
        suggestions = sorted(set(suggestions))

        # Get flavors
        suggestions_flavor = []
        for index in suggestions:
            suggestions_flavor.append(self.df_ingredients['Pizza_Name'][index])
        self.suggestions_flavor = random.sample(suggestions_flavor, 5)
        return self.suggestions_flavor

    def clientsLoop(self):
        SuggestionAnalyzer.createIngredientsData(self)
        self.client_suggestions = pd.DataFrame(columns = ['ID', 'Number', 'Day','Flavor'])

        for client in self.df['Client_ID'].unique():
        # for client in self.listClient:
            df_client = SuggestionAnalyzer.createClientData(self, client)
            print(df_client)
            clientName = df_client['Client_ID'][0]
            clientNumber = df_client['Phone_Number'][0]
            ingredients = SuggestionAnalyzer.clientIngredients(self)
            clientFlavors = SuggestionAnalyzer.getSuggestion(self)
            day = df_client['Day'].value_counts().idxmax()
            
            # Adding a new row to the DataFrame
            new_row = {'ID': clientName, 'Number': clientNumber, 'Day': day,'Flavor': clientFlavors}
            self.client_suggestions = self.client_suggestions.append(new_row, ignore_index=True)

        self.client_suggestions.to_csv('client_suggestions.csv', sep=';', index=False)

if __name__ == "__main__":
    listClient = [1]
    SuggestionAnalyzer(listClient)
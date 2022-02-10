import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
#from scipy import stats #Pour la regression linéaire

plt.close("all")

def initialisation_df(df):
    df = pd.DataFrame(columns = ['Date','Time','Facteur_activite'])
    return df

def ajout_valeur(DF, val):
    DF2 = pd.DataFrame({'Date':[datetime.now().strftime('%d/%m/%Y')],
        'Time':[datetime.now().strftime('%H:%M:%S')],
        'Facteur_activite':[val]})
    print(DF2)
    DF = pd.concat([DF,DF2])
    #print(DF)
    return DF

def affichage_graphique(DF):
    fig, axe = plt.subplots(figsize=(10.6,8))
    x = DF['Time']
    y = DF['Facteur_activite']
    axe.plot(x, y, label='FActivite', color='#1B80EA')
    axe.set_ylabel('Facteur Activité')
    axe.set_xlabel('Horaire')
    axe.set_ylim(int(y.min()))
    axe.set_title("Courbe d'activité nocturne - nuit du {}".format(DF.iloc[0]['Date']))
    #lr = stats.linregress(_x, y) #Pour regression et calcul du nombre de cycles
    plt.show()

def enregistrement_data(DF):
    DF.to_pickle(nomfichier)

def Lecture_fichier():
    DF = pd.read_pickle(nomfichier)
    return DF

if __name__=='__main__':
    df = pd.DataFrame(columns = ['Date','Time', 'Facteur_activite'])

    for i in range(10):
        df = ajout_valeur(df, np.random.randint(1, high=100))
        time.sleep(1)
    #print(df['Date'].datetime.strftime('%H:%M:%S'))
    affichage_graphique(df)

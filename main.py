import ast
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import unidecode
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pandas as pd
import csv
import time
from PIL import ImageTk, Image

# MAIN WINDOW
window = Tk()
window.title("Reciprediskyon")
window.geometry("1920x1080")

# FOR BACKGROUND
img =Image.open('background.png')
bg = ImageTk.PhotoImage(img)

# Add image
label = Label(window, image=bg)
label.place(x = 0,y = 0)


# Comic Sans MS
home = Label(window, text = "Reciprediskyon", font = ("Purisa", 85, "bold")) # master can be a window or a frame
home.pack(pady = 100)
# home.pack()

description = Label(window, text = "A Filipino Cuisine Recipe Recommendation System", font = ("Purisa", 35, "bold")) # master can be a window or a frame
description.pack(pady = 30)

# POP UP WINDOW
def popup():
    popupwindow = Toplevel(window)
    # window.destroy() # Will just remove the home screen window
    popupwindow.title("Ingredients Checkbox")
    # popupwindow.configure(bg='Moccasin')

    img =Image.open('background.png')
    bg = ImageTk.PhotoImage(img)

    # Add image
    label = Label(popupwindow, image=bg)
    label.place(x = 0,y = 0)
        
    # popupwindow.geometry("200x100")
    # alert = Label(popupwindow, text = "Back to Home")
    # button1 = Button(popupwindow, text="OK", command=popupwindow.destroy)
    # alert.pack()
    # button1.pack()

    # get ingredients set
    with open("dataset_ingred.csv", 'r') as recipe_data:
        csv_reader = csv.reader(recipe_data, delimiter=",")
        for row in csv_reader:
            asdf = {y.lower(): 0 for y in row}
        # print(user_input)
    # parse ingredients lowercase
    ref = []
    for ing in row:
        ref.append(ing.lower())
# print(ref)
    # sort alphabetically
    ref.sort()
    user_input = dict(sorted(asdf.items(), key=lambda x: x[0].lower()))
#print(user_input)
# get recipe dataset
    df_recipes = pd.read_csv("dataset_recipe.csv")
    df_recipes['ingredients'] = df_recipes.ingredients.values.astype('U')
    tfidf = TfidfVectorizer()
    tfidf.fit(df_recipes['ingredients'])
    tfidf_recipe = tfidf.transform(df_recipes['ingredients'])
    # create models for reference
    with open("datacsv/tfidf.pkl", "wb") as f:
        pickle.dump(tfidf, f)
    with open("datacsv/tfidf_encoding.pkl", "wb") as f:
        pickle.dump(tfidf_recipe, f)

    # GUI
    f = LabelFrame(popupwindow, text="Check the ingredients you have in your kitchen!", font=("Purisa", 20, "bold"))
    end_result = LabelFrame(popupwindow, font=("Purisa", 13, "bold"))
    d_font = ("Purisa", 20, "bold")
    f.grid(row=0, columnspan=8, pady=10, padx=15, sticky=NW)
    # end_result.grid(row=2, columnspan=8, pady=10, padx=15, sticky=NW)   

    # Checkbutton for input
    i = 0
    for x in user_input:
    # def aq():
    # print(q[x].get())
    # print(q)

        user_input[x] = Variable()
        las = Checkbutton(f, text=x, variable=user_input[x],font=("Purisa", 13, "bold"))  # command=aq)
        las.deselect()
    #print(qwe[i])

        c = i % 21  # MODULO
        ca = i // 21  # DIV
        i += 1
        las.grid(row=c + 1, column=ca, sticky=NW)

    def clear():
        for x in user_input:
            user_input[x].set(0)

    # parse user-ingredients from checkbox
    def ingredient_parser_final(ingredient):
        if isinstance(ingredient, list):
            ingredients = ingredient
        else:
            ingredients = ast.literal_eval(ingredient)

        ingredients = ",".join(ingredients)
        ingredients = unidecode.unidecode(ingredients)
        return ingredients

    # get recomm function
    def get_recommendations(No, scores):
    # load in recipe dataset
        df_recipes = pd.read_csv("dataset_recipe.csv")
    # order the scores with and filter to get the highest N scores
        le = len(scores)
        r = range(le)
        print(r)
        top = sorted(r, key=lambda ix: scores[ix][0], reverse=True)[:No]
    # create dataframe to load in recommendations
        recommendation = pd.DataFrame(columns=['recipe', 'ingredients', 'score'])
        count = 0
        for i in top:
            recommendation.at[count, 'recipe'] = df_recipes['recipe_name'][i]
            recommendation.at[count, "ingredients"] = df_recipes["ingredients"][i]
            recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i][0]))
            print(scores[i][0])
            count += 1
        return recommendation

    def confirm():

        results_window = Toplevel(popupwindow)
        results_window.title("Recommended Filipino Recipes")

        img =Image.open('background.png')
        bg = ImageTk.PhotoImage(img)

        # Add image
        label = Label(results_window, image=bg)
        label.place(x = 0,y = 0)
        
        end_result = LabelFrame(results_window, font=("Purisa", 15, "bold"))
        end_result.grid(row=2, columnspan=8, pady=10, padx=10, sticky=NW)  
        for widget in end_result.winfo_children():
            widget.destroy()

        chosen_ingredients = []
        for z in ref:
            if user_input[z].get() == '1':
            #print(q[z].get())
                print(z)
                chosen_ingredients.append(z)
        print(chosen_ingredients)
    
        with open("datacsv/tfidf_encoding.pkl", 'rb') as fi:
            tfidf_encoding = pickle.load(fi)
        with open("datacsv/tfidf.pkl", "rb") as fi:
            tfidf = pickle.load(fi)
        ingredients_parsed = " ".join(chosen_ingredients)
        ingredients_tfidf = tfidf.transform([ingredients_parsed])
    # print(ingredients_tfidf)
        cos_sim = map(lambda xq: cosine_similarity(ingredients_tfidf, xq), tfidf_encoding)
        scores = list(cos_sim)
    # print(scores)
    # get recomm
        a = get_recommendations(5, scores)
    # print(a)
        n = 0

        lblhead = Label(end_result, text="Top Recipes", font=("Purisa", 20, "bold"),width=50)
        lblhead.grid(row=8, column=1, columnspan=12,padx=10, pady=5, sticky=NE)
        # tkinter show results
        while n < 5:
            lblrank = Label(end_result, text=(n+1), font=("Purisa", 15, "bold"))
            lblrank.grid(row=n +23, column=4, pady=2, padx=5, sticky=N)
            lblfinal = Label(end_result, text=a.at[n, 'recipe'], font=("Purisa", 15, "bold"))
            lblfinal.grid(row=n+23, column=6, columnspan=8, pady=2, padx=5, sticky=N)
            n += 1

        # end_result = LabelFrame(results_window, font=("Arial", 12, "bold"))
        # end_result.grid(row=2, columnspan=8, pady=10, padx=15, sticky=NW)   

        # BACK BUTTON MOTO

        def back():
            results_window.destroy()

        back_button = Button(results_window, text="Generate Again", font = ("Purisa", 12 , "bold"),  padx=10, pady=10, bg="yellow", command=back)
        back_button.grid()
        

        results_window.mainloop()


    # submit button
    btn_clear = Button(popupwindow, text ="Clear", font = ("Purisa", 12 , "bold"), activebackground="lightblue", padx=10, pady=20, bg="green", width=5, command=clear)
    btn_clear.grid(row=1, columnspan=4, pady=20, padx=25, sticky=N)

    btn_submit = Button(popupwindow, text="Show Recommendations", font = ("Purisa", 12 , "bold"),  padx=100, pady=20, bg="yellow", width=5, command=confirm)
    btn_submit.grid(row=1, columnspan=2, pady=20, padx=25, sticky=NW)
    counter = -1
    running = False

    # def counter_label(lbl):
    #     def count():
    #         if running:
    #             global counter
    #             if counter==-1:             
    #                 display="00"
    #             else:
    #                 display=str(counter)

    #             lbl['text']=display    
            
    #             lbl.after(1000, count)    
    #             counter += 1
            

    #     count()     
    
    # def StartTimer(lbl):
    #     global running
    #     running=True
    #     counter_label(lbl)
    #     start_btn['state']='disabled'
    #     stop_btn['state']='normal'
    #     reset_btn['state']='normal'

    # def StopTimer():
    #     global running
    #     start_btn['state']='normal'
    #     stop_btn['state']='disabled'
    #     reset_btn['state']='normal'
    #     running = False
    
    # def ResetTimer(lbl):
    #     global counter
    #     counter=-1
    #     if running==False:      
    #         reset_btn['state']='disabled'
    #         lbl['text']='00'
    #     else:                          
    #         lbl['text']=''

    # lbl = Label(
    #     popupwindow,
    #     text="00", 
    #     fg="black", 
    #     font="Verdana 15 bold"
    #     )

    # label_msg = Label(
    #     popupwindow, text="seconds", 
    #     fg="black", 
    #     font="Verdana 10 bold"
    #     )
    
    # lbl.place(x=650, y=565)
    # label_msg.place(x=700, y=570)

    # start_btn=Button(
    #     popupwindow, 
    #     text='Start', 
    #     width=5, 
    #     command=lambda:StartTimer(lbl)
    # )

    # stop_btn = Button(
    #     popupwindow, 
    #     text='Stop', 
    #     width=5, 
    #     state='disabled', 
    #     command=StopTimer
    # )

    # reset_btn = Button(
    #     popupwindow, 
    #     text='Reset', 
    #     width=5, 
    #     state='disabled', 
    #     command=lambda:ResetTimer(lbl)
    # )

    # start_btn.place(x=600, y=600)
    # stop_btn.place(x=700, y=600)
    # reset_btn.place(x=800, y=600)


    popupwindow.mainloop()

# Continuation of main window content
button = Button(window, text="Generate Recipe", font = ("Purisa", 20, "bold"), activebackground="green", bg="yellow", command=popup)
button.pack(pady = 10)
window.mainloop()



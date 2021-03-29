import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

# Loading a json news dataset
news_df = pd.read_json("News_Category_Dataset_v2.json", lines=True)
news_df.drop(['authors', 'link', 'date'], axis=1, inplace=True)

news_df.head()

# Let's see how many categories we have here
print(f"Total unique categories are: {len(news_df['category'].value_counts())}")
print(f"Count of occurrence of each category:")
news_df['category'].value_counts()

categories = news_df['category'].value_counts().index


def groupper(grouplist, name):
    for ele in categories:
        if ele in grouplist:
            news_df.loc[news_df['category'] == ele, 'category'] = name


groupper(grouplist=['WELLNESS', 'HEALTHY LIVING', 'HOME & LIVING', 'STYLE & BEAUTY', 'STYLE'],
         name='LIFESTYLE AND WELLNESS')

groupper(grouplist=['PARENTING', 'PARENTS', 'EDUCATION', 'COLLEGE'], name='PARENTING AND EDUCATION')

groupper(grouplist=['SPORTS', 'ENTERTAINMENT', 'COMEDY', 'WEIRD NEWS', 'ARTS'], name='SPORTS AND ENTERTAINMENT')

groupper(grouplist=['TRAVEL', 'ARTS & CULTURE', 'CULTURE & ARTS', 'FOOD & DRINK', 'TASTE'],
         name='TRAVEL-TOURISM & ART-CULTURE')

groupper(grouplist=['WOMEN', 'QUEER VOICES', 'LATINO VOICES', 'BLACK VOICES'], name='EMPOWERED VOICES')

groupper(grouplist=['BUSINESS', 'MONEY'], name='BUSINESS-MONEY')

groupper(grouplist=['THE WORLDPOST', 'WORLDPOST', 'WORLD NEWS'], name='WORLDNEWS')

groupper(grouplist=['ENVIRONMENT', 'GREEN'], name='ENVIRONMENT')

groupper(grouplist=['TECH', 'SCIENCE'], name='SCIENCE AND TECH')

groupper(grouplist=['FIFTY', 'IMPACT', 'GOOD NEWS', 'CRIME'], name='GENERAL')

groupper(grouplist=['WEDDINGS', 'DIVORCE', 'RELIGION', 'MEDIA'], name='MISC')

print("We have a total of {} categories now".format(news_df['category'].nunique()))
news_df['category'].value_counts()

# Replacing punctuation with ''
translator = str.maketrans('', '', string.punctuation)

# Mapping the categories to numbers
# news_df['CATEGORY'] = news_df.CATEGORY.map({ 'b': 1, 't': 2, 'e': 3, 'm': 4 })

# Converting all the titles into lowercase and removing punctuation
news_df['headline'] = news_df.headline.map(lambda x: x.lower().translate(translator))

news_category = news_df['category']
news_title = news_df['headline']
news_df.head()

# Separating the dataset into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(
    news_title,
    news_category,
    random_state=1
)

# Applying bag of words approach and removing stop words
# Transforming the text of the data sets to a vector of token counts
cv = CountVectorizer(stop_words='english')
training_data = cv.fit_transform(X_train)
testing_data = cv.transform(X_test)

print(training_data.shape)
print(testing_data.shape)

# Training the Naive Bayes Classifier and creating a Model
naive_bayes = MultinomialNB()

naive_bayes.fit(training_data, y_train)

predictions = naive_bayes.predict(testing_data)
print(predictions)

# The best value is 1 and the worst value is 0
print("Accuracy score: ", accuracy_score(y_test, predictions))
print("Precision score: ", precision_score(y_test, predictions, average='weighted'))
print("F1 score: ", f1_score(y_test, predictions, average='weighted'))
print("Recall score: ", recall_score(y_test, predictions, average='weighted'))


# Running the program
def run():
    a = input("Run Program: (Y/N)? ")

    if a in {'y', 'Y', 'yes', 'Yes', 'YES'}:
        calculation()
    elif a in {'n', 'N', 'no', 'No', 'NO'}:
        print("Thank You.")
    else:
        print("Please type properly.")
        run()


def calculation():
    new_headline = input("Enter News Headline: ")

    new_headline_list = [new_headline]

    # Predicting the new headline category
    count_vector = cv.transform(new_headline_list)
    check = naive_bayes.predict(count_vector)

    if check.item(0) == 'LIFESTYLE AND WELLNESS':
        print("Category: LIFESTYLE AND WELLNESS")

    elif check.item(0) == 'PARENTING AND EDUCATION':
        print("Category: PARENTING AND EDUCATION")

    elif check.item(0) == 'SPORTS AND ENTERTAINMENT':
        print("Category: SPORTS AND ENTERTAINMENT")

    elif check.item(0) == 'TRAVEL-TOURISM & ART-CULTURE':
        print("Category: TRAVEL-TOURISM & ART-CULTURE")

    elif check.item(0) == 'BUSINESS-MONEY':
        print("Category: BUSINESS-MONEY")

    elif check.item(0) == 'SCIENCE AND TECH':
        print("Category: SCIENCE AND TECH")

    elif check.item(0) == 'WORLDNEWS':
        print("Category: WORLDNEWS")

    elif check.item(0) == 'ENVIRONMENT':
        print("Category: ENVIRONMENT")

    elif check.item(0) == 'MISC':
        print("Category: MISC")

    elif check.item(0) == 'GENERAL':
        print("Category: GENERAL")

    elif check.item(0) == 'EMPOWERED VOICES':
        print("Category: EMPOWERED VOICES")

    run()


Examples_Headlines = ["EU shellfish import ban permanent, UK fishing industry told",
                      "Is the market about to crash?",
                      "Summer House's Kyle Cooke Gives Wedding Update Amid Pandemic Postponement",
                      "How do binge eating and drinking impact the liver?", ]

run()

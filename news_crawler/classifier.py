# Importing Libraries
import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

# Loading the data into a Pandas data frame
news_df = pd.read_csv("uci-news-aggregator.csv", sep=",")
news_df.head()

# Replacing punctuation with ''
translator = str.maketrans('', '', string.punctuation)

# Mapping the categories to numbers
news_df['CATEGORY'] = news_df.CATEGORY.map({'b': 1, 't': 2, 'e': 3, 'm': 4})

# Converting all the titles into lowercase and removing punctuation
news_df['TITLE'] = news_df.TITLE.map(lambda x: x.lower().translate(translator))

news_category = news_df['CATEGORY']
news_title = news_df['TITLE']
news_df.head()

news_title.head()

# Separating the dataset into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(
    news_title,
    news_category,
    random_state=1
)

# Number contained in the training, testing and total datasets
print("Training Dataset:", X_train.shape[0], "|",
      "Test Dataset:", X_test.shape[0])

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
b = 0
t = 0
e = 0
m = 0

for i in range(len(predictions)):
    if predictions.item(i) == 1:
        b = b + 1
    elif predictions.item(i) == 2:
        t = t + 1
    elif predictions.item(i) == 3:
        e = e + 1
    elif predictions.item(i) == 4:
        m = m + 1

print('Business:', b, '|', 'Science:', t, '|', 'Entertainment:', e, '|', 'Health:', m)

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

    if check.item(0) == 1:
        print("Category: Business")
    elif check.item(0) == 2:
        print("Category: Science & Technology")
    elif check.item(0) == 3:
        print("Category: Entertainment")
    elif check.item(0) == 4:
        print("Category: Health")
    run()


Examples_Headlines = ["EU shellfish import ban permanent, UK fishing industry told",
                      "Is the market about to crash?",
                      "Summer House's Kyle Cooke Gives Wedding Update Amid Pandemic Postponement",
                      "How do binge eating and drinking impact the liver?", ]

run()

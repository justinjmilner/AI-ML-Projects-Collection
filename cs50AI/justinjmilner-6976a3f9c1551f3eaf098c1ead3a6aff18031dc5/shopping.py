import csv
import sys
import numpy

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    y_test = numpy.ravel(y_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    megalist = []
    evidence = []
    labels = []

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            list1 = []
            list = []

            # Load the evidence into a list
            for i in range(17):
                if row[i].isnumeric():
                    list.append(int(row[i]))
                elif row[i].replace('.', '').replace('E', '').replace('-', '').isnumeric():
                    list.append(float(row[i]))
                else:
                    if row[i].lower() == 'false':
                        list.append(int(0))
                    elif row[i].lower() == 'true':
                        list.append(int(1))
                    elif row[i].lower() == 'returning_visitor':
                        list.append(int(1))
                    elif row[i].lower() == 'new_visitor':
                        list.append(int(0))
                    elif row[i].lower() == 'other':
                        list.append(int(0))
                    else:
                        month = row[i]
                        month = month[:3]
                        month = datetime.strptime(month, '%b').month - 1
                        list.append(int(month))

            # Load the label into a list
            if row[17].lower() == 'true':
                list1.append(int(1))
            elif row[17].lower() == 'false':
                list1.append(int(0))

            labels.append(list1)
            evidence.append(list)

    megalist.append(evidence)
    megalist.append(labels)

    return megalist


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    labels = numpy.ravel(labels)

    knn_model = KNeighborsClassifier(n_neighbors=1)
    knn_model.fit(evidence, labels)

    return knn_model



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive = 0
    negative = 0
    true_negative = 0
    true_positive = 0

    for i in range(len(labels)):

            # Check for actual negatives and predicted negatives
            if labels[i] == 0:
                negative += 1
                if labels[i] == predictions[i]:
                    true_negative += 1

            # Check for actual positivies and predicted positives
            if labels[i] == 1:
                positive += 1
                if labels[i] == predictions[i]:
                    true_positive += 1
    
    sensitivity = true_positive / positive
    specificity = true_negative / negative

    set = (sensitivity, specificity)
    return set


if __name__ == "__main__":
    main()

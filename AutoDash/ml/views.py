from django.shortcuts import render
import pandas as pd
from upload.models import Data
import os
from pycaret.classification import *

def ml(request):
    context = bestmodel()
    return render(request, 'ml/ml.html', context=context)

def get_categorical_columns(df):
    """
    Returns a list of column names that contain categorical values in a Pandas DataFrame.
    """
    categorical_columns = []
    for column in df.columns[:-1]:
        if pd.api.types.is_categorical_dtype(df[column].dtype):
            categorical_columns.append(column)
        elif df[column].dtype == 'object':
            df[column] = df[column].astype('category')
            categorical_columns.append(column)
    return categorical_columns


def bestmodel():

    # Select the last file uploaded..
    last_file = Data.objects.latest('time_stamp')
    filepath = os.path.join('./documents', last_file.document)

    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_csv('./documents/CVD_save.csv')
    
    setup(df, target=df.columns[-1], silent=True, normalize=True, train_size=0.75,
          categorical_features = get_categorical_columns(df))
    setup_df = pull()

    best_model = compare_models()
    compare_df = pull()
    compare_df = compare_df.to_html()
    # Display the results..
    context = {
        'compare_df': compare_df
    }
    return context

    



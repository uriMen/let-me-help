import os
import pandas as pd


def get_questions(num_questions: int):

    q_df = pd.read_csv('questions.csv')
    # print(q_df)
    return q_df.sample(num_questions)


if __name__ == '__main__':
    df = get_questions(3)
    print(df)
    print(df.iloc[2, 0:2].values)


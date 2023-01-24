import numpy as np
import pandas as pd

GLOVE_FILE_PATH = 'glove.6B.50d.txt'


def get_word_embedding(word: str,
                       glove_file_path: str = GLOVE_FILE_PATH) -> np.ndarray:
    """
    Return the embedding vector of the given word using GloVe pretrained model
    """
    # Initialize the embedding to None
    embedding = None
    # Open the GloVe file
    with open(glove_file_path, 'r') as f:
        # Iterate through the lines in the file
        for line in f:
            # Split the line into parts
            parts = line.split()
            # The first part is the word
            curr_word = parts[0]
            # If the word matches the input word
            if curr_word == word:
                # Convert the embedding values to floats
                embedding = np.array([float(val) for val in parts[1:]])
                break
    return embedding


def distance_between_embeddings(emb1: np.array, emb2: np.array) -> float:
    """Return euclidean distance between 2 given embedding vectors"""
    dist = np.linalg.norm(emb1 - emb2)
    return dist


def get_feature_relative_score(selected_word: str,
                               other_word: str,
                               feature: str) -> float:
    """
    Return a score between 0-1 which represents the user's selection
    between 2 words based on their distance to the feature.
    """
    selected_emb = get_word_embedding(selected_word, GLOVE_FILE_PATH)
    other_emb = get_word_embedding(other_word, GLOVE_FILE_PATH)
    feature_emb = get_word_embedding(feature, GLOVE_FILE_PATH)

    selected_dist = distance_between_embeddings(selected_emb, feature_emb)
    other_dist = distance_between_embeddings(other_emb, feature_emb)

    return other_dist / (selected_dist + other_dist)


def cosine_sim_based_feature_score(selected_word: str,
                                   other_word: str,
                                   feature: str) -> float:
    """
    Based on cosine similarity, return 1 if selected word was more
    similar to the feature comparing to the other word. return 0 otherwise.
    """
    selected_emb = get_word_embedding(selected_word) #, GLOVE_FILE_PATH)
    other_emb = get_word_embedding(other_word) #, GLOVE_FILE_PATH)
    feature_emb = get_word_embedding(feature) #, GLOVE_FILE_PATH)

    words_emb = np.vstack((selected_emb, other_emb))
    # print("shapes: ", words_emb.shape, feature_emb.shape)
    # compute cosine similarity
    cosine = (np.dot(words_emb, feature_emb)
              / (np.linalg.norm(words_emb, axis=1)
                 * np.linalg.norm(feature_emb)))
    # transform to [0,1] range
    # print("**** cosine ****: ", cosine)
    # cosine = cosine + 1
    # print('cosine is: ', cosine)
    # return cosine[0] / np.sum(cosine)
    return 1 if cosine[0] > cosine[1] else 0


def get_user_score_vec(features: list, selection: list) -> np.ndarray:
    """
    Returns a scores vector of size as the number of features
    based on the given user selection - a list of tuples in which the
    first word is the selected and the second is the other.
    """
    scores = dict()
    for feature in features:
        feature_score = 0
        for words in selection:
            feature_score += cosine_sim_based_feature_score(words[0],
                                                            words[1],
                                                            feature)
        scores[feature] = feature_score / len(selection)
    return scores


def get_recommendations(domain, selection=None, user_score=None, num_rec=3) -> tuple:
    """Returns num_rec most relevant recommendation from the given domain"""
    df = pd.read_csv(f"data/{domain}.csv")
    features = df.columns[1:]
    if not user_score:
        user_score = get_user_score_vec(features, selection)
    user_vec = np.array([user_score[f] for f in features])
    # print(df.iloc[:, 1:].values, user_vec)

    cosine = (np.dot(df.iloc[:, 1:].values, user_vec)
              / (np.linalg.norm(df.iloc[:, 1:].values, axis=1)
                 * np.linalg.norm(user_vec)))
    top_idx = np.argpartition(cosine, -num_rec)[-num_rec:]
    recommendation = df.iloc[top_idx, 0].values.tolist()
    return recommendation, user_score, features


def help_decide(phrase1, phrase2, selection):
    """return decision (1 or 2) based on average similarity between
    the user selection and the phrases"""
    tokens1 = phrase1.split()
    tokens2 = phrase2.split()

    phrase1_emb = np.vstack(tuple(get_word_embedding(t) for t in tokens1))
    phrase2_emb = np.vstack(tuple(get_word_embedding(t) for t in tokens2))

    decision = {1: 0, 2: 0}
    for selected, _ in selection:
        selected_emb = get_word_embedding(selected)
        cosine1 = (np.dot(phrase1_emb, selected_emb)
                  / (np.linalg.norm(phrase1_emb, axis=1)
                     * np.linalg.norm(selected_emb)))
        # print("1: ", cosine1)

        cosine2 = (np.dot(phrase2_emb, selected_emb)
                   / (np.linalg.norm(phrase2_emb, axis=1)
                      * np.linalg.norm(selected_emb)))
        # print("2: ", cosine2)

        if cosine1.mean() > cosine2.mean():
            decision[1] += 1
        else:
            decision[2] += 1

    return max(decision, key=decision.get)


if __name__ == '__main__':
    word1 = 'computer'
    word2 = 'king'
    selection = [(word1, word2), ('pizza', 'palace')]
    feature = 'phone'
    features = ['price', 'queen', 'country']


    scores = get_user_score_vec(features, selection)

    print('score: ', scores)
    # print(f'dist between {word1} and {feature} is: {distance_between_embeddings(word_emb1, feature_emb)}')
    # print(f'dist between {word2} and {feature} is: {distance_between_embeddings(word_emb2, feature_emb)}')
    # print(f'score is: {score}')
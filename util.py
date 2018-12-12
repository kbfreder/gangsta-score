import pickle
import numpy as np

def pkl_this(filename, df):
    '''Saves df as filename. Must include .pkl extension'''
    with open(filename, 'wb') as picklefile:
        pickle.dump(df, picklefile)

def open_pkl(filename):
    '''Must include .pkl extension. Returns object that can be saved to a df.
    '''
    with open(filename,'rb') as picklefile:
        return pickle.load(picklefile)

def log_this(s):
    with open("log.txt", "a") as f:
        f.write("\n" + s + "\n")
# ------------ #
def load_lyrics_data():
    '''returns df (dataframe):
            ID, Song, Arist, Album, Genre, Lyrics,
            Median Most Sim Idx*, Top 20 Most Sim*, Cluster Label**.
            * as determined by HD of 10-topic LDA
            ** as assigned by KMeans clustering, n_clusters = 6
        and 'X': list of strings of lyrics.
    (Created after 02f-...-01)
    '''
    df = open_pkl('Data/all_lyrics_with_sim_df.pkl')
    X = df[['Lyrics']].values
    X = X.tolist()
    X = [x[0] for x in X]
    return df, X


# ---------- #
def num_doc_with_token(token, dtm):
    '''Returns number of documents in dtm (dataframe; document-term-matrix) containing token (string)'''
    return len(dtm[dtm[token] != 0])

def get_random_doc_with_token(token, dtm, doc_df, verbose=True):
    '''Input: token (string), dtm (dataframe; document-term-matrix), doc_df (dataframe; contains documents & their ID's)
    Returns index of random document containing token
    Prints song-artist ID. If verbose = True, also prints lyrics.
    '''
    token_idxs = dtm[dtm[token] != 0].index
    rand_idx = np.random.choice(token_idxs)
    print(doc_df.loc[rand_idx, 'ID'])
    if verbose:
        print(doc_df.loc[rand_idx, 'Lyrics'])
    return rand_idx


def get_idx_from_key(key, doc_df):
    return doc_df[doc_df['ID'] == key].index[0]

def get_key_from_idx(idx, doc_df):
    return doc_df.loc[idx,'ID']

def print_song_lyrics(key, doc_df):
    print(doc_df[doc_df['ID'] == key]['Lyrics'][0])

def get_lyrics(key_or_idx, doc_df, info=True, verbose=False):
    # print(type(key_or_idx))
    if type(key_or_idx) != int:
        idx = doc_df[doc_df['ID'] == key_or_idx].index[0]
    else:
        idx = key_or_idx
        # print('index passed!')
    lyrics = doc_df.loc[idx, 'Lyrics']
    song_title = doc_df.loc[idx, 'Song']
    artist = doc_df.loc[idx, 'Artist']
    # else:
    #     lyrics = doc_df[doc_df['ID'] == key_or_idx]['Lyrics']
    #     song_title = doc_df[doc_df['ID'] == key_or_idx]['Song']

    if verbose:
        print(lyrics)
    if info:
        print(f'{song_title} - {artist}')
    return lyrics


def get_song_entry(song, doc_df):
    return doc_df[doc_df['Song'] == song]

def get_idxs_by_artist(artist, doc_df):
    return doc_df[doc_df['Artist'] == artist].index

def get_song_by_artist(artist, doc_df):
    idxs = doc_df[doc_df['Artist'] == artist].index
    return doc_df.loc[idxs, 'Song'].values

def get_sim_songs(idx, doc_df, verbose=False):
    '''This pulls the top 20 most similar based on Hellinger-distance similarity of 10-topic LDA features
    '''
    sims = doc_df.loc[idx, 'Top 20 Most Sim']
    if verbose:
        print(f"Similar songs for: {doc_df.loc[idx, 'ID']}")
        print()
        for i in range(20):
            print (f"{doc_df.loc[sims[i], 'ID']} ({doc_df.loc[sims[i], 'Genre']})")
    return sims

def rap_cnty_dfs(df):
    rap_df = df[df['Genre'] == 'rap']
    cnty_df = df[df['Genre'] == 'country']
    return rap_df, cnty_df

def gangsta_score(idx, lda):
    # return np.log(lda[idx, 7]) - np.log(lda[idx, 5])
    # return np.log(lda[idx, 0]) - np.log(lda[idx, 1])
    return np.log(lda[idx, 1] / lda[idx, 0])


def pp_lda(idx, lda):
    '''Pretty print LDA vector values'''
    i = 0
    for x in lda[idx]:
        print(f'{i}: {x:.4f}')
        i += 1

def hide_axes(ax, top, right, bottom, left):
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['bottom'].set_visible(bottom)
    ax.spines['left'].set_visible(left)

    # plt.tick_params(left=False, labelleft=False, bottom=bottom, labelbottom=bottom) #, labelbottom='on')

def random_example_score(score, df):
    '''Return a random index from df whose Gangsta Score is score +/- 0.5'''
    m =((df['Gangsta Score'] > score-0.5) & (df['Gangsta Score'] < score+0.5))
    return df[m].sample().index[0]

#### Jupyter Notebooks:

- **01a_Scraping-Rap**: web-scraping Rap songs

- **01b_Scraping-Country**: web-scraping Country songs

- **01c_DataClean**: pull data from MongoDB into a pandas dataframe. Remove "emtpy" entries. 

- **02a_TopicModeling_Similarity_Clustering**: 

  - creation of document-term matrix (DTM) by Count-Vectorizing & Tf-IDF
  - LDA to reduce dimensions & Topic Model
  - Similarity: compare Cosine Similarity & Hellinger Distance
  - Clustering: compare Euclidean, Cosine, and Hellinger Distances

- **02b_EDA**: histograms of words by song, songs by artist, etc.

- **03a_FinalEval**: plots for presentation

  Appendix:

- **A01-LDA-Gensim**: LDA in Gensim. Did not perform as well as sklearn

- **A02-WordEmbeddings**: GloVE Twitter word embedding. Did not perform well.



#### Data

*Note data folder & file are not in GitHub repo, but would be created if all code were run.*

- **all_lyrics_df_181109**: dataframe containing Lyrics data. 

- **all_lyrics_with_sim_df_9_topics** dataframe with Lyrics and analysis data. Columns:

  - ID, Song, Arist, Album, Genre, Lyrics, Median Most Sim\*, Top 20 Most Sim\*, Clusters Label 2 Cosine

    \* as determined by Hellinger Distance

- **dtm_tf**: term-frequency document-term frequency matrix.
- **dtm_tf_df**: term-frequency document-term dataframe
- **tf_sparse_mtx**: sparse document term-frequency matrix
- **song_artist_list**: running tally of song-artist keys of songs scraped
- **album_url_list**: list of album url's to scrape release date from


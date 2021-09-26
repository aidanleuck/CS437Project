## Different parts of the project

# User Interface - Medium (maybe easy?) - Victor
Use graphics.py to set up necessary graphical connections to backend. Needs to be able to display query suggestions, ranked list of results, and allow users to submit queries.

# Text Processing, Stopwords, Stemming - Easy - Oscar
Implement tokenizer (HW2), remove stopwords (Zipf's law?) (HW2), stem or lem non-stopwords (HW2), create index structure for dc (HW3).

# Suggesting Queries - Hard - Aidan
Use a query log to generate query suggestions. Triggered by space. Identify possible candidates that include the terms triggering it. Rank each suggest on given equation.

# Identify Candidate Resource - Medium
Create set of documents comprised of all documents in DC that contain each of the terms in q. If less than 50 then get resources that contain n-1 in q.

# Relevance Ranking - Medium
Compute relevance for each resource in CR based on given equations.

# Generating Snippets - Medium
For each selected result, create a corresponding snippet which includes the title and the two sentences that have the highest cosine similarity with respect to q, TF-IDF.

# Examining SE Performance - Easy - Group
Run the queries in TestSet and make sure we are getting the expected results.

# Comparison - Easy - Group
Getting expected result from Wikipedia search module.

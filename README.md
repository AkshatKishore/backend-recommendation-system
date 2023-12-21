# Recommendation System
This repository contains a complete source code for a recommendation engine.
The algorithm was followed for this projects development:

1. Model development in Python: A Collaborative Filtering algorithm based on cosine silimarity was used to generate n recommendations for users.
2. An AWS EC2 backend was created.
3. A pre-existing SQL database was instantiated in the backend.
4. The model was deployed in the backend, and the relevant SQL databases were linked to the model scripts using a MySQL connector.
5. This backend was connected to a front end using a Flask API.

## Utilisation
The provided source code can be used as is in a pre-existing backend, changing only the SQL database name and password name at time of instantiation. 

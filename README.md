# FMI Arena

## Users

Create a user
 ```bash
 curl -X POST 'http://127.0.0.1:5000/users/' \
--data-raw '{
    "first_name": "itso",
    "last_name": "boyanov",
    "email": "itso@gmail.com"
}'
```

Find users
 ```bash
 curl -X GET 'http://127.0.0.1:5000/users/'  # all
 curl -X GET 'http://127.0.0.1:5000/users/1'  # user with id 1
 
```


## Problems
### Endpoints
 - submit a problem (cin / cout format)
 - get problems by tags (simplified - id, name)
 - assign tags
 - get problem by id
 - post submission 
    - [optional] will store in submission history
    - will result in test case_results
      `  [{input: .. ,expected: .., output: .., passed: True|False }...]`

## Submissions
 - each submission is stored, linked to user
 - only the best submission per user is stored
 - submissions are ranked - % passed test and speed in ms
 - you can resubmit (re-execute) submission
 - you can fetch all user submissions

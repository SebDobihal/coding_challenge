# solution

this solution was created by Sebastian Dobihal
as part of a coding challenge for sipgate GmbH
---

## setup

this solution uses Python 3.12.1
it's requirements are stated in the [**requirements.txt**](./requirements.txt).
pip install -r ./requirements.txt should do the trick

## localhost

I used uvicorn to run it locally: pip install uvicorn[standard]
but any other local server should work as well, so it's not part of the
requirements.txt

### uvicorn
uvicorn main:app --port 8080 --reload
starts the localserver 


## database

I use an SQLite database, as it seems sufficient for this project's scope

---

## used modules or tools and my reasoning why I used them

| module or tool | reasoning                                                                              |
|----------------|----------------------------------------------------------------------------------------|
| Python | I am currently most used to programming in Python |
| FastAPI        | The challenge is to implement an API, so using a framework to do so seemed reasonable     |
| httpx          | FastAPIs TestClient requires it, and I use the TestClient to test the API              |
| pydantic       | I prefer typing as it reduces bugs in my opinion, and pydantic provides tools to do so |
| SQLAlchemy     | ORM, easier data handling                                                              |

## Thoughts and remarks

### my solution

- I didn't implement any user management or authentication of any kind
  as this is not in the scope of this challenge
- I didn't implement any db migration tooling(like for example Alembic) as this
  database
  schema is fairly simple and not subject to immediate changes
- I didn't implement any mocking data as that would be out of scope for this  
project. There are no complex datastructures or relationships that would make
it necessary.

### Problems and self-critique

- the patch request doesn't work inside the todo.json, and I don't know why
  (status code: 418)
    - postman patch request works fine
    - automated tests are working fine as well
    - Manual tests are fine too
- the openAPI doc uses due_date instead of the alias due-date, which breaks the
  post request
- my tests create a .db file which isn't used, it's because of the
  TestClient, and its use of the app from the FastAPI implementation
- my request body isn't "multipart/form-data" but "x-www-form-urlencoded",
  which is right-ish, as I don't use/permit files in the requests
- some types don't perfectly match, but I didn't find any better solution

## additional information:

- even though I know about their existence,
  I didn't use any generator tool to create the API from the give JSON file
    - even though this would have been faster and more efficient I think it
      would
      defeat the purpose of this challenge
    - neither did I use any AI tool to generate any of the code, for the same
      reason



### What I learnt already
- having the newest packages isn't always the best idea, it can produce bugs
very fast 
- pushing code while having multiple GitHub accounts and multiple IDEs 
can lead to pushing code from the wrong account.


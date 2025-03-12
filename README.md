# About the backend
The project uses swagger with pydantic validations to ensure correct data is being sent to and from the backend.
It also helps frontend devs to know what needs to be send and what to expect from the api.

Swagger is available at root url, which is (by default) http://localhost:8000/

# Supabase docs
https://supabase.com/docs/reference/python/introduction

# Pydantic docs
https://docs.pydantic.dev/latest/

# Folder core has code for supabase setup
you don't need to touch db_connection, and in routers there are routers used by the modules.

# Backend structure
Each backend module should be in a seperate folder, for example test_lessons, which coresponds to a database table with the same name and should be used for writing APIs that manage use this table, like creating, deleting, updating.

Inside of the modeule, there should be at least these three files:
  dataclasses.py
  router.py
  service.py

In dataclasses.py should be pydantic models that create a class/Python type (like types in TypeScript).
In service.py we write functions that connect to supabase.
Router.py describes REST API and invoke coresponing functions of the service. After creating a router with API, you have to add it to the routers inside of the /core/routers.py.

There can be more files ina module if you need them.

There's a test module, test_lessons with all the needed files and setup. Use it as a refrence if you need it. :D

# About .ENV
You should all create .env file with variables used in docker.

The structure of the .env file can be found in template.env. Do not put credentials or secret data in other files than .env.
If you have default ports taken, you can change it in the .env file as well.
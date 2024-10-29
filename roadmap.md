- [x] Define Some Models with SQLModel
    - [x] Article (async driver)
    - [x] Server applies migration on startup
        - [x] use alembic to manage migrations
        - [x] Use FastAPI lifespan to apply migrations

- [x] Add Some Article Endpoints
    - [x] Create
    - [x] Get
    - [x] List
    - [x] Update
    - [x] Delete

- [ ] Model a Series of Articles

- [ ] Provide a Health Check Endpoint

- [ ] Authorization
    - OAuth2, see FastAPI Doc
    - Would an API key be better?
    - Maybe use Basic Auth to request an API key?
    - [ ] Create
    - [ ] Update
    - [ ] Delete

- [ ] Rate Limit the API
    - Most likely SlowAPI

- [ ] Front End
    - [ ] Server Static Files with FastAPI
    - [ ] React? Probably.

- [ ] Docker Image(s)
    - [x] FastAPI deployment build
    - [ ] Build step for front end
    - [ ] Dev container?
        - only really need this if using docker compose to access other resources
 
- [ ] CLI to manage articles
    - what language go / rust / python
    - I'd like compiled with easy builds
    - Crossplatform support

- [ ] Search
    - Use postgresql index? 
    - Elastic Search?
    - Whoosh? 

- [ ] K8s / Helm Chart
    - Maybe ... 

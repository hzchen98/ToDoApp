# To Do App


## Dev

**Frontend**: any change build it before rerun docker.  

**Database**: in Docker Compose include DB instance, for external DB usage change the API service environment variables: 
* MYSQL_HOST
* MYSQL_PORT
* MYSQL_USER
* MYSQL_PASS
* MYSQL_DB



## Run

```
docker-compose up
```

## Deploy

Use CI/CD for deploy to production server

**Single Server**: 

Github Action workflow job deploy via SSH
```
     - name: Deploy to production
        run: |
          ssh user@your-server-address 'cd /home/app/ToDoApp/ && git pull origin main && docker-compose up -d'
```


**K8s**:

CI/CD steps:

* Build, test and upload docker image to an docker registry server.
E.g. Gitlab, it allows us to save the image in the same repository of the code.
* Deploy docker image from registry server to K8s


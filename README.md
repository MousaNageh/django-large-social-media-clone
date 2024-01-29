# social media clone

## Run Application

#### 1) get a clone from repo or just download it
#### 2) create `.env` file in root directory  
#### 3) Copy `env_files/.env.local` to `.env`
#### 4) run docker compose :

- run the following commnand to build images and run containers
```sh
docker-compose up 
 ```
- or for docker detached mode run :
```sh
docker-compose up --build  -d
 ```
- or for newer vision of docker 
```sh
docker compose up
 ```
### base_url : `http://127.0.0.1:6060`
### admin panel url : `http://127.0.0.1:6060/admin`
- default admin email `admin@admin.com`
- default admin password `12345`
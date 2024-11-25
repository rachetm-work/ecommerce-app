# e-com-app - Basic Ecommerce App

## Zania Assignment

**Author:** Rachet M

### Environment file setup
- Create a `.env` file in the root directory and add the all the variables in the `.env.example` file.
- Since the default username and password for the database in the docker db container is `postgres` and `postgres`, the same is used.


### For deployment on docker -
- Navigate to `/deployment` directory from project root
- Run `bash deploy.sh`
  - This will build the docker image and run the containers using docker-compose
  - The database for the app i.e.`ecommerce` and the test database i.e.`ecommerce_test` will be created once the db container starts and the initial migrations will also be run on the database.
- The app will be running on `http://localhost:8000`
- The api documentation can be accessed at `http://localhost:8000/api/docs`

### For running tests -
- Execute the following command from the terminal after deployment on docker -
    ```shell
    docker exec -it ecom-service pytest
    ```
  This will run all the tests in the app.



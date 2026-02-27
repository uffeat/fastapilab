1. Create a new Web Service on Render.
2. Specify the URL to your new repository or this repository.
3. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
4. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

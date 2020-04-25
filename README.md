## Time Tracking Tool

Using [Hubstaff V1 API](https://api.hubstaff.com/v1/)

# Prerequisites
To run this project locally, you need the following;
- Python - installed locally
- Create a `.env` file and populate it with env variables according to the `.env.sample` file


# NOTE:
- App may not run properlyif the required environment variables are not set up, especially the email report feature

**Set Up**
- Clone the repository 
> run `git clone https://github.com/cdvx/time-tracker`

- Cd into project
> `cd time-tracker`

- Run the start-api.sh script to set up project for the first time
> `bash start-api.sh`

- Project can easily be run later on by running
> `bash run-api.sh`

- Test the application 
> Go to [home](http://127.0.0.1:5000/)


- Run tests with 
> `pytest --cov=api`




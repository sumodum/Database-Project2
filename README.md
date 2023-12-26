#CZ4031 Assignment 2

### Connecting your Query with Query Plans

### Execution Instructions
- Run `pip install -r requirements.txt` to ensure all required libraries/ packages are installed
- Check `config.json` file in directory to ensure credentials for database connection is inputted correctly (TPC-H hosted on cloud)
  ```json
  {
  "TPC-H": {
      "host" : "ec2-18-215-41-121.compute-1.amazonaws.com",
      "database" : "d6kbte63gmo8od",
      "user" : "cexnpxrplobezy",
      "password" : "4649116bc8b22d9beaa9061d46010eb1058d625685495d5a2084b12a713f7fe1",
      "port" : "5432"
	}
  "IMDB": {
    "host": "ec2-54-163-34-107.compute-1.amazonaws.com",
    "database": "d53bimrbn8tguo",
    "user": "zjmruztvuhtmyt",
    "port": "5432",
    "password": "ee47705719ff563e609e8cb6108851e3faa071eb189a822880ce032b940a38b5"
  }
  }
  
  ```
- Navigate to folder with project.py
- Ensure python 3 is installed and execute python project.py on terminal: `python project.py`
- Flask app will be bulit and local host link will created: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Click on link and a web browser will be opened to direct you to web page.

## Tools

* [PostgreSQL](https://www.postgresql.org/)
* [FLASK](https://flask.palletsprojects.com/)


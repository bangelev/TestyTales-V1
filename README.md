# Recipe App

The Recipe App is a web application that allows users to manage and discover recipes. It provides functionality to add, update, and retrieve recipes using a RESTful API.

## Features

- Add, update, and retrieve recipes with details such as name, category, ingredients, instructions, and cooking time.
- Error handling for various scenarios, such as recipe not found or internal server errors.

## Installation

1. Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/bangelev/TastyTales.git
cd TastyTales-V1

```

2. Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows
```

3. Install the required dependencies.

```bash
cd Backend
pip install -r requirements.txt
```

4. Configure the application settings.

- set up environment variables in .env file

- MongoDB uri - currently is setup to localhost

  4.1 Seed the DB

```bash
cd Backend\utils
python seedDB.py
```

5. Start the application.
   If using local MongoDb activate

```bash
mongod
```

Activate the main app.py file

```bash
python app.py
```

## API Endpoints

- `GET /recipes`: Retrieve a list of all recipes.
- `GET /recipes/{id}`: Retrieve a single recipe by its ID.
- `POST /recipes`: Add a new recipe.
- `PUT /recipes/{id}`: Update an existing recipe.

## Testing

Run the test suite to ensure proper functionality and error handling.

```bash
pytest
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is not licensed

## Next to come

Adding OAuth with GitHub and User model

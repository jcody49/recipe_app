# The Cookbook Collective

The Cookbook Collective is a web application that allows users to explore, share, and contribute recipes. Whether you're a seasoned chef or a cooking enthusiast, this platform provides a space to discover new culinary creations, share your favorite recipes, and engage with a community of food lovers.

## Features

- **Browse Recipes:** Explore a diverse range of recipes categorized by type, difficulty, and more.

![Browse recipes...](/static/recipes/images/browse.png)

- **Search Functionality:** Quickly find specific recipes using by searching for the recipe name or its ingredients.

![Search recipes...](/static/recipes/images/search.png)

- **Create and Share Recipes:** Contribute your own recipes and share them with the community.

![Upload recipes...](/static/recipes/images/create_recipe.png)

- **Data Visualizations:** Gain insights into recipe distributions, difficulty levels, and more through interactive visualizations.

![Data Visualizations...](/static/recipes/images/visualization.png)

- **User Accounts:** Create an account to personalize your Cookbook Collective experience.

![Account Creation](/static/recipes/images/account_creation.png)





## Build

### Technologies Used
- HTML, CSS, JavaScript
- Python 
- Django 
- Pandas 

### Deployment
- Hosted on Heroku
- Gunicorn 21.2.0
- Whitenoise 6.6.0 for serving static files
- Django-Storages[boto3] 1.11.0 for static and media file storage on AWS S3


## Installation

To run The Cookbook Collective locally, follow these steps:

1. Clone the repository:

   git clone https://github.com/your-username/cookbook-collective.git

2. Navigate to the project directory:


    cd cookbook-collective


3. Install dependencies:


    pip install -r requirements.txt


4. Apply migrations:


    python manage.py migrate

5. Run the development server:


    python manage.py runserver

6. Access the application at http://localhost:8000/

## Usage

- Create a user account or log in if you already have one.
- Explore recipes, contribute your own, or save your favorites.
- Enjoy the Cookbook Collective community and culinary inspiration!


## License

This project is licensed under the MIT License.

Happy cooking!
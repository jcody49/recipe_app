from django import template
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import pandas as pd
from .models import Recipe
from django.db.models import Count
from enum import Enum
from django.http import HttpResponse




def get_recipe_name_from_id(value):
    try:
        recipe_name = Recipe.objects.get(id=value).name
    except Recipe.DoesNotExist:
        recipe_name = f"Recipe {value} (Not Found)"
    return recipe_name



def get_recipe_type_distribution_data(type_of_recipe=None):
    print("Inside get_recipe_type_distribution_data function")

    # Get all distinct recipe types
    all_recipe_types = Recipe.TYPE_OF_RECIPE

    # Create a dictionary to store counts for each type
    recipe_type_counts = {type_of_recipe: 0 for type_of_recipe, _ in all_recipe_types}

    # Loop through each type and count the number of recipes
    for type_of_recipe, _ in all_recipe_types:
        count = Recipe.objects.filter(type_of_recipe=type_of_recipe).count()
        recipe_type_counts[type_of_recipe] = count

    # Convert the dictionary to a Pandas DataFrame
    data = pd.DataFrame(list(recipe_type_counts.items()), columns=['recipe_type', 'count'])
    
    print("Data for recipe type distribution:", data)
    return data






#test
def get_recipe_difficulty_distribution_data(type_of_recipe):
    # Filter recipes based on type_of_recipe
    recipes = Recipe.objects.filter(type_of_recipe=type_of_recipe)

    # Query the database to get the difficulty distribution data
    data = recipes.values('difficulty').annotate(count=Count('difficulty'))

    # Convert the queryset to a Pandas DataFrame
    data_df = pd.DataFrame.from_records(data)

    return data_df


def render_chart(request, chart_type, data=None, **kwargs):
    print("chart_type:", chart_type)
    print("data:", data)

    if data is None or data.empty:
        # Handle the case when data is not available or empty
        print("No data available.")
        return HttpResponse("No data available.")

    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)

    if chart_type == 1:
        plt.title("Recipe Type Distribution", fontsize=20)
        plt.bar(data["recipe_type"], data["count"])
        plt.xlabel("Recipe Types", fontsize=16)
        plt.ylabel("Number of Recipes", fontsize=16)

    elif chart_type == 2:
        plt.title("Recipe Difficulty Distribution", fontsize=20)
        labels = data["difficulty"]
        plt.pie(data["count"], labels=labels, autopct="%1.1f%%")
        plt.legend(data["difficulty"], loc="upper right", bbox_to_anchor=(1.0, 1.0), fontsize=12)

    elif chart_type == 3:
        plt.title("Recipes Created per Month", fontsize=20)
        x_values = data["month"].to_numpy()
        y_values = data["recipe_count"].to_numpy()
        plt.plot(x_values, y_values)
        plt.xlabel("Months", fontsize=16)
        plt.ylabel("Number of Recipes", fontsize=16)

    else:
        print("Unknown chart type.")

    plt.tight_layout(pad=3.0)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode("utf-8")

    print("Chart Image Length:", len(chart_image))
    return chart_image


def get_graph(fig):
    # create a BytesIO buffer for the image
    buffer = BytesIO()

    # create a plot with a BytesIO object as a file-like object. Set format to png
    fig.savefig(buffer, format='png')

    # set cursor to the beginning of the stream
    buffer.seek(0)

    # retrieve the content of the file
    image_png = buffer.getvalue()

    # encode the bytes-like object
    graph = base64.b64encode(image_png)

    # decode to get the string as output
    graph = graph.decode('utf-8')

    # free up the memory of buffer
    buffer.close()

    # return the image/graph
    return graph




register = template.Library()

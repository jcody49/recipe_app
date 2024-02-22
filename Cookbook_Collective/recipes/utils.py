# Standard Library Imports
from io import BytesIO
import base64
from enum import Enum

# Third-party Library Imports
import matplotlib.pyplot as plt
import pandas as pd



# Django Imports
from django import template
from django.db.models import Count
from django.http import HttpResponse
from django.http import JsonResponse


# Project-specific Imports
from .models import Recipe


def get_recipe_name_from_id(value):
    try:
        recipe_name = Recipe.objects.get(id=value).name
    except Recipe.DoesNotExist:
        recipe_name = f"Recipe {value} (Not Found)"
    except Exception as e:
        # Handle unexpected errors during the operation
        print(f"Error getting recipe name: {e}")
        recipe_name = f"Error fetching recipe name"
    return recipe_name



# counts the occurance of each recipe type for a data visualization
def get_recipe_type_distribution_data(type_of_recipe=None):
    try:
        all_recipe_types = Recipe.TYPE_OF_RECIPE
        recipe_type_counts = {type_of_recipe: 0 for type_of_recipe, _ in all_recipe_types}

        for type_of_recipe, _ in all_recipe_types:
            count = Recipe.objects.filter(type_of_recipe=type_of_recipe).count()
            recipe_type_counts[type_of_recipe] = count

        data = pd.DataFrame(list(recipe_type_counts.items()), columns=['recipe_type', 'count'])
        return data
    except Exception as e:
        # Handle unexpected errors during the operation
        print(f"Error getting recipe type distribution data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error


# counts the occurrence of each difficulty for a data visualization
def get_recipe_difficulty_distribution_data(request, type_of_recipe="default"):
    try:
        if type_of_recipe == "default":
            # Handle default logic or return an appropriate response
            default_data = {'message': 'Default data or message for recipe difficulty distribution'}
            return HttpResponse("No data available for rendering the chart.")
        else:
            recipes = Recipe.objects.filter(type_of_recipe=type_of_recipe)
            data = recipes.values('difficulty').annotate(count=Count('difficulty'))
            print("Difficulty Distribution Data:", data)
            data_df = pd.DataFrame.from_records(data)

            if data_df.empty:
                print("No data available for rendering the chart.")
                return HttpResponse("No data available for rendering the chart.")

            return data_df

    except Exception as e:
        print(f"Error getting recipe difficulty distribution data: {e}")
        return pd.DataFrame()








# takes data and renders its respective chart_image
def render_chart(request, chart_type, data=None, **kwargs):
    if data is None or data.empty:
        print("No data available for rendering the chart.")
        return HttpResponse("No data available for rendering the chart.")

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
    plt.close(fig)

    return chart_image


def get_graph(fig):
    try:
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph
    except Exception as e:
        # Handle unexpected errors during the operation
        print(f"Error getting graph: {e}")
        return None



# template.Library is a class provided by Django in the django.template module.
# It is used to register and organize custom template tags and filters.
register = template.Library()

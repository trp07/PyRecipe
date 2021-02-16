from pyrecipe.storage.shared.recipe_model import RecipeModel

from recipe_scrapers import scrape_me
from recipe_scrapers import WebsiteNotImplementedError


def import_from_url(url: str) -> dict:
    """
    The public interface to this module.  Import the recipe from the supplied
    URL and return the attributes as a dict.
    """
    try:
        scraper = scrape_me(url)
    except WebsiteNotImplementedError:
        scraper = scrape_me(url, wild_mode=True)
    except Exception as e:
        return {"error": e}

    notes = ["Imported from: " + url]
    nutrients = [k + ": " + v for k,v in scraper.nutrients().items()]

    print("SCRAPER: ", scraper.yields())
    return {
        "name": scraper.title(),
        "prep_time": 0,
        "cook_time": scraper.total_time() or 999,
        "servings": scraper.yields() or "",
        "ingredients": scraper.ingredients(),
        "directions": scraper.instructions().split("\n"),
        "tags": ["imported", scraper.host().split(".")[0]],
        "notes": notes + nutrients,
        "images": scraper.image(),
    }

import json
import numpy as np

from ouroboros.helpers.options import SliceOptions

Result = tuple[any, None] | tuple[None, str]

ParseResult = tuple[dict, None | str]


def parse_neuroglancer_json(json_path) -> ParseResult:
    """
    Open and parse a neuroglancer state JSON string and return a dictionary of the parsed data.

    Parameters
    ----------
    json_string : str
        The JSON string to parse.

    Returns
    -------
    ParseResult
        A tuple containing the parsed JSON dictionary and an error if one occurred.
    """
    try:
        with open(json_path) as f:
            json_string = f.read()

            parsed_json = json.loads(json_string)

            return parsed_json, None
    except json.JSONDecodeError as e:
        return {}, f"An error occurred while parsing the given JSON file: {str(e)}"
    except Exception as e:
        return {}, f"An error occurred while opening the given JSON file: {str(e)}"


def neuroglancer_config_to_annotation(config, options: SliceOptions) -> Result:
    """
    Extract the first annotation from a neuroglancer state JSON dictionary as a numpy array.

    Parameters
    ----------
    config : dict
        The neuroglancer state JSON dictionary.

    Returns
    -------
    Result
        A tuple containing the annotation points and an error if one occurred.
    """

    try:
        for layer in config["layers"]:
            if (
                layer["type"] == "annotation"
                and layer["name"] == options.neuroglancer_annotation_layer
            ):
                annotations = layer["annotations"]

                result = [
                    data["point"] for data in annotations if data["type"] == "point"
                ]

                return np.array(result), None
    except Exception as e:
        return None, f"An error occurred while extracting the annotations: {str(e)}"

    return None, "No annotations found in the file."


def neuroglancer_config_to_source(config, options: SliceOptions) -> Result:
    """
    Extract the source URL from a neuroglancer state JSON dictionary.

    Parameters
    ----------
    config : dict
        The neuroglancer state JSON dictionary.

    Returns
    -------
    Result
        A tuple containing the source URL and an error if one occurred.
    """
    try:
        for layer in config["layers"]:
            if (
                layer["type"] == "image"
                and layer["name"] == options.neuroglancer_image_layer
            ):
                if isinstance(layer["source"], dict):
                    return layer["source"]["url"], None
                elif isinstance(layer["source"], str):
                    return layer["source"], None
                else:
                    return None, "Invalid source format in the file."
    except Exception as e:
        return None, f"An error occurred while extracting the source URL: {str(e)}"

    return None, "No source URL found in the file."

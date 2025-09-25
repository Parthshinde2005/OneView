import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def main(client, customer_id):
    """
    The main function that creates all campaigns for the specified customer_id.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    # Create the query.
    query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.name"""

    # Issue a search request.
    stream = googleads_service.search_stream(customer_id=customer_id, query=query)

    print(f"Campaigns in customer ID '{customer_id}':")
    # Iterate through the results and print campaign information.
    for batch in stream:
        for row in batch.results:
            print(
                f"\t- Campaign with ID {row.campaign.id} "
                f"and name '{row.campaign.name}' was found."
            )

if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file
    # Load from the current directory instead of home directory
    import os
    config_path = os.path.join(os.path.dirname(__file__), "google-ads.yaml")
    googleads_client = GoogleAdsClient.load_from_storage(path=config_path)

    # The customer ID for the account you want to fetch campaigns from.
    # Replace this with a real account ID that your MCC has access to.
    # Do NOT include hyphens.
    CUSTOMER_ID = "7217957631"

    try:
        main(googleads_client, CUSTOMER_ID)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
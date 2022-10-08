from frameioclient import FrameioClient

async def upload(file_name):
    client = FrameioClient("fio-u-FHtWy9PLoivouhMtkpTj3LnN9_a-4dsyow-WO6WPEd9uEMMk1ZKPwNMZ4TRnCBfS")

    data = client.assets.upload("6d9aa811-fc85-4d80-a208-1b10716567d0", f"/Users/matthewxia/Documents/Coding/Tennis69420/tennis360/videos/{file_name}.mov")

    asset_id = data['id']

    link = client.review_links.create(
                project_id="6d9aa811-fc85-4d80-a208-1b10716567d0",
                name="review_link"
            )

    client.review_links.update_assets(
                link_id = link['id'],
                asset_ids = [asset_id]
            )

    print(link['short_url'])
    return link['short_url']
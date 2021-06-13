import requests
from requests import HTTPError


class StorageFileApi:
    DEFAULT_SEARCH_OPTIONS = {
        "limit": 100,
        "offset": 0,
        "sortBy": {
            "column": "name",
            "order": "asc",
        },
    }

    def __init__(self, url: str, headers: dict, bucket_id: str):
        """
        Parameters
        ----------
        url
            base url for all the operation
        headers
            the base authentication headers
        bucket_id
            the id of the bucket that we want to access, you can get the list of buckets with the SupabaseStorageClient.list_buckets()
        """
        self.url = url
        self.headers = headers
        self.bucket_id = bucket_id
        # self.loop = asyncio.get_event_loop()
        # self.replace = replace
        pass

    def create_signed_url(self, path: str, expires_in: int):
        """
        Parameters
        ----------
        path
            file path to be downloaded, including the current file name.
        expires_in
            number of seconds until the signed URL expires.
        """
        try:
            _path = self._get_final_path(path)
            print(f"{self.url}/object/sign/{_path}")
            response = requests.post(
                f"{self.url}/object/sign/{_path}",
                json={"expiresIn": str(expires_in)},
                headers=self.headers,
            )
            data = response.json()
            print(data)
            data["signedURL"] = f"{self.url}{data['signedURL']}"
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6
        except Exception as err:
            print(f"Other error occurred: {err}")  # Python 3.6
        else:
            return data

    def move(self, from_path: str, to_path: str):
        """
        Moves an existing file, optionally renaming it at the same time.
        Parameters
        ----------
        from_path
            The original file path, including the current file name. For example `folder/image.png`.
        to_path
            The new file path, including the new file name. For example `folder/image-copy.png`.
        """
        try:
            response = requests.post(
                f"{self.url}/object/move",
                data={
                    "bucketId": self.bucket_id,
                    "sourceKey": from_path,
                    "destinationKey": to_path,
                },
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6
        except Exception as err:
            print(f"Other error occurred: {err}")  # Python 3.6
        else:
            return response.json()

    def remove(self, paths: list):
        """
        Deletes files within the same bucket
        Parameters
        ----------
        paths
            An array or list of files to be deletes, including the path and file name. For example [`folder/image.png`].
        """
        try:
            response = requests.delete(
                f"{self.url}/object/{self.bucket_id}",
                data={"prefixes": paths},
                headers=self.headers,
            )
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6
        except Exception as err:
            raise err  # Python 3.6
        else:
            return response.json()

    def list(self, path: str = None, options: dict = {}):
        """
        Lists all the files within a bucket.
        Parameters
        ----------
        path
            The folder path.
        options
            Search options, including `limit`, `offset`, and `sortBy`.
        """
        try:
            body = dict(self.DEFAULT_SEARCH_OPTIONS, **options)
            headers = dict(self.headers, **{"Content-Type": "application/json"})
            body["prefix"] = path if path else ""
            getdata = requests.post(
                f"{self.url}/object/list/{self.bucket_id}", json=body, headers=headers
            )
            getdata.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6
        except Exception as err:
            raise err  # Python 3.6
        else:
            return getdata.json()

    def _get_final_path(self, path: str):
        return f"{self.bucket_id}/{path}"

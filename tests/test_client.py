from __future__ import annotations

import random
import string
from typing import TYPE_CHECKING, Any, Union

import pytest
from gotrue import Session, User

if TYPE_CHECKING:
    from supabase import Client


def _random_string(length: int = 10) -> str:
    """Generate random string."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def _assert_authenticated_user(data: Union[Session, User, str, None]) -> None:
    """Raise assertion error if user is not logged in correctly."""
    assert data is not None
    assert isinstance(data, Session)
    assert data.user is not None
    assert data.user.aud == "authenticated"


@pytest.mark.xfail(
    reason="None of these values should be able to instanciate a client object"
)
@pytest.mark.parametrize("url", ["", None, "valeefgpoqwjgpj", 139, -1, {}, []])
@pytest.mark.parametrize("key", ["", None, "valeefgpoqwjgpj", 139, -1, {}, []])
def test_incorrect_values_dont_instanciate_client(url: Any, key: Any) -> None:
    """Ensure we can't instanciate client with nonesense values."""
    from supabase import Client, create_client

    _: Client = create_client(url, key)


@pytest.mark.skip(reason="TO FIX: Session does not terminate with test included.")
def test_client_auth(supabase: Client) -> None:
    """Ensure we can create an auth user, and login with it."""
    # Create a random user login email and password.
    random_email = f"{_random_string(10)}@supamail.com"
    random_password = _random_string(20)
    # Sign up (and sign in).
    user = supabase.auth.sign_up(
        email=random_email,
        password=random_password,
        phone=None,
    )
    _assert_authenticated_user(user)
    # Sign out.
    supabase.auth.sign_out()
    assert supabase.auth.user() is None
    assert supabase.auth.session() is None
    # Sign in (explicitly this time).
    user = supabase.auth.sign_in(email=random_email, password=random_password)
    _assert_authenticated_user(user)


def test_client_select(supabase: Client) -> None:
    """Ensure we can select data from a table."""
    # TODO(fedden): Add this set back in (and expand on it) when postgrest and
    #               realtime libs are working.
    data, _ = supabase.table("countries").select("*").execute()
    # Assert we pulled real data.
    assert data


def test_client_insert(supabase: Client) -> None:
    """Ensure we can select data from a table."""
    data, _ = supabase.table("countries").select("*").execute()
    # Assert we pulled real data.
    previous_length = len(data)
    new_row = {
        "name": "test name",
        "iso2": "test iso2",
        "iso3": "test iso3",
        "local_name": "test local name",
        "continent": None,
    }
    result, _ = supabase.table("countries").insert(new_row).execute()
    # Check returned result for insert was valid.
    assert result
    data, _ = supabase.table("countries").select("*").execute()
    current_length = len(data)
    # Ensure we've added a row remotely.
    assert current_length == previous_length + 1


@pytest.mark.skip(reason="missing permissions on test instance")
def test_client_upload_file(supabase: Client) -> None:
    """Ensure we can upload files to a bucket"""

    TEST_BUCKET_NAME = "atestbucket"

    storage = supabase.storage()
    storage_file = storage.StorageFileAPI(TEST_BUCKET_NAME)

    filename = "test.jpeg"
    filepath = f"tests/{filename}"
    mimetype = "image/jpeg"
    options = {"contentType": mimetype}

    storage_file.upload(filename, filepath, options)
    files = storage_file.list()
    assert files

    image_info = None
    for item in files:
        if item.get("name") == filename:
            image_info = item
            break

    assert image_info is not None
    assert image_info.get("metadata", {}).get("mimetype") == mimetype

    storage_file.remove([filename])

from spotivrau.models import Artist
from .utils import file_fixture


def create_artist(client, **data):
    return client.post(
        '/artist',
        data=data,
        content_type='multipart/form-data'
    )


def test_create_artist(client):
    response = create_artist(
        client,
        name='Astrix',
        picture=file_fixture('astrix.jpg'),
    )

    data = response.get_json()
    artist = Artist.objects.get(id=data['id'])

    assert response.status_code == 200
    assert artist.name == 'Astrix'
    assert artist.picture_path.endswith(data['id'] + '.artist.jpg')


def test_list_artist(client):
    Artist(
        id='fd070bb5-84eb-4042-8020-c0a6996f88c1',
        name='John Von Neuman',
        picture_path='/tmp/fd070bb5-84eb-4042-8020-c0a6996f88c1.artist.jpg'
    ).save()

    response = client.get('/artists')

    assert len(response.get_json()['artists']) > 0


from tnd_api.models import Artist
artists = Artist.objects.all()
for a in artists:
	for al1 in a.album_set.all():
		for al2 in a.album_set.all():
			if al1.id != al2.id and al1.title == al2.title:
				al1.delete()
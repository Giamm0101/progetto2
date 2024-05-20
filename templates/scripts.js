function openPopup(title, artist, album, year) {
    document.getElementById('popup-title').innerText = title;
    document.getElementById('popup-artist').innerText = "Artist: " + artist;
    document.getElementById('popup-album').innerText = "Album: " + album;
    document.getElementById('popup-year').innerText = "Year: " + year;
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

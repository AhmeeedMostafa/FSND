window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};


var deleteBtn;
if (deleteBtn = document.getElementById('deleteVenueBtn')) {
  deleteBtn.onclick = function(e) {
    e.preventDefault();

    var confirmation = confirm("Are you sure that you want to delete this venue?");

    if (confirmation === true) {
      var venueId = e.target.dataset.venueId;
  
      fetch('/venues/' + venueId, {
        method: 'DELETE'
      })
      .then((res) => res.json())
        .then(data => window.location = data.location)
      .catch((error) => alert('something went wrong while deleting the venue, ' + error + '.'))
    }
  }
}
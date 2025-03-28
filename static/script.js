$(document).ready(function() {
    $('#predictionForm').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            luas_tanah: $('#luas_tanah').val(),
            lokasi: $('#lokasi').val()
        };

        $.ajax({
            url: '/predict',
            method: 'POST',
            data: formData,
            success: function(response) {
                if (response.error) {
                    alert(response.error);
                    return;
                }
                
                $('#prediksiText').html(
                    `Prediksi harga rumah di ${response.lokasi} dengan luas tanah ${response.luas_tanah} m²:<br>
                    <strong>${response.prediksi}</strong>`
                );
                $('#hasil').removeClass('d-none');
            },
            error: function() {
                alert('Terjadi kesalahan. Silakan coba lagi.');
            }
        });
    });
}); 
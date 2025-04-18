document.addEventListener('DOMContentLoaded', function() {
    // Initialize thumbnail gallery
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('main-image');
    
    if (thumbnails.length > 0 && mainImage) {
      thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
          // Remove active class from all thumbnails
          thumbnails.forEach(t => t.classList.remove('active'));
          
          // Add active class to clicked thumbnail
          this.classList.add('active');
          
          // Update main image
          const img = this.querySelector('img');
          mainImage.src = img.src;
        });
      });
    }
    
    // Check availability form
    const availabilityForm = document.getElementById('availability-form');
    if (availabilityForm) {
      availabilityForm.addEventListener('submit', function(e) {
        // Form is submitted normally to the reservation page
        // Additional validation could be added here if needed
        
        // Example of AJAX availability check (uncomment if needed)
        /*
        e.preventDefault();
        
        const carId = document.getElementById('car-id').value;
        const pickupDate = document.getElementById('pickup-date').value;
        const returnDate = document.getElementById('return-date').value;
        
        fetch(`/api/check-availability/?car_id=${carId}&start_date=${pickupDate}&end_date=${returnDate}`)
          .then(response => response.json())
          .then(data => {
            if (data.available) {
              // Redirect to reservation page
              window.location.href = this.action + '?agency=' + 
                document.getElementById('pickup-location').value + 
                '&start_date=' + pickupDate + 
                '&end_date=' + returnDate;
            } else {
              alert('Sorry, this car is not available for the selected dates.');
            }
          })
          .catch(error => {
            console.error('Error checking availability:', error);
          });
        */
      });
    }
  });
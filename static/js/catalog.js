document.addEventListener('DOMContentLoaded', function() {
    // Price range slider
    const priceRange = document.getElementById('price-range');
    const priceValue = document.getElementById('price-value');
    
    if (priceRange && priceValue) {
      priceRange.addEventListener('input', function() {
        priceValue.textContent = this.value + '€';
      });
    }
    
    // Filter form reset
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
      filterForm.addEventListener('reset', function() {
        // Wait for the form to reset
        setTimeout(() => {
          // Update price value display
          if (priceRange && priceValue) {
            priceValue.textContent = priceRange.value + '€';
          }
          
          // Submit form to apply reset
          this.submit();
        }, 10);
      });
    }
    
    // Sort select change
    const sortSelect = document.getElementById('sort');
    if (sortSelect) {
      sortSelect.addEventListener('change', function() {
        // Update hidden sort input in filter form
        const sortInput = document.querySelector('input[name="sort"]');
        if (sortInput) {
          sortInput.value = this.value;
          
          // Submit the form
          if (filterForm) {
            filterForm.submit();
          }
        }
      });
    }
    
    // Pagination
    const pageButtons = document.querySelectorAll('.page-number');
    if (pageButtons.length > 0) {
      pageButtons.forEach(button => {
        button.addEventListener('click', function() {
          const page = this.getAttribute('data-page');
          
          // Create URL with page parameter
          const url = new URL(window.location.href);
          url.searchParams.set('page', page);
          
          // Navigate to the URL
          window.location.href = url.toString();
        });
      });
    }
    
    // Previous/Next page buttons
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    
    if (prevPageBtn) {
      prevPageBtn.addEventListener('click', function() {
        if (!this.disabled) {
          const currentPage = parseInt(document.querySelector('.page-number.active').getAttribute('data-page'));
          
          if (currentPage > 1) {
            const url = new URL(window.location.href);
            url.searchParams.set('page', currentPage - 1);
            window.location.href = url.toString();
          }
        }
      });
    }
    
    if (nextPageBtn) {
      nextPageBtn.addEventListener('click', function() {
        if (!this.disabled) {
          const currentPage = parseInt(document.querySelector('.page-number.active').getAttribute('data-page'));
          const totalPages = document.querySelectorAll('.page-number').length;
          
          if (currentPage < totalPages) {
            const url = new URL(window.location.href);
            url.searchParams.set('page', currentPage + 1);
            window.location.href = url.toString();
          }
        }
      });
    }
  });
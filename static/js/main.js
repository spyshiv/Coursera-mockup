jQuery(function($){

// 1. SEARCH FORM

   jQuery('#co-search-icon').on('click', function(event) {
        event.preventDefault();
        $('#co-search').addClass('co-search-open');
        $('#co-search form input[type="search"]').focus();
    });
    
    jQuery('.co-search-close').on('click', function(event) {
      $("#co-search").removeClass('co-search-open');
    });

});
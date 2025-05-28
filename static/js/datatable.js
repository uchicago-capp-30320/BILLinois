new DataTable('#search', {
    paging: false,
    searching: false,
    // prevent sorting in favorites column (because datatables doesn't allow sorting by icon)
    columnDefs: [{ orderable: false, targets: -1 }] 
  });
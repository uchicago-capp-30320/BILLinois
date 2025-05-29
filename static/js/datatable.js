new DataTable("#search", {
  paging: false,
  searching: false,
  info: false, //exclude showing 1 of x entries
  // prevent sorting in favorites column (because datatables doesn't allow sorting by icon)
  columnDefs: [{ orderable: false, targets: -1 }],
});

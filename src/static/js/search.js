$(document).ready(function(){
    search_doctor = $("#search-doctor")
    search_facility = $("#search-facility")
    search_issue = $("#search-issue")

    search_doctor_form = $("#search-doctor-form")
    search_facility_form = $("#search-facility-form")
    search_issue_form = $("#search-issue-form")
    $(search_doctor).on("click", function() {
        search_doctor_form.attr("class", "d-flex home-search justify-content-center");
        search_facility_form.attr("class", "d-none");
        search_issue_form.attr("class", "d-none");

        search_doctor.attr("class", "search-menu-active");
        search_facility.removeClass("search-menu-active")
        search_issue.removeClass("search-menu-active")
    });
    $(search_facility).on("click", function() {
        search_doctor_form.attr("class", "d-none");
        search_facility_form.attr("class", "d-flex home-search justify-content-center");
        search_issue_form.attr("class", "d-none");

        search_facility.attr("class", "search-menu-active");
        search_doctor.removeClass("search-menu-active")
        search_issue.removeClass("search-menu-active")
    });
    $(search_issue).on("click", function() {
        search_doctor_form.attr("class", "d-none");
        search_facility_form.attr("class", "d-none");
        search_issue_form.attr("class", "d-flex home-search justify-content-center");

        search_issue.attr("class", "search-menu-active");
        search_doctor.removeClass("search-menu-active")
        search_facility.removeClass("search-menu-active")
    });

})
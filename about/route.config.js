angular
    .module('app.about')
    .config(routeConfig);

function routeConfig($stateProvider) {
    $stateProvider
        .state('about', {
            abstract: true,
            url: "/about",
            templateUrl: "app/layout/content.html"
        })
        .state('about.list', {
            url: "/page",
            templateUrl: "about/list.html",
            controller: aboutController
        })




}
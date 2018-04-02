angular
    .module('app.profile')
    .config(routeConfig);

function routeConfig($stateProvider) {
    $stateProvider
        .state('profile', {
            abstract: true,
            url: "/profile",
            templateUrl: "app/layout/content.html"
        })
        .state('profile.list', {
            url: "/page",
            templateUrl: "profile/list.html",
            controller: profileListController
        })
        .state('profile.edit', {
            url: "/edit/:id",
            templateUrl: "profile/edit.html",
            controller: profileController
        })
        .state('profile.create', {
            url: "/create",
            templateUrl: "profile/create.html",
            controller: profileController
        })


}
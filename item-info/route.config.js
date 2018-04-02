angular
    .module('app.item-info')
    .config(routeConfig);

function routeConfig($stateProvider) {
    $stateProvider
        .state('item-info', {
            abstract: true,
            url: "/item-info",
            templateUrl: "app/layout/content.html"
        })
        .state('item-info.list', {
            url: "/item-info",
            templateUrl: "item-info/item-info.html",
            controller: itemPageController
        })
        .state('item-info.edit', {
            url: "/edit/:id",
            templateUrl: "item-info/edit.html",
            controller: itemPageController
        })
        .state('item-info.create', {
            url: "/create",
            templateUrl: "item-info/create.html",
            controller: itemPageController
        })


}
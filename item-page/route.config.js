angular
    .module('app.item-page')
    .config(routeConfig);

function routeConfig($stateProvider) {
    $stateProvider
        .state('item-page', {
            abstract: true,
            url: "/item-page",
            templateUrl: "app/layout/content.html"
        })
        .state('item-page.list', {
            url: "/item-page",
            templateUrl: "item-page/item-page.html",
            controller: itemPageController
        })
        .state('item-page.edit', {
            url: "/edit/:id",
            templateUrl: "item-page/edit.html",
            controller: itemPageController
        })
        .state('item-page.create', {
            url: "/create",
            templateUrl: "item-page/create.html",
            controller: itemPageController
        })


}
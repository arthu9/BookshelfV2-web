angular
    .module('app.g', [])
    .controller('mainController', mainController)
    .config(routeConfig);

function mainController($scope, $http, $state, $window, authService) {
    $scope.currentUser = JSON.parse($window.localStorage.getItem('user'));
    $scope.loginUser = function (form) {
        var username = form.username;
        var password = form.password;

        authService.obtainToken(username, password)
            .then(function (result) {
                $scope.currentUser = $window.localStorage.getItem('user');
                if (result.success) {
                    $state.go('index.home', {reload: true});
                }
            });
    };
}

function routeConfig($stateProvider) {
    $stateProvider
        .state('auth', {
            abstract: true,
            url: "/auth",
            templateUrl: "app/layout/content.html"
        })
        // .state('auth.login', {
        //     url: "/login",
        //     templateUrl: "js/dashboard/login.html",
        //     controller: mainController
        // })
}
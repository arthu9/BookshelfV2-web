(function () {
    angular
        .module('app.main')
        .controller('FooterController', FooterController);


    function FooterController($scope, $http, $localStorage, releaseService) {
        var vm = this;

        vm.$storage = $localStorage;

    }


})();

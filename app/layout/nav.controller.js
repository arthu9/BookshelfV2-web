(function () {
    angular
        .module('app.main')
        .controller('NavbarController', NavbarController);


    function NavbarController($scope, $window, $state, $localStorage,
                              $sessionStorage, jwtHelper, authManager, authService) {
        var vm = this;
        vm.$storage = $localStorage;
 
        $scope.state = $state;
        vm.logoutUser = function () {
            authService.unauthenticate();
        };
        if(vm.$storage.user) {
            $scope.fullname = vm.$storage.user.firstname + " " + vm.$storage.user.lastname;
        }
        else {
            $scope.fullname = 'Guest';
        }

    }
})();
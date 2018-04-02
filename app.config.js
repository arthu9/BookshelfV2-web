angular
    .module('bookshelf')
    .config(jwtConfig)
    .config(routeConfig)
    .run(run)
    .controller('loginController', loginController)
    .controller('signupController', signupController)
    .controller('forgotPasswordController', forgotPasswordController)
    .controller('changePasswordController', changePasswordController);


function jwtConfig($httpProvider, $localStorageProvider, jwtOptionsProvider) {

    jwtOptionsProvider.config({
        tokenGetter: function () {
            return $localStorageProvider.get('token');
        },
        loginPath: '/login',
        unauthenticatedRedirectPath: '/home'
    });

    $httpProvider.interceptors.push('jwtInterceptor');
}

function routeConfig($stateProvider) {
    $stateProvider
        .state('index', {
            abstract: true,
            url: "",
            templateUrl: "app/layout/content.html"
        })
        .state('index.home', {
            url: "/",
            templateUrl: "site/home.html"
            //controller: homeController
        })
        .state('index.login', {
            url: "login",
            templateUrl: "login/login.html",
            controller: loginController
        })
        .state('index.create', {
            url: "signup",
            templateUrl: "login/signup.html",
            controller: signupController
        })
        .state('index.forgot', {
            url: "forgot-password",
            templateUrl: "login/forgot_password.html",
            controller: forgotPasswordController
        })
        .state('index.change', {
            url: "change-password",
            templateUrl: "login/change_password.html",
            controller: changePasswordController
        })
        .state('index.confirmed', {
            url: "confirmed",
            templateUrl: "login/confirmed.html"
        })

}

function run($state, $rootScope, $localStorage, $location, authManager, authService, jwtHelper, SweetAlert) {
    // Use the authManager from angular-jwt to check for
    // the user's authentication state when the page is
    // refreshed and maintain authentication
    authManager.checkAuthOnRefresh();

    // Listen for 401 unauthorized requests and redirect
    // the user to the login page
    // Not working
    authManager.redirectWhenUnauthenticated();
    if ($localStorage.token) {
        var isExpired = jwtHelper.isTokenExpired($localStorage.token);
        if (isExpired)
            authService.unauthenticate();
    }
    $rootScope.$state = $state;

    $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
        if (toState.url === "login") {
            $location.path('/login');
        }if (toState.url === "signup") {
            $location.path('/signup');
        }
        // else if (toState.url === "change-password") {
        //     $location.path('/change-password');
        // }
        // else if (toState.url === "confirmed") {
        //     $location.path('/confirmed');
        // }
        // else if (toState.url === "forgot-password") {
        //     $location.path('/forgot-password');
        // }
        if (!$localStorage.isAuthenticated) {
             $state.go('index.home', {}, {reload: true});
        }
        // else if (toState.name === "userAccount.create") {
        //     console.log(event);
        //     SweetAlert.swal({
        //             title: "Number of Users Reach Limit",
        //             type: "warning",
        //             showCancelButton: true,
        //             confirmButtonColor: "#DD6B55",
        //             confirmButtonText: "Upgrade now!",
        //             closeOnConfirm: true
        //         },
        //         function (isConfirm) {
        //             if (isConfirm) {
        //                 $state.go('subscription.view', {}, {reload: true});
        //             }
        //         });
        // }
        // else if (toState.name === "server.create") {
        //     SweetAlert.swal({
        //             title: "Number of Servers Reach Limit",
        //             type: "warning",
        //             showCancelButton: true,
        //             confirmButtonColor: "#DD6B55",
        //             confirmButtonText: "Upgrade now!",
        //             closeOnConfirm: true
        //         },
        //         function (isConfirm) {
        //             if (isConfirm) {
        //                 $state.go('subscription.view', {}, {reload: true});
        //             }
        //         });
        // }


    });
}

function loginController($scope, authManager, authService) {
    $scope.loginUser = function (form) {
        var username = form.username;
        var password = form.password;

        authService.obtainToken(username, password)
            .then(function (result) {
                    if (result.success) {
                        authManager.authenticate();
                        authService.authenticate(result.token, result.user);
                    }
                }
            );

    };
}

function signupController($scope, $state, $http, alerts) {
    $scope.signupUser = function (form) {

        // if(form.company_name && form.username && form.email && form.password === form.confirm_password) {
        //    return $http.post('/api/admin-create/', {
        //     company_name: form.company_name, username: form.username, firstname: form.firstname,
        //     lastname: form.lastname, email: form.email,
        //     password: form.password, confirm_password: form.confirm_password,
        //     role: 'a'
        // })
        //     .then(function (result) {
        //         alerts.success('Account Successfully Created!', true);
        //         $state.go('index.login', {success: true}, {reload: true});
        //     },
        //     function (result) {
        //         alerts.error("Error! Please check and try again", true);
        //     })
        // }
        // else {
        //     alerts.error("Error! Please check and try again", true);
        //
        //     //5 seconds timeout
        //     $timeout(function () {
        //         alerts.clearMessages();
        //     }, 2500);
        // }
    };
}

function forgotPasswordController($scope, $state, $http, alerts) {
    $scope.forgot_password = function (form) {
        // return $http.post('/api/forgot-password/', {
        //     email: form.email
        // })
        //     .then(function (result) {
        //         alerts.success('Email Sent!', true);
        //         $state.go('index.login', {success: true}, {reload: true});
        //     },
        //     function (result) {
        //         alerts.error("Error! Please check and try again", true);
        //     });
    };
}

function changePasswordController($scope, $state, $http, alerts, $timeout) {

    function getUrlVars() {
        var vars = {};
        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
            vars[key] = value;
        });
        return vars;
    }

    console.log(getUrlVars()["username"]);

    $scope.change_password = function (form) {
        // if (form.new_password === form.confirm_password) {
        //     return $http.post('/api/change-password/', {
        //         user_name: getUrlVars()["username"], new_password: form.new_password,
        //         confirm_password: form.confirm_password
        //     })
        //         .then(function (result) {
        //             alerts.success('Password Successfully Changed!', true);
        //             $state.go('index.login', {success: true}, {reload: true});
        //         },
        //         function (result) {
        //             alerts.error("Error! Please check and try again", true);
        //         });
        // }
        // else {
        //     alerts.error("Both Password didn't match", true);
        //
        //     //5 seconds timeout
        //     $timeout(function () {
        //         alerts.clearMessages();
        //     }, 2500);
        // }
    };
}
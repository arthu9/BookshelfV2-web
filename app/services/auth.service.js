angular
    .module('app.main')
    .factory('authService', function ($state, $filter, $http, $window, $resource, $localStorage,
                                      $sessionStorage, jwtHelper, alerts, SweetAlert) {

        return {
            obtainToken: function (username, password) {
                return $http.post('/api-token-auth/', {username: username, password: password})
                    .then(function (result) {
                        return {
                            success: true, token: result.token, user: result.user
                        }
                    }, function () {
                        alerts.error("Username or Password Didn't Match.", true);
                    });
            },
            authenticate: function (token, user, membership, subscription) {
                $localStorage.isAuthenticated = true;
                $localStorage.token = token;
                $localStorage.user = user;

                $state.go('index.list', {
                    limit: 10, offset: 0, sort: 'name', order: 'desc',
                    username: $localStorage.user.username
                }, {reload: true});
            },
            unauthenticate: function () {
                $localStorage.$reset({
                    isAuthenticated: false,
                    user: null,
                    token: null
                });

                $state.go('index.login', {}, {reload: true});
            }

        };
    });

(function () {
    angular
        .module('app.main')
        .config(growlConfig)
        .config(httpConfig)
        .config(routeConfig)
        .filter('sumByKey', sumByKey)
        .directive('stringToNumber', stringToNumber)
        .run(run);

    function run($state, $rootScope) {
        $rootScope.$state = $state;
    }

    function routeConfig($urlRouterProvider, $resourceProvider) {
        $urlRouterProvider.otherwise("/");
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }

    function growlConfig($urlRouterProvider, $stateProvider, $resourceProvider, growlProvider, $httpProvider, $localStorageProvider) {
        growlProvider.onlyUniqueMessages(true);
        growlProvider.globalTimeToLive({success: 2000, error: -1, warning: 3000, info: 4000});
        growlProvider.globalDisableCountDown(true);
    }

    function httpConfig($urlRouterProvider, $stateProvider, $resourceProvider, growlProvider, $httpProvider, $localStorageProvider) {
        $httpProvider.interceptors.push('xmlHttpInterceptor');
        $httpProvider.interceptors.push(growlProvider.serverMessagesInterceptor);
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }

    function sumByKey() {
        return function (data, key) {
            if (typeof (data) === 'undefined' || typeof (key) === 'undefined') {
                return 0;
            }

            var sum = 0;
            for (var i = data.length - 1; i >= 0; i--) {
                var val = parseInt(data[i][key]);
                if (!isNaN(val))
                    sum += val;
            }

            return sum;
        };
    }

    function stringToNumber() {
        return {
            require: 'ngModel',
            link: function (scope, element, attrs, ngModel) {
                ngModel.$parsers.push(function (value) {
                    return '' + value;
                });
                ngModel.$formatters.push(function (value) {
                    return parseFloat(value, 10);
                });
            }
        };
    }


})();
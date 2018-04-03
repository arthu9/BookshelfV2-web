(function () {
    'use strict';

    angular
        .module('bookshelf',
            [

                /*
                 * Re-usable components
                 * */
                'app.main',

                // Auth
                'angular-jwt',
                'angular-storage',
                'ngStorage',

                /*
                 * Third Party Modules
                 * */
                'xml',
                'ngResource',
                'ui.router',
                'ngRoute',
                'ngSanitize',
                'ui.bootstrap',
                'ui.bootstrap.tpls',
                'ui.bootstrap.pagination',
                'ui.bootstrap.alert',

                'mgcrea.ngStrap',
                'mgcrea.ngStrap.timepicker',
                'mgcrea.ngStrap.datepicker',
                'angular-growl',
                'oitozero.ngSweetAlert',
                'angular.morris'
            ]);
})();

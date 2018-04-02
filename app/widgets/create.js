/*
 * Needs the following scope variables to be defined in the main controller:
 * - modelName
 * - form
 * - formState
 * - api - derived from dataService.getApi
 * - item
 * */
(function () {
    angular
        .module('app.main')
        .directive('mainCreate', function () {
            return {
                restrict: 'EA',
                transclude: true,
                templateUrl: 'app/widgets/create.html',
                controller: function ($scope, $state, alerts) {

                    function saveErrorCallback(response) {
                        console.log(response);
                        $scope.formState.saving = false;
                        alerts.error('Something went wrong. Please try again.', true);
                    }

                    $scope.doSave = function (item, success) {
                        console.log(item);
                        $scope.formState.saving = true;
                        alerts.clearMessages();

                        if ($scope.validateItem(item)) {
                            var obj = new $scope.api(item);
                            obj.$save(function (response) {
                                $scope.formState.saving = false;
                                $scope.item = {};
                                alerts.success(response.id + ' created.', true);
                                success();
                            }, saveErrorCallback);
                        } else {
                            alerts.showNow();
                            $scope.formState.saving = false;
                        }

                    };

                    $scope.create = function (item) {
                        $scope.doSave(item, function () {
                        });
                        $scope.form.$setPristine();
                        $state.go($scope.modelName + '.create', {}, {reload: true});
                    };

                    $scope.createAndClose = function (item) {
                        $scope.doSave(item, function () {
                            $scope.form.$setPristine();
                            $scope.close(item);
                        });
                    };

                    $scope.createAndNew = function (item) {
                        $scope.doSave(item, function () {
                        });
                        $scope.form.$setPristine();                        
                        $state.go($scope.modelName + '.create', {}, {reload: true});
                        
                    };

                    $scope.close = function (item) {
                            $state.go($scope.modelName + '.list', {limit: 10, offset: 0});
                    };

                    //TODO: REFACTOR!
                    $scope.toggleLock = toggleLock;

                    function toggleLock() {
                        if (!$scope.item.locked) {
                            $scope.item.locked = true;
                            $scope.create($scope.item);
                        } else {
                            $scope.item.locked = !$scope.item.locked;
                        }

                    }
                }
            }
        });
})();
(function () {
    angular
        .module('app.main')
        .directive('mainUpdate', function () {
            return {
                restrict: 'EA',
                transclude: true,
                templateUrl: 'app/widgets/update.html',
                controller: function ($scope, $state, SweetAlert, alerts) {

                    function saveErrorCallback(response) {
                        console.log(response);
                        $scope.formState.saving = false;
                        alerts.error('Something went wrong. Please try again.', true);
                    }

                    function deleteSuccess(data) {
                        alerts.addMessages(data.id + ' deleted', true);
                        $scope.formState.saving = false;
                        $scope.form.$setPristine();
                        $scope.close();
                    }

                    $scope.doSave = function (item, success) {
                        $scope.formState.saving = true;
                        alerts.clearMessages();
                        console.log(item);
                        if ($scope.validateItem(item)) {
                            $scope.api.update({id: $state.params.id}, new $scope.api(item), function (response) {
                                $scope.formState.saving = false;
                                alerts.success(response.id + ' updated', true);
                                success(response.item);
                            }, saveErrorCallback);
                        } else {
                            alerts.showNow();
                            $scope.formState.saving = false;
                        }

                    };

                    $scope.update = function (item) {
                        $scope.doSave(item, function (data) {
                            $scope.form.$setPristine();
                            $state.go($scope.modelName + '.edit', {id: $state.params.id});
                        });
                    };

                    $scope.updateAndClose = function (item) {
                        $scope.doSave(item, function (data) {
                            $scope.form.$setPristine();
                            $scope.close();
                        });
                    };

                    $scope.updateAndDelete = function () {
                        SweetAlert.swal({
                                title: "Are you sure?",
                                text: "Are you sure you want to delete this?",
                                type: "warning",
                                showCancelButton: true,
                                confirmButtonColor: "#DD6B55",
                                confirmButtonText: "Yes, delete it!",
                                closeOnConfirm: true
                            },
                            function (isConfirm) {
                                if (isConfirm) {
                                    $scope.formState.saving = true;
                                    var obj = new $scope.api($scope.item);
                                    obj.$delete(deleteSuccess);
                                    $scope.close();
                                }
                            });
                    };

                    $scope.close = function (item) {
                        $state.go($scope.modelName + '.list', {limit: 10, offset: 0});
                    };

                    //TODO: REFACTOR!
                    $scope.toggleLock = toggleLock;

                    function toggleLock() {

                        if (!$scope.item.locked) {
                            $scope.item.locked = true;
                            $scope.update($scope.item);
                        } else {
                            $scope.item.locked = !$scope.item.locked;
                        }

                    }
                }
            }
        });
})();
/*
 * Needs the following scope variables to be defined in the main controller:
 * - modelName
 * - list
 * - listOptions
 * - maxRanges
 * - fields
 * - filters
 * */
angular
    .module('app.main')
    .directive('mainCustomTable', function () {
        return {
            restrict: 'EA',
            transclude: true,
            templateUrl: 'app/widgets/no-button-table.html',
            controller: function ($scope, $state) {

                $scope.refreshList = refreshList;
                $scope.changeOptionAndRefresh = changeOptionAndRefresh;
                $scope.changeLimit = changeLimit;
                $scope.selectPage = selectPage;
                $scope.pageChanged = pageChanged;

                function refreshList() {
                    var options = angular.copy($scope.listOptions);
                    delete options.total;
                    delete options.currentPage;
                    $state.go($scope.modelName + ".list", options, {reload: true});
                }

                function changeOptionAndRefresh(field, value) {
                    $scope.listOptions[field] = value;
                    $scope.refreshList(); // Update When changed.
                }

                function changeLimit(limit) {
                    $scope.listOptions.offset = 0;
                    $scope.changeOptionAndRefresh("limit", limit);
                }

                function selectPage(page) {
                    $scope.changeOptionAndRefresh("offset", $scope.listOptions.limit * (page - 1));
                }

                function pageChanged() {
                    $scope.selectPage($scope.listOptions.currentPage);
                }
            }
        }
    });
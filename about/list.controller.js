angular
    .module('app.about')
    .controller('aboutController', aboutController);

function aboutController($state, $scope, dataService, $localStorage) {
    var filters = [
        {'id': 'all', 'name': 'All'},
        {'id': 'active', 'name': 'Active'},
        {'id': 'inactive', 'name': 'Not Active'}
    ];

    var fields = [
        {
            'id': 'firstname',
            'name': 'firstname'
        }
    ];

    $scope.storage = $localStorage;
    $scope.modelName = 'about';
    $scope.listOptions = dataService.getListOptions();
    $scope.listLoaded = false;
    $scope.maxRanges = [10, 20];
    $scope.fields = fields;
    $scope.filters = filters;

    //loadList();

    function loadList() {
        dataService
            .getApi('api/useraccounts-list')
            .list($state.params, function (data) {
                $scope.list = data.results;
                $scope.listOptions.total = data.count;
                $scope.listOptions.currentPage = Math.ceil($scope.listOptions.offset / $scope.listOptions.limit) + 1;
                $scope.listLoaded = true;
            });
    }
}
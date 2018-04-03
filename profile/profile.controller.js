angular
    .module('app.profile')
    .controller('profileController', profileController);


function profileController($state, $scope, alerts, $localStorage, dataService) {
    alerts.clearMessages();

    $scope.storage = $localStorage;
    $scope.modelName = 'profile';
    $scope.api = dataService.getApi('api/useraccounts');
    $scope.formState = {loaded: false, saving: false};
    $scope.validateItem = validateItem;
    $scope.temp = [];

    loadItem();
    function loadItem() {
        $scope.item = [];
        $scope.formState.loaded = true;
        $scope.isEdit = false;

        if ($state.params.id) {
            $scope.api.query({uid: $state.params.id}, function (response) {
                $scope.formState.loaded = false;
                $scope.item = response[0];
                $scope.isEdit = true;
            });
        }
    }

    /* Override for default impls */
    function validateItem(item) {
        return true;
    }
}
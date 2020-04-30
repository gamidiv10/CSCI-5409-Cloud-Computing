var myapp = angular.module('gutenberg', []);

myapp.controller('appController', ['$scope' , '$http', function($scope, $http) {
    console.log("app controller");
    $scope.isInitialized = false;
    
    $scope.search = function(){
        $scope.hideVar = false;
        $http.get('/search/'.concat($scope.keyword)).then(function(response) {
            $scope.rows = response.data;
            $scope.isInitialized = true;
        });
    }

    $scope.save = function(){
        $scope.isInitialized = true;
        var data = {'note': $scope.note, 'keyword': $scope.keyword };
        $http.post('/notes', data).then(function(response) {
            console.log(response.data);
        });
        $scope.note = '';
    }

    $scope.retrieve = function(){
        $scope.isInitialized = true;
        $scope.hideVar = true;
        $http.get('/retrieve/'.concat($scope.keyword)).then(function(response) {
            $scope.rows = response.data;
        });
    }

    $scope.clear = function() {
        $scope.note = '';
    };
}]);
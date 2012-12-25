(function () {
'use strict';


var qontour = angular.module('qontour', []);

qontour.controller('ImageListCtrl', function($scope, Images) {
    Images.get().success(function (data) {
        $scope.imageResults = data;
    });

});

qontour.service('Images', function($http) {
    this.get = function () {
        return $http.get('/ilist?q=dragon');
    };
});

})();

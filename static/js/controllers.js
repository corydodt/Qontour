'use strict';

/* Controllers */


function ImageListCtrl($scope) {
    // $scope.imageResults = ImageSearch.query({q: 'displacer'});
    $scope.imageResults = [
        {label: 'a.jpg', url: '/static/i/a.jpg'},
        {label: 'b.jpg', url: '/static/i/b.jpg'}
        ];
}
// ImageList.$inject = [];


/// function MyCtrl2() {
/// }
/// MyCtrl2.$inject = [];

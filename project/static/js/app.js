(function(){
    var app = angular.module("CloudDDS", []);

    app.directive('followingHeader', function(){
        return {
            restrict: 'E',
            templateUrl: 'template/views/following-header.html'
        };
    });

    

})();